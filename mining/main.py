# Data that needs to be collected:
# 1) For a given repository:
#   a) The pull requests from the start year through the end year
# 2)
# 3)

import sys
from datetime import datetime
import os
import requests

import repo_mining
import analysis

import pandas
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # read the github access token from file
    try:
        token_file = sys.argv[1]
    except:
        print("Error: no access token file specified!\n")
        exit(1)

    # read the repository to mine from
    try:
        repo_owner = sys.argv[2]
        repo_name = sys.argv[3]
    except:
        print("Error: repo name and owner not specified!\n")
        exit(1)


    # Import a text file containing the access token
    with open(token_file, 'r') as file:
        access_token = file.read().strip()

    startingtime = [
    "2019-01-01T00:00:00Z",
    "2020-03-28T00:00:00Z",
    "2021-05-02T00:00:00Z"]
    endingtime = [
    "2020-03-27T00:00:00Z",
    "2021-05-01T00:00:00Z",
    "2022-11-01T00:00:00Z"]

    #region Question 1 How many more people started supporting open-source projects?

    print('getting forks')
    repo_mining.getForks(access_token, repo_owner, repo_name, startingtime[0], endingtime[2])

    print('getting contributors')
    repo_mining.mineRepoContributors(access_token,repo_owner,repo_name) # note that this is used in answering question 2 as well, so change to call once

    print('analyzing start dates of contributors')
    forks_df = pandas.read_csv('forks.csv')
    contributors_df = pandas.read_csv('contributors.csv')
    contributors_df = contributors_df[['login']]
    forks_df['full_name'] = forks_df.apply(lambda name: name[0].split('/')[0], axis=1)
    forks_df = forks_df.rename(columns={'full_name':'login'})
    forks_df = forks_df.rename(columns={'created_at':'start_date'})
    contributor_start_date_df = forks_df.merge(contributors_df, on='login', sort=True)
    contributor_start_date_df.drop_duplicates(subset='login', keep='first', inplace=True)
    contributor_start_date_df['era'] = '';
    contributor_start_date_df['era'] = contributor_start_date_df.apply(lambda row: 'pre' if row['start_date'] >= startingtime[0] and row['start_date'] <= endingtime[0] else row['era'], axis=1)
    contributor_start_date_df['era'] = contributor_start_date_df.apply(lambda row: 'during' if row['start_date'] >= startingtime[1] and row['start_date'] <= endingtime[1] else row['era'], axis=1)
    contributor_start_date_df['era'] = contributor_start_date_df.apply(lambda row: 'post' if row['start_date'] >= startingtime[2] and row['start_date'] <= endingtime[2] else row['era'], axis=1)
    contributor_start_date_df.to_csv('contributor_start_date.csv')
    #endregion

    #region Question 2 How many contributors where new github users
    contriexists = os.path.exists("./contributor_start_date.csv")

    if(contriexists == False):
        print('No contributors file  found please check...')
        exit(1)

    print('Started Analysis for Question 2....')
    firsttime = analysis.getFirstTimeUsers(access_token)

    print('Analysis completed for Question 2')

    endregion

    region Question 3 Were the words used in the comments more negative?

    file_exists = os.path.exists("./Question3.csv")
    if file_exists == True:
        os.remove("./Question3.csv")



    for x in range(3):

        print('getting commits for ' + startingtime[x] + '  to  ' + endingtime[x] + '...')
        commit_dataframe = repo_mining.mineRepoCommits(access_token, repo_owner, repo_name,startingtime[x],endingtime[x])

        print('getting pulls for ' + startingtime[x] + '  to  ' + endingtime[x] + '...')
        pull_dataframe = repo_mining.getPullRequest(access_token,repo_name,repo_owner)

        #Analysis
        print('Started Analysis for Question 3')
        comments_dataframe = analysis.getCommentsCount(access_token, startingtime[x],endingtime[x])

    print('Analysis completed for Question 3')
    #endregion
