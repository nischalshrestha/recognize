"""Helper model class for Recognize API.

Defines models for persisting and querying data on Question(s) related to Album(s)
"""

from google.appengine.ext import ndb

class Image(ndb.Model):
	title = ndb.StringProperty()
	correct = ndb.BooleanProperty()
	image = ndb.BlobProperty()

class Question(ndb.Model):
	title = ndb.StringProperty()
	fact = ndb.StringProperty()
	effect = ndb.StringProperty()
	difficulty = ndb.StringProperty()
	images = ndb.StructuredProperty(Image, repeated=True)
	date = ndb.DateTimeProperty(auto_now_add=True)

class Album(ndb.Model):
	title = ndb.StringProperty()
	category = ndb.StringProperty()
	album_type = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)