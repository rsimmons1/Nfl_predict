from sklearn import svm
import matplotlib.pyplot as plt
import numpy as np
from pymongo import MongoClient
from team import *

client = MongoClient('localhost', 27017)

db = client['nfl_stats']

data_set = db['dataset']

if __name__ == '__main__':
    sizes = []
    x_data = {}
    y_data = {}
    x_data['win'] = []
    x_data['loss'] = []
    y_data['win'] = []
    y_data['loss'] = []
    input_data = []
    result = []
    start_year = 2009
    end_year = 2015 + 1

    for cur_year in range(start_year,end_year):
        team = 'cin'
        year = str(cur_year)
        this_season = Season(team,year,data_set.find_one({'team':team,'year':year}))
        stat1 = 'ORushY'
        stat2 = 'OPassY'



        for week in this_season.reg_season():
            cur_week = this_season.get_week(week)
            print '{} {} {}'.format(year,week,bool(cur_week))
            if(bool(cur_week)):
                if(cur_week['Win_loss'] == 'W'):
                    x_data['win'].append(cur_week[stat1])
                    y_data['win'].append(cur_week[stat2])
                    result.append(1)
                else:
                    x_data['loss'].append(cur_week[stat1])
                    y_data['loss'].append(cur_week[stat2])
                    result.append(0)
                print '{} {}'.format(cur_week[stat1], cur_week[stat2])
                input_data.append([cur_week[stat1], cur_week[stat2]])
                sizes.append(200)
        wins = plt.scatter(x_data['win'],y_data['win'],c='red',s=sizes)
        losses = plt.scatter(x_data['loss'],y_data['loss'],c='blue',s=sizes)


    C = 1.0
    input_data = np.array(input_data)
    result = np.array(result)
    clf = svm.SVC(kernel = 'linear',  gamma=0.7, C=C )
    clf.fit(input_data,result)

    w = clf.coef_[0]
    a = -w[0] / w[1]
    xx = np.linspace(0, 200)
    yy = a * xx - (clf.intercept_[0]) / w[1]

    plt.plot(xx, yy, 'k-')

    plt.xlabel(stat1)
    plt.ylabel(stat2)
    plt.title( '{} {}-{}'.format(team.upper(),start_year,end_year-1) )
    plt.ylim(ymin=0,ymax=500)
    plt.xlim(xmin=0,xmax=400)
    plt.show()
