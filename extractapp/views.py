from django.shortcuts import render
# Create your views here.

from django.http import HttpResponse
from mendeley import Mendeley
from mendeley.session import MendeleySession
import requests
import webbrowser

CLIENT_ID = '1656'
CLIENT_SECRET = 'LA5Ns1k9bJzfaWZ8'
TOKEN_URL = 'https://api-oauth2.mendeley.com/oauth/token'
REDIRECT_URI = 'http://localhost:8000/mendeleyRedirect/'

def firstView(request):
    return HttpResponse('first view response')

def mendeleyRedirect(request):
	print request
	code = request.GET.get('code','empty')
	print code
	client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
	post_data = {"grant_type": "authorization_code", "code": code, "redirect_uri":REDIRECT_URI}
	response = requests.post(TOKEN_URL,auth=client_auth,data=post_data)
	token_json = response.json()
	access_token = token_json["access_token"]
	refresh_token = token_json["refresh_token"]
	print "Access token " + str(access_token)
	access_token = renew_token(access_token,refresh_token)
	print "Access 2" + str(access_token)

	
	return HttpResponse(token_json["access_token"],token_json["refresh_token"])



def renew_token(access_token,refresh_token):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    headers = {"Authorization": "bearer " + access_token}
    post_data = {"grant_type": "refresh_token","refresh_token": refresh_token}
    response = requests.post(TOKEN_URL,
                             auth=client_auth,
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"], token_json["refresh_token"]

def callMendeley(request):
	global mendeley_obj = Mendeley(CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
	auth = mendeley_obj.start_authorization_code_flow()
	login_url = auth.get_login_url()
	webbrowser.open(login_url,new=0,autoraise=True)
	return HttpResponse(1)


