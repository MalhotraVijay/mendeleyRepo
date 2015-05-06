from django.db import models

# Create your models here.


print "Mendeley model definition called "


from mendeley import Mendeley
from mendeley.session import MendeleySession

CLIENT_ID = '1656'
CLIENT_SECRET = 'LA5Ns1k9bJzfaWZ8'
TOKEN_URL = 'https://api-oauth2.mendeley.com/oauth/token'
REDIRECT_URI = 'http://localhost:8000/mendeleyRedirect/'




class MendeleyStructure():


    def authorizeMendeley(self):
        self.mendeley_obj = Mendeley(CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
        self.auth = self.mendeley_obj.start_authorization_code_flow()

        login_url = self.auth.get_login_url()
        
        return login_url


    def getMendeleyObject(self):
        return self.mendeley_obj


    def getAuthObject(self):
        return self.auth

    def setSessionState(self,state):
        self.state = state

    def getSessionState(self):
        return self.state

    def setToken(self,token):
        self.token = token

    def getToken(self):
        return self.token
