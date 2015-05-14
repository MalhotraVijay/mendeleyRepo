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

from mendeley.models.common import Person


CLIENT_ID = '1656'
CLIENT_SECRET = 'LA5Ns1k9bJzfaWZ8'
TOKEN_URL = 'https://api-oauth2.mendeley.com/oauth/token'
REDIRECT_URI = 'http://localhost:8000/mendeleyRedirect/'


#make an instance of MendeleyStructure
MendeleyInstance = MendeleyStructure()

print MendeleyInstance




def mendeleyRedirect(request):

    if(not checkDjangoSession(request.session)):
        response = {'error' : 'Authentication required to save the document'}
        try:

            state = MendeleyInstance.getSessionState()
            mendeley  = MendeleyInstance.getMendeleyObject()
            #print state

            auth = mendeley.start_authorization_code_flow(state=state)
            #print request.get_full_path()

            current_url = request.get_full_path()
            current_url = 'http://localhost:8000'+current_url

            auth_response = ""
            
            auth_response = auth.authenticate(current_url)
            MendeleyInstance.setToken(auth_response.token)
            print 'auth token: ', auth_response.token
            
            if auth_response != "":
                request.session['thisSession'] = True
        except:
            response = {'error' : 'Authentication required to save the document'}
            return HttpResponse(current_url)

        return render_to_response('close_window.html')
    else:
        response = {'error' : 'Already authenticated'}
        return HttpResponse(json.dumps(response))


def createMendeleyDocument(request):
    
    if(checkDjangoSession(request.session)):
        response = {'error' : 'Authentication required to save the document'}
        #try:

        mendeley_session = returnMendeleySession()
        print 'in the tyr blocl'

        #print request.POST
        document = json.loads(request.POST.get('document'))
        print document
        title =  document.get('title')
        city = document.get('city')
        doc_type = document.get('doc_type')

        year = document.get('year')
        pages = document.get('pages')
        publisher =  document.get('publisher')
        authors =  document.get('authors')
        abstract = document.get('abstract')
        tags = document.get('tags')
        keywords =  document.get('keywords')
        print authors,keywords

        newauthors = []
        for author in authors:
            name = author.split(',')
            newauthors.append(Person.create(name[1],name[0])) #pattern Person.create(first_name,last_name)

        print newauthors

        newtags = []

        for tag in tags:
            t = ""
            try:
                t = tag.split(';')[0]
            except:
                t = tag
            if(len(t)<50):
                newtags.append(t)

        print newtags
            
        doc = mendeley_session.documents.create(title=title, type= 'Working_Paper', year = year, city = city, publisher = publisher, abstract = abstract, keywords = keywords, tags = newtags, authors = newauthors, pages = pages)
        print doc.id
        #response = {'error' : 'ductomc'}
        response = {'success' : {'documentId' : doc.id, 'title' : doc.title }}
        #except:
        #    response = {'error' : 'Authentication required to save the document'}
        return HttpResponse(json.dumps(response))

    else:
        response = {'error' : 'Authentication required to save the document'}
        return HttpResponse(json.dumps(response))

def getMendeleyDocs(request):

    if(checkDjangoSession(request.session)):
        try:
            mendeley_session = returnMendeleySession()
            name = mendeley_session.profiles.me.display_name
            docs = mendeley_session.documents.list(view='client').items

            return render_to_response('allDocs.html', {'name' : name , 'docs' : docs})
        except:
            response = {'error' : 'Authentication required to access this endpoint'}
            return HttpResponse(json.dumps(response))

    response = {'error' : 'Django Session expired'}
    return HttpResponse(json.dumps(response))
    


def getSingleDocument(request):

    if(checkDjangoSession(request.session)):
        try:
            mendeley_session = returnMendeleySession()
            document_id = request.GET.get('docid','29a7bb5d-36b1-3e22-a6c2-707359098ad7')

            print document_id

            doc = mendeley_session.documents.get(document_id)

            try:
                print 'dict', doc.__dict__

            except :
                pass

            return render_to_response('singleDoc.html', {'doc' : doc})
        except:
            response = {'error' : 'Authentication required to access this endpoint'}
            return HttpResponse(json.dumps(response))
    response = {'error' : 'Django Session expired'}
    return HttpResponse(json.dumps(response))
    



#method to invoke authorization for mendeley
def callMendeley(request):
    
    login_url = authenticateMendeley()
    print 'login_url', login_url

    return render_to_response('home.html',{'login_url' : login_url})



#return MendeleySession to talk to API
def returnMendeleySession():
    mendeley = MendeleyInstance.getMendeleyObject()
    return MendeleySession(mendeley, MendeleyInstance.getToken())




def authenticateMendeley():
    
    login_url = MendeleyInstance.authorizeMendeley()
    auth = MendeleyInstance.getAuthObject()
    MendeleyInstance.setSessionState(auth.state)
    
    print 'login_url', login_url
    return login_url
    


def checkDjangoSession(session):

    print session.__dict__
    try:
        
        if session['thisSession'] and session['thisSession'] == True:
            print 'session key set:', session['thisSession']
            return True
    except:
        return False
    return False

def logout(request):
    session = request.session
    try:
        if session['thisSession'] and session['thisSession'] == True:
            del request.session['thisSession']
            return HttpResponse(json.dumps({'message':'Successfully Logged out of the system'}))
    except:
        return HttpResponse(json.dumps({'message':'Already Logged out of the system'}))
    return HttpResponse(json.dumps({'message':'Already Logged out of the system'}))
    
