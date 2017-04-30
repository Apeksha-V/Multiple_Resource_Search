# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.db import models

# Create your models here.

class Result:
    def __init__(self, url, text):
        self.url = url
        self.text = text

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class Response:
    def __init__(self,query,results):
        self.results = results
        self.query = query

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
