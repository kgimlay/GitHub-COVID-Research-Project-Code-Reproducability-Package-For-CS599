import pandas as pd
import requests
from pandas import *
import json
from datetime import datetime
import time


def mineRepoContributors(access_token, repo_owner, repo_name):
    # authentification helper function
    def token_auth(request):
        request.headers["User-Agent"] = "CS599" # Required
        request.headers["Authorization"] = "token {}".format(access_token)
        return request

    # get the contributors to the repo
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
    response = requests.get("https://api.github.com/repos/{owner}/{repo}/contributors?page=1&per_page=100".format(owner=repo_owner, repo=repo_name, page=0), auth=token_auth)
    response_json = response.json()
    if 'message' in response_json:
            print(response_json['message'])
            exit(1)
    if len(response_json) == 0:
        print('Failed to get contributors. No csv file produced')
        return
    # export to csv
    data_frame = pd.DataFrame.from_dict(response_json)
    data_frame.to_csv('contributors.csv', index=False)

    page_num = 2
    while True:  # loop until end of contributors list
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
        response = requests.get("https://api.github.com/repos/{owner}/{repo}/contributors?per_page=100&page={page}".format(owner=repo_owner, repo=repo_name, page=page_num), auth=token_auth)
        response_json = response.json()
        if 'message' in response_json:
            print(response_json['message'])
            exit(1)
        if len(response_json) == 0:
            break
        # export to csv as progresses
        # this will save progress if program needs to be terminated
        data_frame = pd.DataFrame.from_dict(response_json)
        data_frame.to_csv('contributors.csv', mode='a', header=False, index=False)
        page_num = page_num + 1

    return;


def mineRepoCommits(access_token, repo_owner, repo_name, start_year, end_year):
    # authentification helper function
    def token_auth(request):
        request.headers["User-Agent"] = "CS599" # Required
        request.headers["Authorization"] = "token {}".format(access_token)
        return request
    try:
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
        response = requests.get("https://api.github.com/repos/{owner}/{repo}/commits?since={start}&until={end}&page=1&per_page=100".format(owner=repo_owner, repo=repo_name, page=0, start=start_year, end=end_year), auth=token_auth)
        response_json = response.json()
        if 'message' in response_json:
            print(response_json['message'])
            exit(1)
        if len(response_json) == 0:
            print('Failed to get commits. No csv file produced')
            return
        # export to csv

        sha = response_json[0]['sha']

        col=[['Sha'],[sha]]
        df = pd.DataFrame(col)
        df.to_csv('commits.csv',header=False,index=False)

        page_num = 2
        while True:  # loop until end of contributors list
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

            response = requests.get("https://api.github.com/repos/{owner}/{repo}/commits?since={start}&until={end}&page={page}&per_page=100".format(owner=repo_owner, repo=repo_name, page=page_num, start=start_year, end=end_year), auth=token_auth)
            response_json = response.json()
            if 'message' in response_json:
                print(response_json['message'])
                exit(1)
            if len(response_json) == 0:
                break
            # export to csv as progresses
            # this will save progress if program needs to be terminated
            for x in response_json:
                col = [[x['sha']]]
                data_frame = pd.DataFrame.from_dict(col)
                data_frame.to_csv('commits.csv', mode='a', header=False, index=False)

            page_num = page_num + 1

    except:
        print(response_json)


def getPullRequest(access_token,repo,owner):
    # authentification helper function
    def token_auth(request):
        request.headers["User-Agent"] = "CS599" # Required
        request.headers["Authorization"] = "token {}".format(access_token)
        return request

    data = read_csv("commits.csv")
    if len(data) == 0:
        print('No commit CSV found')
        return
    sha_val = data['Sha'].to_list()
    sha_val = set(sha_val)
    col=[['User','Number','Comments','URL','SHA']]
    df = pd.DataFrame(col)
    df.to_csv('pulls.csv',header=False, index=False)

    for sha in sha_val:
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
        response = requests.get("https://api.github.com/repos/{owner}/{repo}/commits/{sha}/pulls".format(sha=sha,repo=repo,owner=owner), auth=token_auth)
        response_json = response.json()
        if 'message' in response_json:
            print(response_json['message'])
            exit(1)
        if len(response_json) == 0 or response_json[0]['id'] == None:
            continue

        user = response_json[0]['user']['login']
        number = response_json[0]['number']
        url = response_json[0]['url']
        comments_url = response_json[0]['comments_url']
        if(comments_url != None):
            comments = getComments(comments_url,access_token)


        dict = [[user,number,comments,url,sha]]

        df = pd.DataFrame(dict)
        df.to_csv('pulls.csv', mode='a', header=False, index=False)

