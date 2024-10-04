# github_repo_list.py
Python API client for Github repository reporting

Features

* List Github repositories
* Filter (grep) on list
* Summary statisics (total and selected number of repositories


## Tech stack

- Github credentials (user, personal access token with read-permission on repositories)
- Python 3
- Python Requests library

## Setup

Create Python virtualenv for dependencies and load it:

```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt
(venv) $ ./github_repo_list.py -h
usage: github_repo_list.py [-h] [-l] [-s] [-u USER] [-t TOKEN] [--org ORG] [--owner OWNER] [-g FILTER] [-d]

options:
  -h, --help            show this help message and exit
  -l, --list            Show repository list
  -s, --summary         Show summary stats
  -u USER, --user USER  API username
  -t TOKEN, --token TOKEN
                        API token
  --org ORG             Github organization
  --owner OWNER         Github repository owner
  -g FILTER, --filter FILTER
                        Filter (grep) on the repository names
  -d, --debug           Debug mode
(venv) $

```



## Usage
List (--list) all public repositories in the Github account (--owner) "ovirt":
```
(venv) $ ./github_repo_list.py --user "<github_username>" --token "<github_pat>" --list --owner ovirt
```

List all public repositories in the Github project "ovirt", filter (--filter) for repositories that contain 'node' in their names:

```
(venv) $ ./github_repo_list.py -u "<github_username>" -t "<github_pat>" -l --owner ovirt --filter node
```


