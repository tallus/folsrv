import unittest
from flask import Flask
app = Flask(__name__)

from folsrv import app

if __name__ == "__main__":
    app.debug = True   # for dev purposes only, never production
    app.run()

