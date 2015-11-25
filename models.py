"""Helper model class for Recognize API.

Defines models for persisting and querying data on Image(s) related to Album(s)
"""

from google.appengine.ext import ndb

class Image(ndb.Model):
	correct = ndb.BooleanProperty()
	title = ndb.StringProperty()
	image = ndb.BlobProperty()

class Album(ndb.Model):
	title = ndb.StringProperty()
	images = ndb.StructuredProperty(Image, repeated=True)

class Game(ndb.Model):
	title = ndb.StringProperty()
	albums = ndb.StructuredProperty(Album)