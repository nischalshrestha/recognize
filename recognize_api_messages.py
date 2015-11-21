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

# Game model which contains Level models
# class Game(messages.Message):

# Level model which has Image models
# class Level(messages.Message):

class ImageRequest(messages.Message):
	search_exp = messages.StringField(1)

# Image model which has a title, whether it is the correct answer or not, and the image
class ImageMessage(messages.Message):
    """Sub model for representing an author."""
    # correct = messages.BooleanField()
    image_url = messages.StringField(1)

# Collection of ImageMessages (i.e. collection of image urls)
class ImageCollection(messages.Message):
	items = messages.MessageField(ImageMessage, 1, repeated=True)
