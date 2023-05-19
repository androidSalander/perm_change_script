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
if the owner is root
get the name of the directory
find the username that matches the name of the directory
get value of user and group
recursively set ownership of the directory to that user and group
"""
class RecursePermChange:
    def __init__(self, dir, user):
        self.dir = dir

    def get_dir_user(self):
        stat_info = os.stat(self.dir)
        uid = stat_info.st_uid
        user = pwd.getpwuid(uid).pw_name
        print("directory user is " + user)
        return user

    def get_dir_group(self, uname):
        stat_info = os.stat(self.dir + uname)
        gid = stat_info.st_gid
        group = grp.getgrgid(gid).gr_name
        print("directory group is " + group)
        return group
    
    def get_group_by_user(self, user):
        gid = pwd.getpwnam(user).pw_gid
        usr_group = grp.getgrgid(gid).gr_name
        print("user group is " + usr_group)
        return usr_group
    
    def owned_by_root(self, uname):
        if self.get_dir_group(uname) == 'root':
            print(self.dir + uname + " is owned by root")
            return True
        
    def get_uname_list(self):
        file_list = os.listdir(self.dir)
        uname_list = []
        for file in file_list:
            print("adding " + file + " to username list")
            uname_list.append(file)
        return uname_list

    def get_root_dir_list(self):
        file_list = os.listdir(self.dir)
        print(file_list)
        dir_list = []
        for file in file_list:
            if os.path.isdir(self.dir + file) and self.owned_by_root(file):
                print("adding " + file)
                dir_list.append(file)
        print(dir_list)
        return dir_list
    
    def change_permissions(self):
        group = self.get_group_by_user(self.user)
        shutil.chown(self.dir, self.user, group)

    def get_directories(self, full_path):
        for file in self.get_dir_list(dir):
            print("testing " + file)

            if os.path.isdir(full_path + file):
                print("file " + file + " is a directory")
                return True

# get_directories("permissions_tests", "/home/katfish/Desktop/WorkStuff/permissions_tests/")
# get_group("permissions_tests")
# zhuChongba = RecursePermChange('/home/katfish/Desktop/WorkStuff/permissions_tests/zhuChongba', 'zhuChongba')
# calFalcons = RecursePermChange('/home/katfish/Desktop/WorkStuff/permissions_tests/calFalcons', 'calFalcons')
# test_dir.get_group()
# test_dir.get_user()
# test_dir.owned_by_root()
# test_dir.get_root_dir_list()
# zhuChongba.get_group_by_user(zhuChongba.user)
# calFalcons.get_group_by_user(calFalcons.user)
# zhuChongba.change_permissions()
test = RecursePermChange('/home/katfish/Desktop/WorkStuff/permissions_tests/')
test.get_root_dir_list()