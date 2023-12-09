#! /usr/bin/env python2

"""
Get pass and user from pass manager for offlineimap :)
"""

from subprocess import check_output


def get_pass(account):
    "Get password from pass manager"
    return check_output("pass show email/" + account + "/pass", shell=True).splitlines()[0]

def get_user(account):
    "Get user from pass manager"
    return check_output("pass show email/" + account + "/user", shell=True).splitlines()[0]
