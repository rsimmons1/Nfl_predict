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

def clf_data(team_names,years):
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
                    stat = ['Wins']
                    switch = True
                    matches.append([convert_acr[team_name],convert_acr[opp_name],year,str(week)])
                    for item in team.cur_stats(week):
                        if item in stat or switch:
                            prev_week.append(team.cur_stats(week)[item])
                    for item in opp_team.cur_stats(week):
                        if item in stat or switch:
                            prev_week.append(opp_team.cur_stats(week)[item])

                    x_data.append(prev_week)
                    y_data.append(l2b(team.get_week(week+1)['Win_loss']))
    return (np.asarray(x_data),np.asarray(y_data),np.asarray(matches))

def guess_match_clf(data_set,clf,week_info):
    week = int(week_info[3])
    team = get_team(data_set, week_info[0], week_info[2])
    opp = get_team(data_set, week_info[1], week_info[2])
    prev_week = []
    for item in team.cur_stats(week):
        prev_week.append(team.cur_stats(week)[item])
    for item in opp.cur_stats(week):
        prev_week.append(opp.cur_stats(week)[item])
    prev_week = np.asarray(prev_week)
    prev_week = StandardScaler().fit_transform(prev_week)
    print week_info
    print clf.predict_proba(data_scale(prev_week.reshape(1,-1)).reshape(1,-1) )
    print



X_train = []
y_train = []
result = []
start_year = 2011
end_year = 2014 + 1



X_train,y_train,matches = clf_data(team_acr,range(start_year,end_year))
X_train = StandardScaler().fit_transform(X_train)
X_test,y_test,matches = clf_data(team_acr,[2015])
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
clf = MLPClassifier(algorithm='l-bfgs',alpha=0.000001, random_state=0,hidden_layer_sizes=(22,4))
clf2 = LogisticRegression(random_state=0)
clf3 = SVC(C=0.001, tol=1e-10, cache_size=600, kernel='rbf', gamma=(1.0/22.0),
          class_weight='balanced')
clf1 = RandomForestClassifier(random_state=0)

print "Fitting data..."
clf.fit(data_scale(X_train), y_train)

if __name__ == '__main__':
    print "Testing results..."
    total_tests = len(X_test)
    correct = 0
    correct2 = 0
    for i in range(len(X_test)):
        input_game = X_test[i]
        result = y_test[i]
        week = int(matches[i][3])
        tm1 = get_team(data_set,convert_acr[matches[i][0]],matches[i][2])
        tm2 = get_team(data_set,convert_acr[matches[i][1]],matches[i][2])
        tm1_wins = tm1.cur_stats(week)['Wins']
        tm2_wins = tm2.cur_stats(week)['Wins']
        if bool(tm1.get_week(week)) == True:
            at = bool(tm1.get_week(week)['At'])
        else:
            at = False
        print tm1.cur_stats(week)
        print tm2.cur_stats(week)
        if(tm1_wins > tm2_wins and result == 1):
            correct2 += 1
        elif(tm2_wins > tm1_wins and result == 0):
            correct2 += 1
        elif(tm2_wins == tm1_wins and result == 1 and at == True):
            correct2 += 1
        elif(tm2_wins == tm1_wins and result == 0 and at == False):
            correct2 += 1
        predict_result = clf.predict(data_scale(input_game.reshape(1,-1)))[0]
        real_label = b2l(result)
        predict_label = b2l(predict_result)

        # print clf.predict_proba(data_scale(input_game.reshape(1,-1)))
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
    print "MLP Model Accuracy: {}".format(100*(float(correct)/float(len(X_test))))
    print "Win/Loss Model Accuracy: {}".format(100*(float(correct2)/float(len(X_test))))
    # fig = plot_decision_regions(X=X_train, y=y_train, clf=clf, legend=2)
    # plt.show()
