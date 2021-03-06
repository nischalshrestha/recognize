"""Helper model class for Recognize API.

Defines models for persisting and querying data on Question(s) related to Album(s)
"""

from google.appengine.ext import ndb

class Image(ndb.Model):
	title = ndb.StringProperty()
	correct = ndb.BooleanProperty()
	image = ndb.BlobProperty()

class Question(ndb.Model):
	question_id = ndb.IntegerProperty()
	title = ndb.StringProperty()
	fact = ndb.StringProperty()
	effect = ndb.StringProperty() # Optional for client
	difficulty = ndb.StringProperty() # Optional for client
	images = ndb.StructuredProperty(Image, repeated=True)
	date = ndb.DateTimeProperty(auto_now_add=True)

class Album(ndb.Model):
	album_id = ndb.IntegerProperty()
	title = ndb.StringProperty()
	category = ndb.StringProperty()
	album_type = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)