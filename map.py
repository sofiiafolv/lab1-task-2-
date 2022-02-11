import pandas
import folium
import argparse
import haversine
import csv
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
geolocator = Nominatim(user_agent="map.py")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
from geopy.exc import GeocoderUnavailable

parser=argparse.ArgumentParser()
parser.add_argument("year",type=str,help="A year in which films were filmed")
parser.add_argument("latitude",type=float,help="A latitude of the place where film was filmed")
parser.add_argument("longtitude",type=float,help="A longtitude of the place where film was filmed")
parser.add_argument("path_to_dataset",type=str,help="A path to a file where is an information about films")

args = parser.parse_args()
year = args.year
latitude=args.latitude
longtitude=args.longtitude
path_to_dataset=args.path_to_dataset

def flatten(lst):
    """Return a single list of elements
    >>> flatten([1,2,[3,[4,5],6],7])
    [1, 2, 3, 4, 5, 6, 7]
    """
    if type(lst)!=list:
        return lst
    if lst==[]:
        return lst
    if type(lst[0])==list:
        return(flatten(lst[0])+flatten(lst[1:]))
    return lst[:1]+flatten(lst[1:])

def parser_list(path, year_of_films):
    """Turn a file into list for better data storage
    """
    with open(path, mode='r') as file:
        data=file.readlines()
    data=data[14:-1]
    list_of_films=[]
    for i in data:
        if year_of_films in i:
           list_of_films.append(i.split("(",1)) 
    for i in range(len(list_of_films)):
        list_of_films[i][0] = list_of_films[i][0].rstrip(' ')
        list_of_films[i][-1] = list_of_films[i][-1].rstrip('\n')
        list_of_films[i][1] = list_of_films[i][-1].rsplit('\t',1)
        if list_of_films[i][1][1].startswith('('):
            del list_of_films[i][1][1]
            list_of_films[i][1][0]=list_of_films[i][1][0].rsplit('\t',1)
        list_of_films[i]=flatten(list_of_films[i])
        list_of_films[i][1]=list_of_films[i][1].split(')',1)
        if list_of_films[i][1][1].startswith("\t"):
            list_of_films[i][1][1] = "NODATA"
        else:
            list_of_films[i][1][1]=list_of_films[i][1][1].strip("\t")
        list_of_films[i]=flatten(list_of_films[i])
    return list_of_films

def turn_into_dict(list_of_films):
    """Returns a dict where a key is a place
    >>> turn_into_dict([['"#1 Single"', '2006', 'NODATA', 'Los Angeles, California, USA']])
    {'Los Angeles, California, USA': [['"#1 Single"', '2006', 'NODATA', 'Los Angeles, California, USA']]}
    """
    dict_of_films={}
    for item in list_of_films:
        if item[-1] in dict_of_films:
            dict_of_films[item[-1]].append(item[:])
        else: 
            dict_of_films[item[-1]]=[item[:]]
    return dict_of_films
    
    
def adding_coordinates(dict_of_films):
    """Returns a dict + coordinates
    >>> adding_coordinates({'Los Angeles, California, USA': [['"#1 Single"', '2006', \
    'NODATA', 'Los Angeles, California, USA']]})
    {'Los Angeles, California, USA': [['"#1 Single"', '2006', 'NODATA', 'Los Angeles, California, USA', (34.0536909, -118.242766)]]}
    """
    try:
        for key in dict_of_films:
            location=geolocator.geocode(key)
            
            if hasattr(location,'latitude') and (location.latitude is not None):
                for i in dict_of_films.get(key):
                    i.append((location.latitude,location.longitude))
        for key in dict_of_films:
            if len(dict_of_films.get(key)[0])!=5:
                address=key.split(',',1)[1]
                location=geolocator.geocode(address)
                for i in dict_of_films.get(key):
                    i.append((location.latitude,location.longitude))
    except GeocoderUnavailable as err:
        print(err)
    return dict_of_films

def adding_length_of_way(dict_of_films,coordinates):
    """Return list sorted by length_of_way from a place,
    where a movie was filmed to an initial location
    >>> adding_length_of_way({'Los Angeles, California, USA': [['"#1 Single"', '2006', 'NODATA', \
    'Los Angeles, California, USA', (34.0536909, -118.242766)]]}, (49.83826,24.02324))
    [['"#1 Single"', '2006', 'NODATA', 'Los Angeles, California, USA', (34.0536909, -118.242766)]]
    """
    
    for key in dict_of_films:
        dict_of_films.get(key).append(haversine.haversine(dict_of_films.get(key)[0][-1],coordinates))
    sorted_list=sorted(dict_of_films.values(), key = lambda x: x[-1])
    final_list=[]
    
    for i in sorted_list:
        final_list.append(i[:-1])
    
    final_list=flatten(final_list)
    final_list=[final_list[i:i + 5] for i in range(0, len(final_list), 5)]
    if len(final_list)>10:
        final_list=final_list[:10]
        for i in range(len(final_list)):
            final_list[i][-1]=list(final_list[i][-1])
            final_list[i]=flatten(final_list[i])
        return final_list
    else:
        for i in range(len(final_list)):
            final_list[i][-1]=list(final_list[i][-1])
            final_list[i]=flatten(final_list[i])
        return final_list

def write_csv(final_list_of_movies):
    """Write a csv file with necessary information
    """
    header=["Title","Year","Additional information","Location","Latitude","Longtitude"]
    

    with open('movies.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(final_list_of_movies)

list_of_films=parser_list(path_to_dataset,year)
write_csv(adding_length_of_way(adding_coordinates(turn_into_dict(list_of_films)),(latitude,longtitude)))
data = pandas.read_csv("movies.csv", error_bad_lines=False, encoding="utf-8")
lat=data["Latitude"]
lon=data["Longtitude"]
titles=data["Title"]
info=data["Additional information"]
location=data["Location"]
years=data["Year"]
map=folium.Map(location=[latitude,longtitude],zoom_start=10)
html="""<h4>Information about this movie:</h4>
Title: {},<br>
Year: {},<br>
Additional information: {},<br>
Location: {}
"""
fg=folium.FeatureGroup(name="World map")
for lt, ln, tit, ye, ad, loc  in zip(lat, lon, titles, years,info,location):
    iframe=folium.IFrame(html=html.format(tit,ye,ad,loc),
                        width=300,
                        height=100)
    fg.add_child(folium.Marker(location=[lt,ln],
                                popup=folium.Popup(iframe),
                                icon=folium.Icon(color="pink")))
fg_pp = folium.FeatureGroup(name="Population")
fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
    encoding='utf-8-sig').read(),
    style_function=lambda x: {'fillColor':
    'green' if x['properties']['POP2005'] < 10000000
    else 'red' if 10000000 <= x['properties']['POP2005'] < 20000000
    else 'orange'}))
map.add_child(fg_pp)
map.add_child(fg)
map.save('map.html')



