from sklearn import svm
import matplotlib.pyplot as plt
import numpy as np
from pymongo import MongoClient
from team import *
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from mlxtend.evaluate import plot_decision_regions
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import time
client = MongoClient('localhost', 27017)

db = client['nfl_stats']

data_set = db['dataset']

def b2l(win_loss):
    if win_loss == 1:
        return 'W'
    return 'L'

def l2b(win_loss):
    if win_loss == 'W':
        return 1
    return 0

def data_scale(data,scale=0.01):
    return data*scale

def data_unscale(data,scale):
    return data/scale

def team_season_outcome(team_names,years):
    x_data = []
    y_data = []
    matches = []
    length = len(years)*len(team_names)*len(range(1,18))
    count = 0
    for year in years:
        for team_name in team_names:
            year = str(year)
            team = get_team(data_set,team_name,year)
            for week in range(1,18):
                count += 1.0
                if(bool(team.get_week(week+1))):
                    # print count/length
                    prev_week = []
                    opp_name = convert_acr[team.get_week(week+1)['Opp']]
                    opp_team = get_team(data_set,opp_name,year)
                    stat = ['Tm_score']
                    switch = True
                    matches.append([team_name,opp_name,year,str(week)])
                    for item in team.cur_stats(week):
                        if item in stat or switch:
                            prev_week.append(team.cur_stats(week)[item])
                    for item in opp_team.cur_stats(week):
                        if item in stat or switch:
                            prev_week.append(opp_team.cur_stats(week)[item])

                    x_data.append(prev_week)
                    y_data.append(l2b(team.get_week(week+1)['Win_loss']))
    return (np.asarray(x_data),np.asarray(y_data),np.asarray(matches))


if __name__ == '__main__':
    sizes = []
    X_train = []
    y_train = []
    input_data = []
    result = []
    start_year = 2012
    end_year = 2014 + 1



    X_train,y_train,matches = team_season_outcome(team_acr,range(start_year,end_year))
    X_train = StandardScaler().fit_transform(X_train)
    X_test,y_test,matches = team_season_outcome(team_acr,[2015])
    X_test = StandardScaler().fit_transform(X_test)
    # np.random.seed(1)
    # np.random.shuffle(X_train)
    # np.random.seed(1)
    # np.random.shuffle(y_train)
    # np.random.seed(1)
    # np.random.shuffle(X_test)
    # np.random.seed(1)
    # np.random.shuffle(y_test)
    # np.random.seed(1)
    # np.random.shuffle(matches)


    print "Building Perceptron..."
    clf = MLPClassifier(alpha=0.0001, random_state=0)
    clf3 = LogisticRegression(random_state=0)
    clf4 = SVC(C=0.001, tol=1e-10, cache_size=600, kernel='rbf', gamma=(1.0/22.0),
              class_weight='balanced')
    clf2 = SVC(kernel='rbf', degree=2, C=1.0)
    clf1 = RandomForestClassifier(random_state=0)

    print "Fitting data..."
    clf.fit(data_scale(X_train), y_train)

    print "Testing results..."
    total_tests = len(X_test)
    correct = 0
    for i in range(len(X_test)):
        input_game = X_test[i]
        result = y_test[i]
        predict_result = clf.predict(data_scale(input_game.reshape(1,-1)))[0]
        print clf.predict_proba(data_scale(input_game.reshape(1,-1)))
        real_label = b2l(result)
        predict_label = b2l(predict_result)
        print matches[i]
        if real_label == predict_label:
            print "Correct!"
            correct+=1
        else:
            print "Incorrect!"

        print "Predicted: " + predict_label
        print "Actual: " + real_label
        print "===================="

    print "Test Results"
    print correct
    print 100*(float(correct)/float(len(X_test)))
    # fig = plot_decision_regions(X=X_train, y=y_train, clf=clf, legend=2)
    # plt.show()
