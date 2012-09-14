from pages.base import Base
import base64
import httplib
import urllib
import random
import os
import urlparse
import xml.etree.ElementTree as xmltree

#
# support for xml only
# json support planned once api complete
#

try:
    import json
except ImportError:
    import simplejson as json

class ApiTasks(object):

    def __init__(self, testsetup):
        self.testsetup = testsetup

        default_headers = {'Accept': 'application/xml',
                           'content-type': 'application/xml'}

        self.url = urlparse.urlparse(testsetup.base_url)
        self.host = self.url.netloc
        if ":" in self.host:
           self.host,self.port = self.host.split(':')
        else:
           self.port = 443

        self.path_prefix = "%s/api" % self.url.path
        self.headers = {}
        self.headers.update(default_headers)

    def set_basic_auth_credentials(self, username, password):
        raw = ':'.join((username, password))
        encoded = base64.encodestring(raw)[:-1]
        self.headers['Authorization'] = 'Basic ' + encoded

    def _process_response(self, response):
        return (response.status, response.read(), response.getheaders())

    def _https_connection(self):
        return httplib.HTTPSConnection(self.host, self.port)

    def _build_url(self, path, queries=()):
        if not path.startswith(self.path_prefix):
            path = '/'.join((self.path_prefix, path))
        path = urllib.quote(str(path))
        queries = urllib.urlencode(queries)
        if queries:
           path = '?'.join((path, queries))
        return path

    def _prepare_body(self, body, multipart):
        content_type = 'application/xml'
        if multipart:
            content_type, body = self._encode_multipart_formdata(body)
        elif not isinstance(body, (type(None), int, file)):
            body = json.dumps(body)

        return (content_type, body)

    def _request(self, method, path, queries=(), body=None, multipart=False, customHeaders={}):

        connection = self._https_connection()
        url = self._build_url(path,queries)
        content_type, body = self._prepare_body(body, multipart)

        self.headers['content-type'] = content_type
        self.headers['content-length'] = str(len(body) if body else 0)
        connection.request(method, url, body=body, headers=dict(self.headers.items() + customHeaders.items()))
        return self._process_response(connection.getresponse())

    def _GET(self, path, queries=(), customHeaders={}):
        return self._request('GET', path, queries, customHeaders=customHeaders)

    def _POST(self, path, body, multipart=False, customHeaders={}):
        return self._request('POST', path, body=body, multipart=multipart, customHeaders=customHeaders)

    def _DELETE(self, path, body, multipart=False, customHeaders={}):
        return self._request('DELETE', path, body=body, multipart=multipart, customHeaders=customHeaders)

    def get_element_id_list(self, target, key, \
                            username='admin', password='password'):
        """
        returns list of ids given an API target (URL path) and element key
        for example URL path 'pools' points to conductor/api/pools

        username/password optional
        """
        self.set_basic_auth_credentials(username, password)
        response = self._GET(target)
        data = xmltree.fromstring(response[1])
        id_list = []
        for child in data.findall(key):
            id_list.append(child.attrib['id'])
        return id_list

    def get_detailed_info(self, target, target_id, username='admin', password='password'):
        """
        returns dictionary of detailed info
        given an API target (URL path) and element ID
        for example URL path 'users' and ID '1' points to conductor/api/pools/1

        username/password optional
        """
        self.set_basic_auth_credentials(username, password)
        url = target + "/" + target_id
        response = self._GET(url)
        data = xmltree.fromstring(response[1])
        return data[0].text
