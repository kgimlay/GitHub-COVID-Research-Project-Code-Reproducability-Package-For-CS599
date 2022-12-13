#All our Analysis will be in this file

import pandas as pd
import requests
from pandas import *
import re
from dateutil import parser
import csv

def getNoviceContributors(access_token):
    # authentification helper function
    def token_auth(request):
        request.headers['User-Agent'] = 'CS599' # Required
        request.headers['Authorization'] = 'token {}'.format(access_token)
        return request
    data = read_csv('contributors.csv')
    if len(data) == 0:
        print('No commit CSV found')
        return

    user_val = data['login'].to_list()

    col=[['User','Novice']]
    df = pd.DataFrame(col)
    df.to_csv('Question1.csv',header=False,index=False)

    covidDate = parser.parse('2020-03-27T00:00:00Z')
    for user in user_val:
        api_limit = requests.get("https://api.github.com/rate_limit", auth=token_auth).json()['rate']
        api_remaining = api_limit['remaining']
        api_reset = api_limit['reset']
        print(api_remaining)
        if (int(api_remaining) <= 0):
            print('Waiting for API limit to reset...')
            while True:
                # print(datetime.now())
                # print(datetime.fromtimestamp(int(api_reset)))
                time.sleep(60)
                if (datetime.now() > datetime.fromtimestamp(int(api_reset))):
                    break
        repos = requests.get('https://api.github.com/users/{username}/repos?per_page=100'.format(username = user), auth=token_auth)
        repos_json = repos.json()

        if len(repos_json) == 0:
            print('Failed to get user',user)
            continue


        novice = True
        dateCreated = False

        for repos in repos_json:
            if(repos['created_at'] != None):
                created = parser.parse(repos['created_at'])
                if(created < covidDate):
                    dateCreated = True

            if(repos['license'] != None):
                if(repos['license']['key'] == 'mit'):
                        if(dateCreated):
                            novice = False
                        break

        dict = [[user,novice]]

        df = pd.DataFrame(dict)
        df.to_csv('Question1.csv', mode='a', header=False, index=False)


def getFirstTimeUsers(access_token):
    # authentication helper function
    def token_auth(request):
        request.headers['User-Agent'] = 'CS599' # Required
        request.headers['Authorization'] = 'token {}'.format(access_token)
        return request
    data = read_csv('contributor_start_date.csv')
    if len(data) == 0:
        print('No commit CSV found')
        return

    col=[['User','NewGithubUser']]
    df = pd.DataFrame(col)
    df.to_csv('Question2.csv',header=False,index=False)

    user_val = data['login'].to_list()
    covidDate = parser.parse('2020-03-27T00:00:00Z')

    for user in user_val:
        api_limit = requests.get("https://api.github.com/rate_limit", auth=token_auth).json()['rate']
        api_remaining = api_limit['remaining']
        api_reset = api_limit['reset']
        print(api_remaining)
        if (int(api_remaining) <= 0):
            print('Waiting for API limit to reset...')
            while True:
                # print(datetime.now())
                # print(datetime.fromtimestamp(int(api_reset)))
                time.sleep(60)
                if (datetime.now() > datetime.fromtimestamp(int(api_reset))):
                    break
        user_info = requests.get('https://api.github.com/users/{username}'.format(username = user), auth=token_auth)
        user_info_json = user_info.json()
        if 'message' in user_info:
            print(user_info['message'])
            exit(1)
        if len(user_info_json) == 0:
            print('Failed to get user',user)
            continue

        if(user_info_json['created_at'] != None):
            created = parser.parse(user_info_json['created_at'])
            if(created < covidDate):
                previous =False
            else:
                previous=True

            dict = [[user,previous]]
            df = pd.DataFrame(dict)
            df.to_csv('Question2.csv', mode='a', header=False, index=False)



def getCommentsCount(access_token,startyear,endyear) :
     # authentification helper function
    def token_auth(request):
        request.headers['User-Agent'] = 'CS599' # Required
        request.headers['Authorization'] = 'token {}'.format(access_token)
        return request

    data = read_csv('pulls.csv')
    if len(data) == 0:
        print('No commit CSV found')
        return


    NegativeCount = {'error' : 0,
    'errors' : 0,
    'bug' : 0,
    'buggy' : 0,
    'warnings' : 0,
    'incorrect' : 0,
    'wrong' : 0,
    'ineffective' : 0,
    'failing' : 0,
    'failed' : 0,
    'bad' : 0,
    'horrible' : 0,
    'slow' : 0,
    'broken' : 0,
    'breaks' : 0
    }

    PositiveCount = {'good' : 0,
    'great' : 0,
    'excellent' : 0,
    'works' : 0,
    'fast' : 0,
    'fixed' : 0,
    'fixs' : 0,
    'excellent' : 0,
    'impressive' : 0,
    'brilliant' : 0,
    'fantastic' : 0,
    'nice' : 0,
    'resolved' : 0,
    'awesome': 0
    }

    comments = data['Comments'].astype(str).to_list()

    for comment in comments:
        if len(comment) > 1:
            comment = re.sub(r'\W+', ' ',comment)
            for word in PositiveCount:
                PositiveCount[word] = PositiveCount[word] + comment.count(word)
            for word in NegativeCount:
                NegativeCount[word] = NegativeCount[word] + comment.count(word)

    with open('Question3.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in PositiveCount.items():
            writer.writerow([key, value,startyear,endyear, 'P'])
        for key, value in NegativeCount.items():
            writer.writerow([key, value,startyear,endyear,'N'])
