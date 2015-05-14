from django.shortcuts import render

from django.http import HttpResponse

import urllib2

import json
from datetime import datetime
import xml.etree.ElementTree as ET


from extractapp.views import *


# Create your views here.


def fetchDataFromWorldcat(request):

    
    
    documentId = request.GET.get('documentId','904069807')

    data = urllib2.urlopen('http://www.worldcat.org/webservices/catalog/content/'+documentId+'?wskey=xBo82kDJHO1YFvNihVRsD2YXIhhvJsnEAwN8d7GuygBIXRsiNRSgYeNeFI3XKvCdrOkMliqUHbjO5vcK')

    result = data.read()

    root = ET.fromstring(result)

    doc_type = None
    title = None
    authors = None
    publisher = None
    city = None
    year = None
    pages = None
    abstract = 0
    tags = []

    keywords = []
    abstract_array = []
    publisher_array = []
    page_array =[]

    url_array = []
    url_obj =[]
    for datafield in root:
        dict1 = datafield.attrib
        for key in dict1.keys():
            if key == "tag":
                if (dict1[key] == "245"):
                    # print "Title :"
                    for subfield in datafield:
                        dict2 = subfield.attrib
                        for key in dict2.keys():
                            if key == "code":
                                if(dict2[key] == "a"):
                                    title = subfield.text
                elif (dict1[key] == "720"):
                    # print "Authors :"
                    for subfield in datafield:
                        dict2 = subfield.attrib
                        for key in dict2.keys():
                            if key == "code":
                                if(dict2[key] == "a"):
                                    authors = (subfield.text).split(';')
                elif (dict1[key] == "655"):
                    # print "Type :"
                    for subfield in datafield:
                        doc_type = subfield.text
                elif (dict1[key] == "651"):
                    for subfield in datafield:
                        #print subfield.text
                        keywords = (subfield.text).split(';')
                elif (dict1[key] == "520"):
                    # print "520:"
                    for subfield in datafield:
                        #print subfield.text
                        abstract_array.append(subfield.text)

                elif (dict1[key] == "260"):
                    # print "260:"
                    for subfield in datafield:
                        #print subfield.text
                        publisher_array.append(subfield.text)
                elif (dict1[key] == "856"):
                    # print "856:"
                    url_obj.append(datafield)
                    for subfield in datafield:
                        #print subfield.text
                        url_array.append(subfield.text)
                elif (dict1[key] == "300"):
                    # print "300:"
                    for subfield in datafield:
                        #print subfield.text
                        page_array.append(subfield.text)


    def url_extracter(obj):
        last = len(obj)-1
        target_obj = obj[last]
        return target_obj[1].text

    def abstract_extractor(obj):
        length = len(obj)
        lower = 1
        upper = length-1
        count = 0
        for i in range(lower,upper):
            tags.append(obj[i])
        abstract = obj[length-1]
        return abstract

    abstract = abstract_extractor(abstract_array)
    link = url_extracter(url_obj)
    year = publisher_array[2]
    city = publisher_array[1]
    publisher = publisher_array[0]
    pages = (page_array[0])
    accessed = str(datetime.now())
    
    print "Title:" + title
    print "Type:" + doc_type
    print "Authors:",authors
    print "Year:" + year
    print "Pages:" + pages
    print "Abstract:" + abstract
    print "Tags:" + str(tags)
    print "Author Keywords:" + str(keywords)
    print "City:" + city
    print "Accessed:" + accessed
    print "Publisher:" + publisher
    print "Url:" + link

    document = {
        'title' : title,
        'doc_type' : doc_type,
        'year' : year,
        'pages' : pages,
        'accessed' : accessed,
        'authors' : authors,
        'abstract' : abstract,
        'tags' : tags,
        'keywords' : keywords,
        'city' : city,
        'publisher' : publisher,
        'url' : link
        }

    if(not checkDjangoSession(request.session)):
        #get the login url from the autheticate mendeley function
        login_url = authenticateMendeley()
        return HttpResponse(json.dumps({'document' : document,
                                        'login_url': login_url}))
    else:
        return HttpResponse(json.dumps({'message' : 'Mendeley Authentication done successfully',
                                        'document':document}))
    


    
