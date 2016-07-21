import requests
from team import *
import time
import json
from multiprocessing import Pool

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['nfl_stats']

data_set = db['dataset']

start_year = 2002
end_year = 2015 + 1
team_acr = ["crd", "atl", "rav", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gnb", "htx", "clt", "jax", "kan", "mia", "min", "nwe", "nor", "nyg", "nyj", "rai", "phi", "pit", "sdg", "sfo", "sea", "ram", "tam", "oti", "was"]
seasons = {}

for name in team_acr:
    seasons[name] = {}

# urls = ["http://www.pro-football-reference.com/teams/{}/{}.htm".format(team,year) for team in team_acr[:1] for year in range(start_year,end_year)]
urls = {}

for i,team in enumerate(team_acr):
    urls[team] = []
    for year in range(start_year,end_year):
        if(bool(data_set.find_one({'team':team,'year':str(year)})) == False):
            print "{} {}".format(team,year)
            urls[team].append("http://www.pro-football-reference.com/teams/{}/{}.htm".format(team,year))
    if(bool(urls[team]) == False):
        del urls[team]
    else:
        print
# A simple task to do to each response object
def response_to_season(response,data_container):
    print response.url
    year = filter(lambda x: x.isdigit(),response.url)
    team = response.url.split('/')[4]
    data_container[team][year] = Season(team,year)
    data_container[team][year].parse_season(response)

def get_seasons(url_list,num):
    p = Pool(num)
    seasons = p.map(requests.get,url_list)
    return seasons

def timer(func,args):
     t1 = time.time()
     a = func(*args)
     t2 = time.time()
     print t2-t1
     return a

if __name__ == '__main__':
    for team in urls:
        season_data = timer(get_seasons,[urls[team],15]) #returns a list of responses
        for response in season_data:
            response_to_season(response,seasons)
        for season in seasons[team]:
            data = seasons[team][season]
            if(bool(data_set.find_one({'team':str(data.team),'year':str(data.year)})) == False):
                data_set.insert_one(data.json())
                print "Successfully Insert: {} {}".format(data.team,data.year)
        # response_to_season(season_data[1],seasons)
        time.sleep(5)
