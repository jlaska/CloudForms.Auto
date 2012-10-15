#!/usr/bin/env python

import base64, getpass

password = getpass.getpass("Enter password for base64 encoding: ")
print "Your base64 encoded password: %s" % base64.b64encode(password)
