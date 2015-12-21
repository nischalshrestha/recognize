"""Recognize API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

# import Image
import urllib2

import endpoints
from protorpc import messages
from protorpc import message_types

from protorpc import remote
from google.appengine.ext import ndb
from google.appengine.api import images

from models import Album
from models import Question
from models import Image

import json
# from apiclient.discovery import build

WEB_CLIENT_ID = '141815902829-9brrjl3uhogcqhnl111uvm9u556op701.apps.googleusercontent.com'
ANDROID_CLIENT_ID = '141815902829-g950g3rrmjef0v5op1ggj5aq9oauuoj2.apps.googleusercontent.com'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

package = 'Recognize'

# Message Classes
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

# Performs a google image search given the search expression
def query_image(exp):
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey="AIzaSyAN3l_irEsAG2kT3isRzL8R-baMkOcZgZs")
  # https://developers.google.com/custom-search/json-api/v1/reference/cse/list
  res = service.cse().list(
        q=exp,
        cx='008947772147471846402:fdhywbjbitw',
        num=4,
        searchType="image",
        imgColorType='color',
        imgType='photo',
        safe='high',
        rights='cc_publicdomain',
        filter='1'
      ).execute()
  parsed_res = json.dumps(res)
  json_res = json.loads(parsed_res)
  items = []
  for i in range(4):
    img_url = json_res['items'][i]['link']
    img = Image()
    f = ""
    try: 
      f = urllib2.urlopen(img_url).read() # Opens the url as an image file so we can store it!
    except urllib2.HTTPError, e:
      print "There was an http error with url: "+img_url
      print e
    # TODO: Figure out how to best preserve quality while resizing
    if f:
      op_img = images.Image(f)
      op_img.resize(width=256, height=256, crop_to_fit=False)
      small_img = op_img.execute_transforms(output_encoding=images.JPEG)
      img.image = small_img
    img_id = img.put()
    items.append(ImageMessage(image_url="getgimage?id="+img_id.urlsafe()))
  return items

STORED_GREETINGS = GreetingCollection(items=[
	Greeting(message='hello world!'),
	Greeting(message='goodbye world!'),
])

"""Recognize API v1."""
@endpoints.api(name='recognize', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE],
               scopes=[endpoints.EMAIL_SCOPE])
class Recognize(remote.Service):
  
  # Return all Greetings
  @endpoints.method(message_types.VoidMessage, GreetingCollection,
                    path='recognizegreeting', http_method='GET',
                    name='recognize.listGreeting')
  def greetings_list(self, unused_request):
    return STORED_GREETINGS

  # Multiply message
  MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(
      Greeting,
      times=messages.IntegerField(2, variant=messages.Variant.INT32,
                                required=True))

  @endpoints.method(MULTIPLY_METHOD_RESOURCE, Greeting,
                    path='recognizegreeting/{times}', http_method='POST',
                    name='recognize.multiply')
  def greetings_multiply(self, request):
    return Greeting(message=request.message * request.times)
    
  # ID_RESOURCE = endpoints.ResourceContainer(
  #     message_types.VoidMessage,
  #     id=messages.IntegerField(1, variant=messages.Variant.INT32))

  # ID_RESOURCE = endpoints.ResourceContainer(
  #     ImageRequest,
  #     id=messages.StringField(1, required=True))
  # @endpoints.method(ID_RESOURCE, ImageCollection,
  #                   path='hellogreeting/{id}', http_method='GET',
  #                   name='greetings.getImages')
  # def greeting_get(self, request):
  #   # return ImageCollection(items=query_image(request.id))
  #   try:
  #     return STORED_GREETINGS.items[request.id]
  #   except (IndexError, TypeError):
  #     raise endpoints.NotFoundException('Greeting %s not found.' %
  #                                       (request.id,))

  # @endpoints.method(message_types.VoidMessage, Greeting,
  #                 path='authed', http_method='POST',
  #                 name='greetings.authed')
  # def greeting_authed(self, request):
  #   current_user = endpoints.get_current_user()
  #   email = (current_user.email() if current_user is not None
  #            else 'Anonymous')
  #   return Greeting(message='hello %s' % (email,))

  # Return all created Album(s) on website
  @endpoints.method(message_types.VoidMessage, AlbumCollection,
                    path='recognize/albums', http_method='GET',
                    name='albums.get')
  def albums_list(self, unused_request):
    albums = Album.query().order(-Album.date)
    items = []
    for album in albums:
      a = AlbumMessage(title=album.title, category=album.category, album_type=album.album_type, date=str(album.date.date()))
      questions = Question.query(ancestor=album.key).order(-Question.date).fetch()
      for q in questions:
        q_msg = QuestionMessage(title=q.title, fact=q.fact)
        q_images = q.images
        for image in q_images:
          q_msg.images.append(ImageMessage(image_url=image.image))
        a.questions.append(q_msg)
      items.append(a)
    return AlbumCollection(albums=items)


APPLICATION = endpoints.api_server([Recognize])