# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from search import CommunicationService, Config


class CommunicationServiceTestCase(TestCase):
    def setUp(self):
        self.cs = CommunicationService(Config.getConfig("Configuration-Test.json"))

    def twitterHappyTest(self):
        """Animals that can speak are correctly identified"""
        result = {}
        self.cs.twitterSearch("175da4f64cef7305d30ec3a93493e626",result,"TestHostUrl")

        self.assertEqual(result.url, "TestHostUrl")
        self.assertEqual(result.text, "#175da4f64cef7305d30ec3a93493e626 Python test #GreedyGame")