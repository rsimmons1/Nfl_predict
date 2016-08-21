from __future__ import division
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
    start_year = 2005
    end_year = 2015 + 1
    data_scale = 1/100
    team_acr = ["crd", "atl", "rav", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gnb", "htx", "clt", "jax", "kan", "mia", "min", "nwe", "nor", "nyg", "nyj", "rai", "phi", "pit", "sdg", "sfo", "sea", "ram", "tam", "oti", "was"]
    for cur_year in range(start_year,end_year):
        team = 'den'
        year = str(cur_year)

        stat1 = 'OPassY'
        stat2 = 'Tm_score'


        for team in ['den']:
            this_season = Season(team,year,data_set.find_one({'team':team,'year':year}))
            for week in this_season.reg_season():
                cur_week = this_season.get_week(week)
                # print '{} {} {}'.format(year,week,bool(cur_week))
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
                    input_data.append([cur_week[stat1]*data_scale, cur_week[stat2]*data_scale])
                    sizes.append(200)
        # wins = plt.scatter(x_data['win'],y_data['win'],c='red',s=sizes)
        # losses = plt.scatter(x_data['loss'],y_data['loss'],c='blue',s=sizes)






    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    import itertools
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import SVC
    from sklearn.ensemble import RandomForestClassifier
    from mlxtend.classifier import EnsembleVoteClassifier
    from mlxtend.data import iris_data
    from mlxtend.evaluate import plot_decision_regions

    # Initializing Classifiers
    clf1 = LogisticRegression(random_state=0)
    clf2 = RandomForestClassifier(random_state=0)
    clf3 = SVC(random_state=0, probability=True)
    eclf = EnsembleVoteClassifier(clfs=[clf1, clf2, clf3], weights=[2, 1, 1], voting='soft')

    # Loading some example data
    X = np.array(input_data)
    y = np.array(result)
    # X = np.array(input_data)
    # y = np.array(result)

    # Plotting Decision Regions
    # gs = gridspec.GridSpec(1)
    fig = plt.figure(figsize=(10, 8))
    lab = 'RBF kernel SVM'
    clf = clf3
    clf.fit(X, y)
    ax = plt.subplot(1,1,1)
    fig = plot_decision_regions(X=X, y=y, clf=clf, legend=2)
    plt.title( '{} {}-{}'.format(team.upper(),start_year,end_year-1) )
    plt.xlabel(stat1)
    plt.ylabel(stat2)
    plt.ylim(ymin=0)
    plt.xlim(xmin=0)
    plt.show()
