from moodle import Moodle
import sys
import pprint
import wget
import urllib
import argparse
import configparser

# get config
config = configparser.RawConfigParser()
config.read('config.cfg')
endpoint = config.get('moodle', 'endpoint')
wstoken = config.get('moodle', 'wstoken')

# create webservice client
moodle = Moodle(endpoint, wstoken)

# set up command line argumetns
parser = argparse.ArgumentParser(description = "Upload assignment submission")
parser.add_argument('--assignid', help = "Assignment course module id", type = int, required = True)
parser.add_argument('--guid', help = 'Student\'s GUID (Moodle login)', type = str, required = True)
parser.add_argument('--file', help = "File to upload (student submission)", type = str, required = True)
args = parser.parse_args()

# get arguments
cmid = args.assignid
filename = args.file
guid = args.guid

# look up cmid to get assignment instanceid (hopefully)
cm = moodle.core_course_get_course_module(cmid)
instance = cm['instance']
modname = cm['modname']
name = cm['name']
print("\nGET COURSE MODULE FOR id=" + str(cmid))
print("    instance = " + str(instance))
print("    name = " + name)
print("    modname = " + modname)
if modname != 'assign':
    print('    Course module is not an assignment. Cannot continue')
    sys.exit(0)

# look up guid to find user id
user = moodle.core_user_get_users_guid(guid)
fullname = user['fullname']
userid = user['id']
print("\nGETTING INFO ABOUT USER guid=" + guid)
print("    fullname = " + fullname)
print("    userid = " + str(userid))

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

