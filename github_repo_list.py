#!/usr/bin/env python3
""" Pull a list of code repositories from the Github API """

import argparse
import os
import requests

# Reference:
# https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28

def configure_argparse():
    """ CLI parameters config """
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", help="Show repository list", action="store_true")
    parser.add_argument("-s", "--summary", help="Show summary stats", action="store_true")
    parser.add_argument("-u", "--user", help="API username")
    parser.add_argument("-t", "--token", help="API token")
    parser.add_argument("--org", help="Github organization")
    parser.add_argument("--owner", help="Github repository owner")
    parser.add_argument("-g", "--filter", help="Filter (grep) on the repository names")
    parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")

    return parser

def set_repo_url(args):
    """ Set the GH repo URL based on organization or individual owner """

    # GH API endpoint selection for orgs and users
    if args.owner:
        repo_owner = args.owner
    else:
        repo_owner = args.user

    if ("GH_ORG" in os.environ or args.org):
        if args.org:
            api_org = args.org
        else:
            api_org = os.environ["GH_ORG"]

        # use GH orgs API endpoint if organization is provided
        api_url_base = "https://api.github.com/orgs/%s/repos" % api_org

    else:

        # use GH individual repo owner for GH projects w/o organization
        api_url_base = "https://api.github.com/users/%s/repos" % repo_owner

    return api_url_base

def get_repos_json(api_url_base, api_user, api_token):
    """ Pull the list of GH repos from paginated API """

    # GH repositories list api stops at 30 results (default)
    page = 1
    json_object = []

    response_check = requests.get(api_url_base, auth=(api_user,api_token))
    if response_check.links:
        more_pages = True
    else:
        more_pages = False
        json_object.extend(response_check.json())

    while more_pages is True:
        #print("requesting URL: " + api_url_base +f"?page={page}")
        response = requests.get(api_url_base +f"?page={page}", auth=(api_user,api_token))
        json_object.extend(response.json())
        page += 1

        if response.links["next"]["url"] == response.links["last"]["url"]:
            #print("requesting last URL: " + api_url_base +f"?page={page}")
            response = requests.get(api_url_base +f"?page={page}", auth=(api_user,api_token))
            json_object.extend(response.json())
            more_pages = False

    #print(json_object)

    return json_object

def get_api_creds(args):
    """ Get API credentials from environment or CLI parameters """

    api_user = None
    api_token = None

    # default: get creds from cli params
    if args.user:
        api_user = args.user
    if args.token:
        api_token = args.token

    # prefer API credentials from CLI over environment
    if "API_USER" in os.environ:
        if args.user:
            print("API_USER env override with --user")
            api_user = args.user
        else:
            api_user = os.environ["API_USER"]

    if "API_TOKEN" in os.environ:
        if args.token:
            print("API_TOKEN env override with --token")
            api_token = args.token
        else:
            api_token = os.environ["API_TOKEN"]

    api_creds = { 'user': api_user, 'token': api_token}

    return api_creds

def main():
    """ main """

    parser = configure_argparse()
    args = parser.parse_args()

    api_creds = get_api_creds(args)
    api_user = api_creds['user']
    api_token = api_creds['token']

    repo_url_base = set_repo_url(args)

    json_object = get_repos_json(repo_url_base, api_user, api_token)

    repo_count = 0
    all_repos = len(json_object)
    for repo in json_object:

        if args.filter:
            if args.filter in repo['name']:
                repo_count += 1
                if args.list:
                    print(repo['full_name'])
        else:
            if args.list:
                print(repo['full_name'])

    if args.summary:
        print("All repos: %s" % (all_repos))
        if args.filter:
            print("%s repos: %s" % (args.filter,repo_count))

if __name__ == '__main__':
    main()
