import requests
import pprint
import sys
import json

class Moodle:
    "Access Moodle web services"

    def __init__(self, host, token):
        self.url = host + '/webservice/rest/server.php'
        self.token = token
        self.pp = pprint.PrettyPrinter(indent=4)

    def rest(self, function, params):
        payload = {
            'wstoken': self.token,
            'moodlewsrestformat': 'json',
            'wsfunction': function
        }
        payload.update(params)
        print(payload)
        headers = {'Content-Type': 'text/plain'}
        result = requests.post(self.url, data=payload)
        print(result.status_code, result.reason)
        return result

    def core_user_delete_users(self, id):
        ids = [id]
        try:
            self.proxy.core_user_delete_users(ids)
        except xmlrpc.client.Fault as err:
            print("Fault string: "  + err.faultString) 
        return

    def core_course_get_course_module(self, cmid):
        result = self.proxy.core_course_get_course_module(cmid)
        cm = result['cm']
        return cm

    def mod_assign_get_submissions(self, id):
        data = [id]
        result = self.proxy.mod_assign_get_submissions(data)
        submissions = result['assignments'][0]['submissions']
        return submissions

    def core_user_get_users(self, key, value):
        item = {
            'key': key,
            'value': value
        }
        params = {'criteria[]': [item]};
        result = self.rest('core_user_get_users', params)
        print(result.text)
        sys.exit(0)
        if result['users']:
            user = result['users'][0]
        else:
            user = []
        return user

    def core_user_get_users_guid(self, guid):
        item = {
            'key': 'username',
            'value': guid
        }
        data = [item]
        result = self.proxy.core_user_get_users(data)
        user = result['users'][0]
        return user

    def mod_assign_get_grades(self, id):
        data = [id]
        result = self.proxy.mod_assign_get_grades(data)
        grades = result['assignments'][0]['grades']
        ugrades = {}

        # reindex by userid
        for grade in grades:
            userid = grade['userid']
            grade = grade['grade']
            ugrades[userid] = grade
        return ugrades
