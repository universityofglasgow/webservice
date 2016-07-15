import xmlrpc.client
import pprint

class Moodle:
    "Access Moodle web services"

    def __init__(self, host, token):
        url = host + '/webservice/xmlrpc/server.php?wstoken=' + token        
        self.proxy = xmlrpc.client.ServerProxy(url)

    def core_course_get_course_module(self, cmid):
        result = self.proxy.core_course_get_course_module(cmid)
        cm = result['cm']
        return cm

    def mod_assign_get_submissions(self, id):
        data = [id]
        result = self.proxy.mod_assign_get_submissions(data)
        submissions = result['assignments'][0]['submissions']
        return submissions

    def core_user_get_users(self, userid):
        item = {
            'key': 'id',
            'value': userid
        }
        data = [item]
        result = self.proxy.core_user_get_users(data)
        user = result['users'][0]
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
