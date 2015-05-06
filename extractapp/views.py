from django.shortcuts import render
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from mendeley import Mendeley
from mendeley.session import MendeleySession
import requests
import webbrowser , json

from extractapp.models import *

from django.core.urlresolvers import resolve

CLIENT_ID = '1656'
CLIENT_SECRET = 'LA5Ns1k9bJzfaWZ8'
TOKEN_URL = 'https://api-oauth2.mendeley.com/oauth/token'
REDIRECT_URI = 'http://localhost:8000/mendeleyRedirect/'


#make an instance of MendeleyStructure
MendeleyInstance = MendeleyStructure()

print MendeleyInstance


def firstView(request):
    return HttpResponse('first view response')




def mendeleyRedirect(request):

    state = MendeleyInstance.getSessionState()

    mendeley  = MendeleyInstance.getMendeleyObject()
    print state
    
    auth = mendeley.start_authorization_code_flow(state=state)

    print request.get_full_path()
    
    current_url = request.get_full_path()

    current_url = 'http://localhost:8000'+current_url

    mendeley_session = auth.authenticate(current_url)

    MendeleyInstance.setToken(mendeley_session.token)
    
    print mendeley_session.token
    
    return HttpResponse(current_url)


def createMendeleyDocument(request):

    mendeley_session = returnMendeleySession()

    title = request.GET.get('title','New title') 
    
    doc = mendeley_session.documents.create(title=title, type='journal')
    print doc.id
    return HttpResponse('Document Created %s' % doc.id)


def getMendeleyDocs(request):

    mendeley_session = returnMendeleySession()
    name = mendeley_session.profiles.me.display_name
    docs = mendeley_session.documents.list(view='client').items

    return render_to_response('allDocs.html', {'name' : name , 'docs' : docs})
    





def renew_token(access_token,refresh_token):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    headers = {"Authorization": "bearer " + access_token}
    post_data = {"grant_type": "refresh_token","refresh_token": refresh_token}
    response = requests.post(TOKEN_URL,
                             auth=client_auth,
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"], token_json["refresh_token"]



#method to invoke authorization for mendeley
def callMendeley(request):
    login_url = MendeleyInstance.authorizeMendeley()

    auth = MendeleyInstance.getAuthObject()

    MendeleyInstance.setSessionState(auth.state)
    request.session['state'] = auth.state
    
    print 'login_url', login_url

    return render_to_response('home.html',{'login_url' : login_url})



#return MendeleySession to talk to API
def returnMendeleySession():
    mendeley = MendeleyInstance.getMendeleyObject()
    return MendeleySession(mendeley, MendeleyInstance.getToken())

