import streamlit as st
from utils_cdmx import *
import altair as alt

# Define session variables to share between reruns
# If not available we initialize to None
if 'main_df' not in st.session_state:
    st.session_state['main_df'] = crime_data

if 'results' not in st.session_state:
    st.session_state['results'] = None

if 'map_chart' not in st.session_state:
    st.session_state['map_chart'] = None

# Application starts here

st.title("Delitos en Carpetas de Investigación CDMX")

st.markdown("***")

# App description and data source
st.markdown("""
El siguiente gráfico muestra un mapa de la Ciudad de México con el número de delitos en carpetas de investigación a nivel de colonias.
Una __carpeta de investigación__ constituye un expediente que recopila los datos de una investigación realizada por las autoridades sobre 
la comisión de un delito y que se crea a partir de una denuncia formal. Los datos para generar la visualizacion se obtuvieron de la página 
oficial de datos abiertos de la CDMX. Esta base de datos contiene información acerca de las carpetas de investigación durante el 
periodo 2016-2023 y representa una muestra del total de delitos cometidos diariamente en la Ciudad de México. 
            
Para utilizar esta aplicación seleccione el periodo de visualización y la categoria de delito que desea explorar. También ouede seleccionar
entre Dia, Mes, y Año, para mostrar el número de delitos cometidos por categoria. 
""")

st.caption("""
_Fuentes_: 
\n (Carpetas de Investigación) https://datos.cdmx.gob.mx/dataset/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico
\n (Datos Geográficos) https://datos.cdmx.gob.mx/dataset/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico
""")

st.markdown("***")

# This is a slide selector
date_range = st.slider("Choose a range date", 
                           min_date.date(), 
                           max_date.date(),
                           (min_date.date(), max_date.date()),
                           label_visibility="collapsed",
                           help="Select date range",
                           )

# We need to convert date_range to adatetime object
date_range_min = pd.to_datetime(date_range[0])
date_range_max = pd.to_datetime(date_range[1])

# filter data based on min and max dates and store as a session variable
results = filter_data_based_on_dates(crime_data, date_range_min, date_range_max)
st.session_state.results = results

# Two columns layout
col1, col2 = st.columns([0.35, 0.65])

# Define content of column 1
with col1:

    # Category selector. The map will only show data for this category
    category = st.selectbox(label="Select category", 
                              options=crime_categories,
                              placeholder="Choose categories to show:",
                              label_visibility="collapsed")
        

    # This function creates a dataframe containing information about
    # neighborhoods and the number of crimes for the selected category 
    crimes_per_neighborhood = create_crime_dataframe(st.session_state.results, category=category)
    crimes_per_neighborhood = crimes_per_neighborhood[~(crimes_per_neighborhood[category] == 0)]

    var_to_plot = f"{category}:Q"

    # Downloads data to create the map. Using a URL is the only way to create this visualization
    # in streamlit. 
    url_geojson = "https://raw.githubusercontent.com/AlbertoR94/ProyectoFinalFEC/main/colonias_cdmx.json"
    data_url_geojson = alt.Data(url=url_geojson, format=alt.DataFormat(property="features"))


    # Here we show some metrics
    # Total crimes (for selected category)
    total_crimes = crimes_per_neighborhood[category].sum()
    st.markdown("### Delitos en Carpetas de Investigación:")
    st.markdown(f"###     {total_crimes:,}      ")

    # Max crime count neighborhood
    max_crime_data = crimes_per_neighborhood.sort_values(by=category, ascending=False).head(1)
    max_crime_neighborhood = max_crime_data.Colonia.values[0]
    max_crime_count = int(max_crime_data[category].values[0])
   
    st.markdown("#### Colonia con Mayor Número de Carpetas de Investigación:")
    col1.metric(max_crime_neighborhood, f"{max_crime_count:,}", delta=None)

    # define table 

    # Category selector. The map will only show data for this category
    time_category = st.selectbox(label="Select category", 
                              options=["Año", "Mes", "Dia"],
                              placeholder="Choose categories to show:",
                              label_visibility="collapsed")

    color = alt.Color('categoria:N', legend=None).scale(scheme='darkred')
    click = alt.selection_point(encodings=['color'])

    bars = alt.Chart(my_new_df).mark_bar().encode(
    x=alt.X('count()').title('Número de Carpetas de Investigación'),
    y=alt.Y(f"{time_category.lower()}:N").title(time_category),
    color=alt.condition(click, color, alt.value('lightgray')),
    tooltip = alt.Tooltip(["categoria:N", "count()"]),
    ).properties(
        width=450,
    ).add_params(
        click
    )

    bars

    # define the map and its properties
    empty_chart = alt.Chart(data_url_geojson).mark_geoshape(fill='gray', stroke='white').encode(
        tooltip=["properties.colonia:N"]
    ).properties(
        width=900,
        height=700
    )

    # add crime data to the visualization
    crimes_chart = alt.Chart(data_url_geojson).mark_geoshape(stroke='white').transform_lookup(
        lookup="properties.colonia",
        from_=alt.LookupData(data=crimes_per_neighborhood, key="Colonia", fields=["Colonia", category])
    ).encode(
        alt.Color(f"{category}:Q").scale(type='log', scheme='darkred'),
        alt.Tooltip(["Colonia:N", f"{category}:Q"])
    ).properties(
        width=900,
        height=700
    )

    st.session_state.map_chart = empty_chart + crimes_chart


with col2:
    st.session_state.map_chart
    #st.altair_chart(empty_chart + crimes_chart)
    
with st.expander("Mostrar Tabla de Carpetas de Investigación", expanded=False):
    st.dataframe(crime_data.head(100))

