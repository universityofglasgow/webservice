# Python/Webservice Moosh style utility
from moodle import Moodle
import sys
import pprint
import wget
import urllib
import argparse
import configparser
import os

# set up command line arguments
epilogtext = """
    \n
    Commands:\n\n

    delete-users username1, username2, username3...\n
"""
parser = argparse.ArgumentParser(description = "Upload assignment submission", epilog = epilogtext)
parser.add_argument('--moodleurl', help = "Moodle url", type = int, required = False)
parser.add_argument('--token', help = 'Token', type = str, required = False)
parser.add_argument('command', help = 'Command', type = str)
parser.add_argument('arguments', help = 'Arguments for command', type = str, nargs = '*')
args = parser.parse_args()
moodleurl = args.moodleurl
token = args.token
command = args.command
arguments = args.arguments

# if config file exists get config
if os.path.isfile('config.ini'):
    config = configparser.RawConfigParser()
    config.read('config.ini')
    if not moodleurl:
        moodleurl = config.get('moodle', 'moodleurl')
    if not token:
        token = config.get('moodle', 'token')

# are we set up?
if (not token) or (not moodleurl):
    print('Token and Moodle URL must be specified either on command line or in config.ini file')
    sys.exit(0)

# create webservice client
moodle = Moodle(moodleurl, token)

# user-delete (list of usernames)
if command == "user-delete":
    print("user-delete: requires web service core_user_delete_users, core_user_get_users")

    # Find the users in Moodle
    users = [];
    for username in arguments:
        user = moodle.core_user_get_users('username', username)
        if user:
            users.append(user) 

    # run through and delete
    for user in users:
        name = user['firstname'] + ' ' + user['lastname']
        id = user['id']
        print('Deleting ' + name)
        moodle.core_user_delete_users(id)
    sys.exit(0)

print("Command not recognised, '" + command + "'")
sys.exit(0)

