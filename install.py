#!/usr/bin/env python
import todoist
import getpass
import todoist
import shutil
import json
import sys
import os


if os.path.isfile(os.path.join(os.path.expanduser('~'), '.task', 'hooks', 'config.json')):
    print("Config file already exists. Skipping config.")
else:
    # ask the user for their todoist credentials & update config
    print('Warning: username and password for Todoist stored in plaintext in config file at ~/.task/hooks/config.json!')

    # TODO ask for a list of projects to ignore instead of making them manually update config.

    # load config
    try:
        with open('config.json', 'r') as configFile:
            config = json.load(configFile)
    except Exception:
       print('Failed to load config.')
       sys.exit(1)

    success = False
    i = 0
    while not success and i <= 3:
        username = raw_input('Todoist login: ')
        password = getpass.getpass('Todoist password: ')

        config['user']['username'] = username
        config['user']['password'] = password

        api = todoist.TodoistAPI()
        user = api.user.login(config['user']['username'], config['user']['password'])
        resp = api.sync()
        try:
            if resp['error_code'] == 401:
                print('Login failed.')
            else:
                print('Failed with code: %s.' % resp['error_code'])
            i = i + 1
            if i == 3:
                print 'Too many attempts.'
                sys.exit(1)
            else:
                print 'Try again.'
        except Exception:
            print('Login succeeded.')
            success = True

    # install
    try:
        with open(os.path.join(os.path.expanduser('~'), '.task', 'hooks', 'config.json'), 'w+') as newConfig:
            newConfig.write(json.dumps(config))
    except Exception:
        print('Failed to install config.')
        sys.exit(1)
shutil.copy('on-add-task.py', os.path.join(os.path.expanduser('~'), '.task', 'hooks'))
sys.exit(0)
