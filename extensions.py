# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""

from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt()




from flask.ext.mongoengine import MongoEngine
db = MongoEngine()


from flask.ext.cache import Cache
cache = Cache()

from flask.ext.mail import Mail
mail = Mail()

from flask.ext.debugtoolbar import DebugToolbarExtension
debug_toolbar = DebugToolbarExtension()