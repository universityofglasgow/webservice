from moodle import Moodle
import sys
import pprint
import wget
import urllib
import configparser

# get config
config = configparser.RawConfigParser()
config.read('config.cfg')
endpoint = config.get('moodle', 'endpoint')
wstoken = config.get('moodle', 'wstoken')

# create webservice client
moodle = Moodle(endpoint, wstoken)

# get assignment cm id from command line
if len(sys.argv) != 2:
    print("\nUsage:\n")
    print("pythong3 ams.py <assignment id>\n")
    sys.exit(0)
cmid = sys.argv[1]

# look up cmid to get assignment instanceid (hopefully)
cm = moodle.core_course_get_course_module(cmid)
instance = cm['instance']
modname = cm['modname']
name = cm['name']
print("\nGET COURSE MODULE FOR id=" + cmid)
print("    instance = " + str(instance))
print("    name = " + name)
print("    modname = " + modname)
if modname != 'assign':
    print('    Course module is not an assignment. Cannot continue')
    sys.exit(0)
    
submissions = moodle.mod_assign_get_submissions(instance)
grades = moodle.mod_assign_get_grades(instance)
print('\nGET SUBMISSIONS')
count = 1
for submission in submissions:
    status = submission['status']
    userid = submission['userid']
    if status != 'submitted':
        continue;

    # look up user
    user = moodle.core_user_get_users(userid)
    print('    Submission # ' + str(count))
    print('        Submitted by ' + user['fullname'])
    print('        Grade ' + grades[userid])

    #pprint.pprint(submission)
    #sys.exit(0)

    # check for and get info about file(s)
    fileareas = submission['plugins'][0]['fileareas'][0]
    files = fileareas['files']
    for sfile in files:
        filepath = sfile['filepath']
        fileurl = sfile['fileurl']

        # download the file using url (needs token added)
        print('        File name ' + filepath)
        downloadurl = fileurl + '?token=' + wstoken
        try:
            wget.download(downloadurl)
        except urllib.error.HTTPError:
            print('        Unable to download file.')

    count = count + 1

