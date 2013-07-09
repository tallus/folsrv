#!/usr/bin/env python

import unittest
from flask import Flask

app = Flask(__name__)
from folsrv import views
