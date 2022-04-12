import folium
import pandas


def editName(x):
    z = ''
    for j in range(0, len(x), 1):
        if x[j] == ',':
            break
        z = z + x[j]
    return z


def pop_color(x):
    z = ''
    for j in range(0, len(x), 1):
        if x[j] == ',':
            j = j + 2
            z = x[j] + x[j+1]
            break
    if z == 'CA':
        return 'lightgreen'
    elif z == 'CO':
        return 'orange'
    elif z == 'FL':
        return 'lightblue'
    else:
        return 'red'


def city_color(x):
    if x<=100:
        return '#ffa07a'
    elif 100 < x <= 500:
        return '#fa8072'
    elif 500 < x <= 1000:
        return '#ff6347'
    elif 1000 < x <= 2500:
        return '#cd5c5c'
    elif 2500 < x <= 5000:
        return '#ff4500'
    elif 5000 < x <= 7500:
        return '#dc143c'
    elif 7500 < x <= 10000:
        return '#b22222'
    elif 10000 < x <= 500000:
        return '#8b0000'
    else:
        return '#560319'


def displayPopulation(x):
    z = ""
    y = str(x)
    for i in range(0, len(y), 1):
        if i !=0:
            if i % 3 == 0:
                z = "," + z
        z = y[len(y)-i-1] + z

    return z


map1 = folium.Map(location=[39.23, -102.28], zoom_start=5)

data = pandas.read_csv("Whole Foods Data.csv")
lat = list(data["lat"])
lon = list(data["lon"])
name = list(data["Location"])

fg_stores = folium.FeatureGroup(name="Whole Food Stores(US)")
for i in range(0, len(lat), 1):
    fg_stores.add_child(folium.Marker(location=[lat[i], lon[i]], radius=6, popup=editName(name[i]),
                                      icon=folium.Icon(color=pop_color(name[i]))))

# We will have polygon displayed on the map now
# We will now have each state coloured as per its population
fg_stateLines = folium.FeatureGroup(name="State Lines(US)")
fg_stateLines.add_child(folium.GeoJson(data=open('US popu.json', 'r', encoding='utf-8-sig').read(),
                                       style_function=lambda x: {'fillColor': 'yellow'}))

# We mark various population centres around the country

data2 = pandas.read_csv("US Population Centres.csv")
lat2 = list(data2['lat'])
lon2 = list(data2['lng'])
population = list(data2['population'])
name2 = list(data2['city'])
fg_populationCentres = folium.FeatureGroup(name="Population Centres(US)")
for i in range(0, len(lat2), 1):
    fg_populationCentres.add_child(folium.CircleMarker(location=(lat2[i], lon2[i]), radius=1,
                                                       popup=name2[i]+"\n"+displayPopulation(population[i]),
                                                       fill_color=city_color(population[i]), fill_opacity=0.5,
                                                       fill=True,
                                                       color=city_color(population[i])))


map1.add_child(fg_stores)
map1.add_child(fg_stateLines)
map1.add_child(fg_populationCentres)


map1.add_child(folium.LayerControl())
map1.save("Whole Foods USA.html")
