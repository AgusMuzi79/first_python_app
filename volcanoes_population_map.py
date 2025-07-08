import folium
import pandas

# Volcanoes analysis
volcanoes = pandas.read_csv('Volcanoes.txt')
lat = list(volcanoes['LAT'])
lon = list(volcanoes['LON'])
name = list(volcanoes['NAME'])
elev = list(volcanoes['ELEV'])

# Generating a color from the volcanoes' elevation
def elevation_color (ev):
    if (ev <= 500):
        return 'darkgreen'
    elif (ev > 500 and ev <= 1000):
        return 'lightgreen'
    elif (ev > 1000 and ev <= 2000):
        return 'beige'
    elif (ev > 2000 and ev <= 3000):
        return 'lightgray'
    elif (ev > 3000 and ev <= 5000):
        return 'gray'
    else:
        return 'black'

# Creation of the map
map =  folium.Map(location = [39.80547597675833, -101.11965292527896], zoom_start=5, tiles='cartodb positron')

# Creating a group of folium childs
fgv =  folium.FeatureGroup(name = 'Volcanoes', control=True)


for lt, ln, nm, ev  in zip(lat, lon, name, elev):
    folium.Circle(
        location = [lt, ln], 
        color = 'black',
        weight = 1,
        fill_opacity = 1,
        opacity = 1,
        fill_color = elevation_color(ev),
        radius = 30000,
        tooltip = nm,
        popup = str(ev) + ' meters'
    ).add_to(fgv)

fgp =  folium.FeatureGroup(name = 'Population', control=True)
geojson_data = open('world.json', 'r', encoding='utf-8-sig').read()

folium.GeoJson(
    geojson_data,
    name="World Population",
    style_function=lambda x: {
        "fillColor": "green"
        if x["properties"]["POP2005"] < 10000000
        else "orange"
        if x["properties"]["POP2005"] < 50000000
        else "red",
        "color": "black",
        "weight": 1,
        "dashArray": "5, 5",
    },
).add_to(fgp)

fgv.add_to(map)
fgp.add_to(map)
folium.LayerControl().add_to(map)


map.save('index.html')



    