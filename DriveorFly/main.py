from bs4 import BeautifulSoup
import requests
import webbrowser
import time
import googlemaps
from math import radians, cos, sin, asin, sqrt

source = requests.get("https://www.gasbuddy.com/USA").text
soup = BeautifulSoup(source, 'lxml')

body = soup.find_all("div", {"class": "col-sm-2 col-xs-3 text-right"})
list1 = []
for item in body:
    num = float(item.text)
    list1.append(num)
avg_gp = round(sum(list1) / len(list1),2)
# print(avg_gp)

gmaps = googlemaps.Client(key='AIzaSyBx0PL5f3BC-eQ3BIl4lCMmRPHU-ykGAEg')

start = input('Starting location: ')
end = input('Final Destination: ')

my_dist = googlemaps.client.distance_matrix(gmaps, start, end)['rows'][0]['elements'][0]

total_km = (my_dist['distance']['value']) / 1000
total_miles = total_km / 1.609344


year = input("Enter year of car: ")
brand = input("Enter brand of car: ")
model = input("Enter model of car: ")
source = requests.get("https://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&path=1&year1="
                      +year+"&year2="+year+"&make="+brand+"&baseModel="+model+"&srchtyp=ymm&pageno=1&sortBy=Comb&tabView=0&rowLimit=10").text
soup = BeautifulSoup(source, 'lxml')
body = soup.find_all("td", {"class": "mpg-comb"})
list1 = []
for item in body:
    num = float(item.text)
    list1.append(num)
avg_mpg = sum(list1) / len(list1)
# print(avg_mpg)


dep_dat = input("Enter the day you wish to leave in MM/DD/YYYY form: ")
rt = input('Roundtrip (Y/N)? ')

if rt == 'Y':
    ret_dat = input("Enter possible return date in MM/DD/YYYY form: ")
    url = 'https://vacation.hotwire.com/Flights-Search?trip=roundtrip&leg1=from%3A'+start+'%2Cto%3A'+end+'%2Cdeparture%3A'+dep_dat[0:2]+'%2F'+dep_dat[3:5]+'%2F'+dep_dat[6:10]+'TANYT&leg2=from%3A'+end+'%2Cto%3A'+start+'%2Cdeparture%3A'+ret_dat[0:2]+'%2F'+ret_dat[3:5]+'%2F'+dep_dat[6:10]+'TANYT&passengers=adults%3A1%2Cchildren%3A0%2Cseniors%3A0%2Cinfantinlap%3AY&mode=search'
else:
    url = 'https://vacation.hotwire.com/Flights-Search?trip=oneway&leg1=from%3A'+start+'%2Cto%3A'+end+'%2Cdeparture%3A'+dep_dat[0:2]+'%2F'+dep_dat[3:5]+'%2F'+dep_dat[6:10]+'TANYT&passengers=adults%3A1%2Cchildren%3A0%2Cseniors%3A0%2Cinfantinlap%3AY&options=cabinclass%3Aeconomy&mode=search&origref=vacation.hotwire.com'

webbrowser.open_new_tab(url)

time.sleep(18)
source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')
# body = soup.find("div",{"class": "justify-right item-price"})
body = soup.find_all("div", {"class": "justify-right item-price"})

# print(soup.prettify())
# price = body.text


def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))


list1 = []
for item in body:
    num = (item.text)
    list1.append(get_num(num))
m = min(list1)
m_str = str(min(list1))

st_loc = googlemaps.client.geocode(gmaps, start)
end_loc = googlemaps.client.geocode(gmaps, end)

def haversine(lon1, lat1, lon2, lat2):
    '''
    calculate the great circle distance between two points
    on the Earth (coordinates specified in decimal degrees)
    '''
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    miles = 3961 * c
    return miles

city1 = start
lat1  = st_loc[0]['geometry']['bounds']['northeast']['lat']
lon1 = st_loc[0]['geometry']['bounds']['northeast']['lng']

city2 = end
lat2  = end_loc[0]['geometry']['bounds']['northeast']['lat']
lon2 = end_loc[0]['geometry']['bounds']['northeast']['lng']

miles = haversine(lon1, lat1, lon2, lat2)
tt = 30
if rt == 'Y':
    miles *= 2
    tt *= 2
time_h = round((miles / (575 / 60) + tt) // 60)
time_m = round((miles / (575 / 60) + tt) % 60)


print('-------------------------------------------------')
print('Drive Distance:',str(round(total_miles,2)),'miles')
if rt == 'Y':
    total_miles *= 2
    my_dist['duration']['value'] *= 2
    new_time_d = my_dist['duration']['value'] // 86400
    new_time_h = (my_dist['duration']['value'] % 86400) // 3600
    new_time_m = ((my_dist['duration']['value'] % 86400) % 3600) // 60
    if new_time_d > 0:
        print('Drive Time:',new_time_d, 'days', new_time_h, 'hours')
    else:
        print ('Drive Time: ',new_time_h, 'hours',new_time_m,'mins')
else:
    print('Drive Time:', my_dist['duration']['text'])


drive_cost = total_miles*(avg_gp/avg_mpg)
drive_cost_srt = str(round(total_miles*(avg_gp/avg_mpg),2))

print('Flight time:',time_h,'hours',time_m, 'min')
print('Total Gas Price: $' + drive_cost_srt)
print('Flight Price: $' + m_str)

print('-------------------------------------------------')
if drive_cost > m and my_dist['duration']['value'] > (time_h*3600+time_m*60):
    print("It is cheaper and shorter to fly")
elif drive_cost > m and my_dist['duration']['value'] < (time_h*3600+time_m*60):
    print("It is cheaper to fly, but shorter to drive")
elif drive_cost < m and my_dist['duration']['value'] > (time_h*3600+time_m*60):
    print("It is cheaper, but also longer to drive")
else:
    print("It is cheaper and shorter to drive")