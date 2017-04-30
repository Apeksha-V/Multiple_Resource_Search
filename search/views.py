import thread
import threading
import urllib2
import json

from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest

from search import Config
from search.CommunicationService import CommunicationService
from search.models import Response


search = CommunicationService(Config.getConfig("Configuration.json"))

def index(request):
    if request.GET.get('q'):
        query = request.GET['q']
        hostUrl = ''.join(['http://', get_current_site(request).domain, request.get_full_path()])
        response = search.callApi(query,hostUrl)

    else:
        return HttpResponseBadRequest()
    return HttpResponse(response.toJSON())

