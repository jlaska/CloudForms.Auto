#!/usr/bin/env python

import httplib2

ce_user = 'admin'
ce_pass = 'password'
url = 'https://qeblade40.rhq.lab.eng.bos.redhat.com/conductor/api/images'

http = httplib2.Http(disable_ssl_certificate_validation=True)

http.add_credentials(ce_user, ce_pass)
response, content = http.request(url, 'GET', headers={'Accept' : 'application/xml'})

print "Response: %s" % response
print "Content: %s" % content
