import pandas as pd
import numpy as np

# define
day_of_week_dic = {0 : "Lun",
                   1 : "Mar",
                   2 : "Mie",
                   3 : "Jue",
                   4 : "Vie",
                   5 : "Sab",
                   6 : "Dom"}

day_of_week_func = lambda day_num : day_of_week_dic[day_num]

# load crime data
crime_data = pd.read_csv("data/crimes.csv")

# convert string date columns to datetime
crime_data["fecha_hecho"] = pd.to_datetime(crime_data["fecha_hecho"])
crime_data["fecha_inicio"] = pd.to_datetime(crime_data["fecha_inicio"])

crime_data["anio_hecho"] = crime_data["anio_hecho"].astype(int)

crime_data["day_of_week"] = crime_data.fecha_hecho.dt.day_of_week
crime_data["day_of_week"] = crime_data.day_of_week.apply(day_of_week_func)

#crime_data.set_index("fecha_hecho", inplace=True)

# Let's define min and max dates
min_date = crime_data.fecha_hecho.min()
max_date = crime_data.fecha_hecho.max()

# create a list of crime categories
crime_categories = ["ALL"]
crime_categories.extend(list(crime_data.categoria.unique()))

# load geometry file and define a list of neighborhoods
df_colonias = pd.read_csv("Data/colonias.csv")
colonias_gpd = list(df_colonias.colonia.sort_values().unique())

def filter_data_based_on_dates(df, start, end):
    """
    Filters a dataframe based on datetime column. Index must be a datetime column.
    """
    return df[((df.fecha_hecho >= start) & (df.fecha_hecho <= end))]


def create_crime_dataframe(filtered_dataframe, category):
    """
    Creates a dataframe of crimes by neighborhood
    """
    crimes_per_neighborhood = filtered_dataframe.dropna(axis=0, subset=["colonia_key"])
    crimes_per_neighborhood = crimes_per_neighborhood[crimes_per_neighborhood.colonia_key.isin(colonias_gpd)]

    crimes_per_neighborhood = crimes_per_neighborhood.groupby(["colonia_key", "categoria"]).count()[["delito"]]
    crimes_per_neighborhood.reset_index(inplace=True, drop=False)

    crimes_per_neighborhood = pd.pivot(crimes_per_neighborhood, index="colonia_key", columns="categoria", values="delito")
    crimes_per_neighborhood = crimes_per_neighborhood.fillna(0).astype(int)

    if category == "ALL":
        crimes_per_neighborhood = pd.DataFrame(crimes_per_neighborhood.sum(axis=1)).reset_index()
        crimes_per_neighborhood.columns = ["Colonia", "ALL"]
    else:
        crimes_per_neighborhood = crimes_per_neighborhood[[category]].reset_index()
        crimes_per_neighborhood.columns = ["Colonia", category]

    # crimes_per_neighborhood.reset_index(inplace=True, drop=False)
    return crimes_per_neighborhood


my_new_df = crime_data.groupby(["fecha_hecho", "categoria"]).count()[["delito"]]
my_new_df = my_new_df.reset_index()
my_new_df["año"] = my_new_df.fecha_hecho.dt.year
my_new_df["mes"] = my_new_df.fecha_hecho.dt.month 
my_new_df["dia"] = my_new_df.fecha_hecho.dt.day_of_week.apply(day_of_week_func)
