from lxml import html
import time
import urllib2
from team_names import *

def get_team(data_set,team,year):
    team_data = data_set.find_one({'team':team,'year':year})
    return Season(team,year,team_data)

class Team():
    stat_table = ["Week","Day","Date","Link","Win_loss","OT","Rec","At","Opp","Tm_score","Opp_score","O1stD","OTotYd","OPassY","ORushY","OTO","D1stD","DTotYd","DPassY","DRushY","DTO","Offense","Defense","Sp Tms"]
    def __init__(self,name):
        self.name = name
        self.seasons = {}
        self.post_season = False
    def set_season(self,new_season):
        self.seasons[new_season.year] = new_season
    def get_season(self,year):
        return self.seasons[year]

class Season():

    def __init__(self,team,year,json_season=None,):
        self.stat_table = ["Week","Day","Date","Link","Win_loss","OT","Rec","At","Opp","Tm_score","Opp_score","O1stD","OTotYd","OPassY","ORushY","OTO","D1stD","DTotYd","DPassY","DRushY","DTO","Offense","Defense","Sp Tms"]
        self.numeric_stats = ["Tm_score","Opp_score","O1stD","OTotYd","OPassY","ORushY","D1stD","DTotYd","DPassY","DRushY"]
        self.year = year
        self.data = {}
        self.team = team
        if(bool(json_season)):
            self.set_json_season(json_season)

    def __iter__(self):
        iter_data = []
        for x in range(1,18):
            iter_data.append(x)
        iter_data.append('Division')
        iter_data.append('Conf Champ')
        iter_data.append('SuperBowl')
        return iter(iter_data)

    def cur_stats(self,week_num):
        """ calculates the teams stats up at that week """
        temp_season = {}
        weeks = 0
        for stat in self.numeric_stats:
            temp_season[stat] = 0
        for x in range(1,week_num+1):
            week = self.get_week(x)
            if(bool(week)):
                weeks = weeks + 1
                for stat in self.numeric_stats:
                    temp_season[stat] += float(week[stat])
        for stat in temp_season:
            temp_season[stat] = float(temp_season[stat])/float(weeks)

        return temp_season

    def reg_season(self):
        """ Iterator for just the regular season games """
        iter_data = []
        for x in range(1,18):
            iter_data.append(x)
        return iter(iter_data)

    def __repr__(self):
        return '{} {}'.format(self.team,self.year)

    def get_week(self,num):
        """ Returns data for given week """
        try:
            week = self.data['{}'.format(num)]
            return week
        except:
            return False

    def set_week(self,data):
        """ Sets data for given week """
        if(data['Week'] and data['Day']):
            week_name = str(data['Week'])
            self.data[week_name] = {}
            for key in data:
                if key != "Week":
                    try:
                        self.data[week_name][key] = float(data[key])
                    except:
                        self.data[week_name][key] = data[key]
                else:
                    try:
                        self.data[week_name][key] = data[key]
                    except:
                        self.data[week_name][key] = data[key]
        else:
            week_name = str(data['Week'])
            self.data[week_name] = False

    def set_season(self,new_season):
        """ Sets data from parsed web page """
        for item in new_season:
            self.set_week(item)

    def json(self):
        """ Returns a json representation of the data """
        season = {}
        season['team'] = self.team
        season['year'] = self.year
        for item in self.data:
            season[item] = self.data[item]
        return season

    def set_json_season(self,json_data):
        """ Uses json data to build the season """
        self.team = json_data['team']
        self.year = json_data['year']
        for item in json_data:
            if(not(item == 'team' or item == 'year' or item == '_id')):
                self.data[item] = json_data[item]

    def parse_season(self,page_info=None):
        """ Parses html into useable format """
        if(page_info == None):
            url = "http://www.pro-football-reference.com/teams/{}/{}.htm".format(self.team,self.year)

            t1 = time.time()
            response = urllib2.urlopen(url)
            t4 = time.time()
            page = html.fromstring(response.read())
            t2 = time.time()
            print "{}: Page Connection Time".format(t4-t1)
            print "{}: LXML Reading Time".format(t2-t4)
        else:
            t2 = time.time()
            page = html.fromstring(page_info.text)
        content = page.get_element_by_id(id="games")

        rows = content.cssselect("tr")
        del rows[0]
        weeks = []
        week_data = {}

        for row in rows:
            week_data = {}
            week_data[self.stat_table[0]] = row.cssselect('th')[0].text_content().replace('.','')
            for i,key in enumerate(row.cssselect('td')):
                if key.text_content() != "":
                    week_data[self.stat_table[i+1]] = key.text_content()
                else:
                    week_data[self.stat_table[i+1]] = ""
            weeks.append(week_data)
        t3 = time.time()
        self.set_season(weeks)
