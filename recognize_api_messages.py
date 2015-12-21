#!/usr/bin/python

"""ProtoRPC message class definitions for Recognize API."""

from protorpc import messages

# Tutorial stuff below
class Greeting(messages.Message):
	"""Greeting that stores a message"""
	message = messages.StringField(1)

class GreetingCollection(messages.Message):
	"""Collection of Greetings."""
	items = messages.MessageField(Greeting, 1, repeated=True)

class ImageRequest(messages.Message):
	search_exp = messages.StringField(1)

# Image model which has a title, whether it is the correct answer or not, and the image
class ImageMessage(messages.Message):
    # correct = messages.BooleanField()
    image_url = messages.BytesField(1)

# Collection of ImageMessages (i.e. collection of image urls)
class ImageCollection(messages.Message):
	items = messages.MessageField(ImageMessage, 1, repeated=True)

class QuestionMessage(messages.Message):
	title = messages.StringField(1)
	fact = messages.StringField(2)
	images = messages.MessageField(ImageMessage, 3, repeated=True)

class AlbumMessage(messages.Message):
	title = messages.StringField(1)
	category = messages.StringField(2)
	album_type = messages.StringField(3)
	date = messages.StringField(4)
	questions = messages.MessageField(QuestionMessage, 5, repeated=True)

class AlbumCollection(messages.Message):
	albums = messages.MessageField(AlbumMessage, 1, repeated=True)
