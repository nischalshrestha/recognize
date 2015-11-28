"""Helper model class for Recognize API.

Defines models for persisting and querying data on Question(s) related to Album(s)
"""

from google.appengine.ext import ndb

class Image(ndb.Model):
	correct = ndb.BooleanProperty()
	title = ndb.StringProperty()
	image = ndb.BlobProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)

class Question(ndb.Model):
	title = ndb.StringProperty()
	images = ndb.StructuredProperty(Image, repeated=True)

class Game(ndb.Model):
	title = ndb.StringProperty()
	questions = ndb.StructuredProperty(Question)
	date = ndb.DateTimeProperty(auto_now_add=True)