# command to recursively change group and owner
# chown -R owner:group directory/
# need the numeric value of owner and group for 
# os.chown(fd, uid, gid)
# but names are okay for 
# shutil.chown(path, user, group)

import os
import shutil
import pwd
import grp

""" 
determine if the directory is owned by root
if the owner is root, put the name of the directory in a list
NOTE: for this use case, the username matches the name of the directory
catch an error where there is no user by that name
get the group from the username
recursively set ownership of the directory to that user and group
"""
class RecursePermChange:
    def __init__(self, dir):
        self.dir = dir

    def get_dir_group(self, uname):
        stat_info = os.stat(self.dir + uname)
        gid = stat_info.st_gid
        group = grp.getgrgid(gid).gr_name
        print("directory group is " + group)
        return group
    
    def get_group_by_user(self, uname):
        if self.user_exists(uname):
            gid = pwd.getpwnam(uname).pw_gid
            usr_group = grp.getgrgid(gid).gr_name
            print("user group is " + usr_group)
            return usr_group
    
    def owned_by_root(self, uname):
        if self.get_dir_group(uname) == 'root':
            print(self.dir + uname + " is owned by root")
            return True

    @staticmethod    
    def user_exists(uname):
        try:
            pwd.getpwnam(uname)
            return True
        except KeyError:
            print("user " + uname + " does not exist")
            return False

    def get_root_dir_list(self):
        file_list = os.listdir(self.dir)
        print(file_list)
        dir_list = []
        for file in file_list:
            if os.path.isdir(self.dir + file) and \
                             self.owned_by_root(file) and \
                             self.user_exists(file):
                print("adding " + file + " to root dir list")
                dir_list.append(file)
        print(dir_list)
        return dir_list
    
    def change_permissions(self, uname):
        group = self.get_group_by_user(uname)
        shutil.chown((self.dir + uname), uname, group)

test = RecursePermChange('/home/katfish/Desktop/WorkStuff/permissions_tests/')
test.get_root_dir_list()
for file in test.get_root_dir_list():
    test.change_permissions(file)

# test.get_group_by_user("scripts")