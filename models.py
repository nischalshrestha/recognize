"""Helper model class for Recognize API.

Defines models for persisting and querying data on Image(s) related to Album(s)
"""

from google.appengine.ext import ndb

class Image(ndb.Model):
	# correct = ndb.BooleanProperty()
	image = ndb.BlobProperty()

class Album(ndb.Model):
	title = ndb.StringProperty()
	images = ndb.StructuredProperty(Image, repeated=True)