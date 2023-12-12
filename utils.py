import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

from collections import Counter
from itertools import chain
from argparse import Namespace

import pandas as pd
import numpy as np

import os
import re
import string

seed = 42

def preprocess_string(text_string):
    """
    Converts text string to lowercase and removes punctation.

    Args:
    text_string (str): text string to process.
    
    Returns:
    text_string (str): processed text string.
    """
    text_string = text_string.lower()
    text_string = re.sub(r'[!"#@$%&\'()*+,-./:;<=>?\[\]^_`{|}~]', 
                         r"", text_string)
    text_string = re.sub(r'\b\d+\b', r"", text_string)
    text_string = re.sub(r'  ', r" ", text_string)
    
    return text_string


train_df = pd.read_csv("data/train.csv")

train_df.text = train_df.text.apply(preprocess_string)

# Split data into train and validation sets
X_train, X_val, y_train, y_val= train_test_split(train_df.drop(['target'], axis=1), 
                                                 train_df.target, 
                                                 test_size=0.20, 
                                                 stratify=train_df.target, 
                                                 random_state=seed)


class Vocabulary():
    def __init__(self, tokens):
        self.tokens = tokens

    @classmethod
    def fromDataframe(cls, dataframe, cutoff=30):
        counts = Counter([word for text in dataframe.text \
                          for word in text.split(" ")])
        tokens = ["unk"]
        for token, count in counts.items():
            if count >= cutoff:
                tokens.append(token)

        return cls(tokens)
            

class Vectorizer():
    """
    Class to convert text strings into a numerical representation
    """
    def __init__(self, vocabulary, dataframe):
        self.vocabulary = vocabulary
        
        def my_tokenizer(text):
            tokens = text.split(" ")
            tokens = [token if token in self.vocabulary.tokens else "unk" for token in tokens]
            return tokens
        
        self.tfidf = TfidfVectorizer(tokenizer=my_tokenizer, 
                                     vocabulary=vocabulary.tokens, 
                                     token_pattern=None)
        self.tfidf.fit(dataframe.text)
    
    def vectorize(self, row):
        text = self.tfidf.transform([row]).toarray().reshape(-1)
        return text
        
        
    @classmethod
    def fromDataframe(cls, dataframe, cutoff=30):
        vocabulary = Vocabulary.fromDataframe(dataframe, cutoff=cutoff)
        return cls(vocabulary, dataframe)


class CustomDataset(Dataset):
    """
    Class to handle vectorization and construction of the vocabulary
    """
    def __init__(self, vectorizer, train_df, test_df):
        """
        Args:
        dataframe (pandas.Dataframe): dataframe containing data 
            (must include a "text" and "target" columns)
        vectorizer (Vectorizer): a vectorizer instantiated from dataset
        """
        self.split = "train"

        self.train_df = train_df
        self.test_df = test_df
        self.set_split(self.split)
        
        self.vectorizer = vectorizer
        self.vocabulary = vectorizer.vocabulary.tokens

    @classmethod
    def fromDataframe(cls, train_df, test_df, cutoff=30):
        vectorizer = Vectorizer.fromDataframe(train_df, cutoff=cutoff)
        return cls(vectorizer, train_df, test_df)

    def __len__(self):
        """
        Returns the number of sample in the dataset.
        """
        return len(self.dataframe)

    def __getitem__(self, idx):
        """
        Loads and returns a sample from the dataset at the given index.
        """
        text = self.dataframe.iloc[idx].text
        text = self.vectorizer.vectorize(text)

        label = self.dataframe.iloc[idx].target
        return text, label

    def getVectorizer(self):
        return self.vectorizer

    def getVocabulary(self):
        return self.vocabulary

    def set_split(self, split):
        if split == "train":
            self.dataframe = self.train_df
        else:
            self.dataframe = self.test_df


class Classifier(nn.Module):
    """Classifier based on simple feed-forward neural network."""
    def __init__(self, n_features):
        super(Classifier, self).__init__()
        self.features = nn.Sequential(
            nn.Linear(in_features=n_features, out_features=32),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=1),
        )
        
    def forward(self, x):
        x = self.features(x).squeeze()
        return x
    

def predict_sentiment(review, classifier, vectorizer):
    """
    Predicts sentiment of review
    Args:
        review (str): a review string 
        classifier : model to make predictions
        vectorizer (Vectorizer): vectorizer to convert review string into a numerical representation
    
    returns:
        probability of sentiment being negative
    """
    X = vectorizer.vectorize(review)
    X = torch.tensor(X).view(1,-1).float()
    prediction = classifier(X)

    return torch.sigmoid(prediction).item()
    
# define important constants inside namespace
args = Namespace(
    # Data info
    cutoff = 10,
    vocab_size = 0,
    # Model hyperparameters
    learning_rate = 0.001,
    weight_decay=0.001,
    batchsize = 32,
    epochs = 30,
    early_stopping_criteria = 10,
    # runtime 
    device = 'cpu',
    model_state_file = 'model.pth',
    min_val_loss = float('inf')
)
    
# Instantiate dataset and vocabulary
reviewDataset = CustomDataset.fromDataframe(X_train, X_val, cutoff=args.cutoff)
vocabulary = reviewDataset.getVocabulary()

args.vocab_size = len(vocabulary) 

# Instantiate classifier
classifier = Classifier(n_features=args.vocab_size)
classifier.load_state_dict(torch.load(args.model_state_file))

vectorizer = reviewDataset.getVectorizer()



