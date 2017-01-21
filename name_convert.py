from team import *
from sample import *
strr = ''
team_names = []
acr_convert = []
team_acr = ["crd", "atl", "rav", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gnb", "htx", "clt", "jax", "kan", "mia", "min", "nwe", "nor", "nyg", "nyj", "rai", "phi", "pit", "sdg", "sfo", "sea", "ram", "tam", "oti", "was"]
def let_in_ord(acr,word):
    order = []
    for let in acr:
        if(let in word):
            order.append(word.index(let))
    if(len(order) == 3):
        return (order == sorted(order))
    else:
        return False

for team1 in data_set.find({'year':'2008'}):
    temp_season_1 = Season(team1['team'],team1['year'],team1)
    team_names.append(temp_season_1.get_week(1)['Opp'])

for team1 in data_set.find({'year':'2008'}):
    temp_season_1 = Season(team1['team'],team1['year'],team1)
    for team2 in data_set.find({'year':'2008'}):
        temp_season_2 = Season(team2['team'],team2['year'],team2)
        if(temp_season_1.team != temp_season_2.team):
            if(temp_season_1.get_week(1)['ORushY'] == temp_season_2.get_week(1)['DRushY'] and temp_season_1.get_week(1)['OPassY'] == temp_season_2.get_week(1)['DPassY']):
                print "{} {}".format(temp_season_1.team,temp_season_2.get_week(1)['Opp'])
                acr_convert.append({temp_season_2.get_week(1)['Opp']:temp_season_1.team})

print acr_convert
