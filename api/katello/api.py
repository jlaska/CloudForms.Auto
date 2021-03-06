import base64
import httplib
import urllib
import random
import os
import urlparse

try:
   import json
except ImportError:
   import simplejson as json


class ApiTasks(object):

    def __init__(self, testsetup):
        self.testsetup = testsetup

        default_headers = {'Accept': 'application/json',
                           'content-type': 'application/json',
                           'User-Agent': 'katello-cli/0.1'}

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
        response_body = response.read()
        try:
            response_body = json.loads(response_body, encoding='utf-8')
        except:
            pass

        return (response.status, response_body, response.getheaders())

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
        content_type = 'application/json'
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

    def _environment_by_name(self, org, envName):
        path = "organizations/%s/environments" % org
        envs = self._GET(path, {"name": envName})[1]
        if len(envs) > 0:
           return envs[0]
        else:
           return None

    def _locker_by_org(self, org):
        path = "organizations/%s/environments/" % (org)
        envs = self._GET(path, {"locker": "true"})[1]
        if len(envs) > 0:
            return envs[0]
        else:
            return None

    def _get_environment(self, orgName, envName=None):
        if envName == None:
            env = self._locker_by_org(orgName)
            envName = env['name']
        else:
            env = self._environment_by_name(orgName, envName)

        if env == None:
            print ("Could not find environment [ %s ] within organization [ %s ]") % (envName, orgName)
        return env

    def create_new_system(self, name, org, username='admin', password='admin'):
        """
        Creates a new system name in org and creates default environments.

        Usage: api.create_new_system(name, org)
        Optional arguments; username and password.
        """
        ENVIRONMENTS = ["DEV", "TEST", "STAGE", "PROD"]
        env_name = random.choice(ENVIRONMENTS)
        self.set_basic_auth_credentials(username, password)

        path = "environments/%s/systems" % self._environment_by_name(org, env_name)["id"]
        sysdata = {
                   "name" : name,
                   "cp_type" : "system",
                   "facts" : {
                              "distribution.name": "Red Hat Enterprise Linux Server",
                              "cpu.cpu_socket(s)" : "1"}}

        return self._POST(path, sysdata)[1]

    def list_orgs(self, name=None, username='admin', password='admin'):
        """
        list avaiable orgs

        Usage: api.list_orgs(org)
        Optional arguments; username and password.
        """
        self.set_basic_auth_credentials(username, password)
        path = "organizations"
        orgdata = dict()
        if name is not None:
            orgdata['name'] = name
        return self._GET(path,orgdata)[1]

    def create_org(self, name, username='admin', password='admin'):
        """
        Creates org name.

        Usage: api.create_org(org)
        Optional arguments; username and password.
        """
        self.set_basic_auth_credentials(username, password)
        path = "organizations"
        orgdata = {
                   "name" : name,
                   "description" : "This test org created via api for QE"}
        return self._POST(path,orgdata)

    def destroy_org(self, name, username='admin', password='admin'):
        """
        Deletes org matching the provided name.

        Usage: api.destroy_org(org)
        Optional arguments; username and password.
        """
        self.set_basic_auth_credentials(username, password)
        path = "organizations/%s" % name
        return self._DELETE(path,{})

    def create_envs(self, org, username='admin', password='admin'):
        """
        Creates default environments in org.

        Usage: api.create_envs(org)
        Optional arguments; username and password.
        """
        self.set_basic_auth_credentials(username, password)
        ENVIRONMENTS = ["DEV", "TEST", "STAGE", "PROD"]

        path = "organizations/%s/environments" % org
        lockerId = self._get_environment(org, "Library")['id']
        envids = [lockerId]


        for x in range(len(ENVIRONMENTS)):
            existing_env = self._get_environment(org, ENVIRONMENTS[x])
            if not existing_env:
                envdata = {"name" : ENVIRONMENTS[x],
                           "description" : "Environment created via api for QE",
                           "prior" : envids[x]}
                e = self._POST(path, {"environment": envdata})[1]
                envids.append(e["id"])
            else:
                envids.append(existing_env["id"])

    def list_users(self, name=None, username='admin', password='admin'):
        """
        list available users

        Usage: api.list_users(org)
        Optional arguments; username and password.
        """
        self.set_basic_auth_credentials(username, password)
        path = "users"
        orgdata = dict()
        if name is not None:
            orgdata['username'] = name
        return self._GET(path,orgdata)[1]

    def create_user(self, name, pw, email, username='admin', password='admin'):
        """
        Creates user name with password and email.

        Usage: api.create_user(name, pw, email)
        Optional arguments; username and password.
        """
        self.set_basic_auth_credentials(username, password)
        path = "users"
        userdata = {"username" : name,
                    "password" : pw,
                    "email" : email,
                    "disabled" : 'false'}

        return self._POST(path, userdata)[1]

    def destroy_user(self, uid, username='admin', password='admin'):
        """
        Deletes org matching the provided user id.

        Usage: api.destroy_user(uid)
        Optional arguments; username and password.
        """
        self.set_basic_auth_credentials(username, password)
        path = "users/%s" % uid
        return self._DELETE(path,{})

    def role(self, role_id):
        """
        Get role by role_id.

        Usage: api.role(role_id)
        """
        path = "roles/%s" % str(role_id)
        return self._GET(path)[1]

    def create_role(self, name, desc="QE Role created by automation", username='admin', password='admin'):
        """
        Create role name with description.

        Usage: api.create_role(name)
        Optional arguments; desc, username, and password.
        """
        self.set_basic_auth_credentials(username, password)
        path = "roles"

        data = {
                "name" : name,
                "description" : desc}        
        return self._POST(path, {"role": data})[1]

    def ping(self, username='admin', password='admin'):
        """
        Pings the application and returns a status for services.

        Usage: api.ping()
        Optional arguments: username and password
        """
        self.set_basic_auth_credentials(username, password)
        path = "ping"
        return self._GET(path)
