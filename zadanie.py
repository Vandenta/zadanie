import json
import requests
import argparse
import database


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--user_name", type=str, dest="name")
parser.add_argument("-r", "--repo", type=str, dest="repo")
parser.add_argument("-b", "--branch", type=str, dest="branch")
args = parser.parse_args()
user_name = args.name
repo_name = args.repo
branch_name = args.branch

URL_APP = "https://api.github.com"
URL = URL_APP + "/repos/" + user_name + "/" + repo_name + "/commits?per_page=100,sha=" + branch_name

request = requests.get(URL)
json_object = json.loads(request.text)
length = len(json_object)


def get_commits():
    list_num = 0
    while list_num < length:
        checking = json_object[list_num]
        sha = checking["sha"]
        commit = checking["commit"]
        for x in commit:
            message = commit["message"]
            committer = commit["committer"]
            for y in committer:
                committer_name = committer["name"]
        info_sha = repo_name + "/" + branch_name + "/" + sha + ": " + message + " [" + committer_name + "]"
        print(info_sha)
        list_num = list_num + 1
        database.database(user_name, repo_name, branch_name, sha, message, committer_name)


if request.status_code == 200:
    get_commits()
elif request.status_code == 404:
    print("User name, repository name or branch name are incorrect")
else:
    print("ERROR")