def getComments(url,access_token):
    def token_auth(request):
        request.headers["User-Agent"] = "CS599" # Required
        request.headers["Authorization"] = "token {}".format(access_token)
        return request
    comments_str = ""

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
    response = requests.get((url), auth=token_auth)
    response_json = response.json()
    if 'message' in response_json:
            print(response_json['message'])
            exit(1)
    if len(response_json) == 0:
        return comments_str

    for comment in response_json:
        if 'message' in response_json:
            print(response_json['message'])
            exit(1)
        if len(comment)  == 0:
            continue
        if(comment['body'] != None):
            comments_str = comments_str + " " + comment['body']

    comments_str = comments_str.lower();

    return comments_str

def getForks(access_token, repo_owner, repo_name, start_year, end_year):
    # authentification helper function
    def token_auth(request):
        request.headers["User-Agent"] = "CS599" # Required
        request.headers["Authorization"] = "token {}".format(access_token)
        return request

    # get the forks of the repo
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
    response = requests.get("https://api.github.com/repos/{owner}/{repo}/forks?page={page}&per_pageinteger=100&sort=newest".format(owner=repo_owner, repo=repo_name, page=0), auth=token_auth)
    response_json = response.json()
    if 'message' in response_json:
            print(response_json['message'])
            print('Error getting forks. No csv file produced')
            return
    if len(response_json) == 0:
        print('Failed to get forks. No csv file produced')
        return
    if datetime.strptime(response_json[0]['created_at'], '%Y-%m-%dT%H:%M:%SZ') < datetime.strptime(start_year, '%Y-%m-%dT%H:%M:%SZ'):
        print('No forks after ' + start_year)
        return

    # export to csv
    data_frame = pd.DataFrame.from_dict(response_json)
    data_frame['created_at'] = to_datetime(data_frame['created_at'], format='%Y-%m-%dT%H:%M:%SZ')
    data_frame = data_frame[data_frame['created_at'] >= datetime.strptime(start_year, '%Y-%m-%dT%H:%M:%SZ')]
    data_frame = data_frame[data_frame['created_at'] <= datetime.strptime(end_year, '%Y-%m-%dT%H:%M:%SZ')]
    data_frame = data_frame[['full_name','created_at']]
    data_frame.to_csv('forks.csv', index=False)

    page_num = 1
    while True:  # loop until end of forks list
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
        response = requests.get("https://api.github.com/repos/{owner}/{repo}/forks?page={page}&per_pageinteger=100&sort=newest".format(owner=repo_owner, repo=repo_name, page=page_num), auth=token_auth)
        response_json = response.json()
        if 'message' in response_json:
                print(response_json['message'])
                print('Error getting forks. No csv file produced')
                return
        if len(response_json) == 0:
            break
        if datetime.strptime(response_json[0]['created_at'], '%Y-%m-%dT%H:%M:%SZ') < datetime.strptime(start_year, '%Y-%m-%dT%H:%M:%SZ'):
            break

        # export to csv as progresses
        # this will save progress if program needs to be terminated
        data_frame = pd.DataFrame.from_dict(response_json)
        data_frame['created_at'] = to_datetime(data_frame['created_at'], format='%Y-%m-%dT%H:%M:%SZ')
        data_frame = data_frame[data_frame['created_at'] >= datetime.strptime(start_year, '%Y-%m-%dT%H:%M:%SZ')]
        data_frame = data_frame[data_frame['created_at'] <= datetime.strptime(end_year, '%Y-%m-%dT%H:%M:%SZ')]
        data_frame = data_frame[['full_name','created_at']]
        data_frame.to_csv('forks.csv', mode='a', header=False, index=False)
        page_num = page_num + 1
