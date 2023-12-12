import streamlit as st
import streamlit.components.v1 as components

st.markdown("# European Football Analysis")

st.markdown("""
## Description
In this project, I analyze the Football Database, which can be downloaded at the following [link](https://www.kaggle.com/datasets/davidcariboo/player-scores). This database which contains information about football games, players, games events, and competitions from 2012-2022, can be used to reveal meaningful insights about the leading football leagues in Europe. 

According to [Wikipedia](https://en.wikipedia.org/wiki/Association_football), football is the most popular sport in the world with an estimated 250 million active players. Furthermore, millions of tv spectators watch football matches of their favorite clubs in domestic and international competitions. Competitions, clubs, and players provide an incredible data that can be processed and analyzed to reveal hidden patterns. 

To analyze the information in this database, I will use mainly PySpark, SQL, and other libraries to build some visualizations. PySpark is the Python API for Apache Spark and is a powerful tool for working with Big Data. Although this database is not large enough or complex to be considered Big Data, it provides a good starting point for learning PySpark and SQL.

The final results were written into a CSV file, "football_league_performance.csv", to create a Tableau [dashboard](https://public.tableau.com/views/EuropeanFootballLeagues_16879911046350/Dashboard1?:language=es-ES&:display_count=n&:origin=viz_share_linkv).

The code used to process and analyze data can be found here: [Github](https://github.com/AlbertoR94/European_Football_Analysis/blob/main/FootballProject.ipynb)
            """)

components.html("""<div class='tableauPlaceholder' id='viz1702419967983' style='position: relative'><noscript><a href='#'><img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Eu&#47;EuropeanFootballLeagues_16879911046350&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='EuropeanFootballLeagues_16879911046350&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Eu&#47;EuropeanFootballLeagues_16879911046350&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='es-ES' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1702419967983');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='1177px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>""",
                height=800)

st.markdown("To correctly visualize the Tableau Dashboard close the navigation bar.")
