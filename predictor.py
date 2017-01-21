import numpy as np
from pymongo import MongoClient
from team import *
from analysis import *
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import time
from sklearn import linear_model
from sklearn.svm import SVR
from sklearn.kernel_ridge import KernelRidge
from sklearn.ensemble import ExtraTreesRegressor
client = MongoClient('localhost', 27017)

db = client['nfl_stats']

data_set = db['dataset']

def regr_data(team_names,years):
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
                    next_week = []
                    opp_name = convert_acr[team.get_week(week+1)['Opp']]
                    opp_team = get_team(data_set,opp_name,year)
                    stat = ['Tm_score']
                    stat2 = ['Tm_score','Opp_score']
                    switch = True
                    switch2 = True
                    matches.append([convert_acr[team_name],convert_acr[opp_name],year,str(week)])
                    for item in team.cur_stats(week):
                        if item in stat or switch:
                            prev_week.append(team.cur_stats(week)[item])
                    for item in opp_team.cur_stats(week):
                        if item in stat or switch:
                            prev_week.append(opp_team.cur_stats(week)[item])

                    x_data.append(prev_week)
                    for item in team.numeric_stats:
                        if item in stat2 or switch2:
                            next_week.append(team.get_week(week+1)[item])
                    y_data.append(next_week)
    return (np.asarray(x_data), np.asarray(y_data), np.asarray(matches))


def guess_match(data_set,week_info):
    week = int(week_info[3])
    team = get_team(data_set, week_info[0], week_info[2])
    opp = get_team(data_set, week_info[1], week_info[2])
    prev_week = []
    for item in team.cur_stats(week):
        prev_week.append(team.cur_stats(week)[item])
    for item in opp.cur_stats(week):
        prev_week.append(opp.cur_stats(week)[item])
    return np.asarray(prev_week)


if __name__ == '__main__':
    sizes = []
    X_train = []
    y_train = []
    input_data = []
    result = []
    start_year = 2012
    end_year = 2014 + 1

    X_train, y_train, matches = regr_data(team_acr,range(start_year,end_year))
    # X_train = StandardScaler().fit_transform(X_train)
    X_test, y_test, matches = regr_data(team_acr,[2015])
    # X_test = StandardScaler().fit_transform(X_test)
    team = Season('a','b',{})
    print "Building Perceptron..."
    clf = linear_model.LinearRegression()

    print "Fitting data..."
    clf.fit(X_train, y_train)

    print "Testing results..."
    total_tests = len(X_test)
    correct = 0
    for i in range(len(X_test)):
        input_game = X_test[i]
        result = y_test[i]
        # predict_result = clf.predict(data_scale(input_game.reshape(1,-1)))
        predict_result = clf.predict(input_game.reshape(1,-1))[0]
        print matches[i]
        print team.numeric_stats
        print map(lambda x: int(x),predict_result)
        print result

        pred1,pred2 = (predict_result[0],predict_result[1])
        res1,res2 = (result[0],result[1])
        if(pred1 > pred2 and res1 > res2):
            correct += 1
            print 'Correct'
        elif(pred2 > pred1 and res2 > res1):
            correct += 1
            print 'Correct'
        else:
            print 'Incorrect'
        print
    print clf.predict(guess_match(data_set,[convert_acr['Washington Redskins'],
                        convert_acr['Dallas Cowboys'], '2015', '16']))
    print "Test Results"
    print correct
    print 100*(float(correct)/float(len(X_test)))
    # fig = plot_decision_regions(X=X_train, y=y_train, clf=clf, legend=2)
    # plt.show()
print clf.score(X_train,y_train)
