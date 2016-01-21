import webapp2

import os
import time
import jinja2
import urllib2

from google.appengine.ext import ndb
from google.appengine.api import images

from models import Album
from models import Question
from models import Image

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Home(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

class Auth(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('auth.html')
		self.response.write(template.render(template_values))

class Admin(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('admin.html')
		self.response.write(template.render(template_values))

class Match(webapp2.RequestHandler):
	def get(self):
		if len(self.request.GET) and self.request.GET['cancel']:
			urlstring = self.request.GET['cancel']
			album_key = ndb.Key(urlsafe=urlstring)
			album_key.delete()
		# Order by recently added
		album = Album.query(Album.album_type == 'match').order(-Album.date)
		template_values = {
			'album_store': album
		}
		template = JINJA_ENVIRONMENT.get_template('match.html')
		self.response.write(template.render(template_values))

class Correlate(webapp2.RequestHandler):
	def get(self):
		if len(self.request.GET) and self.request.GET['cancel']:
			urlstring = self.request.GET['cancel']
			album_key = ndb.Key(urlsafe=urlstring)
			album_key.delete()
		# Order by recently added
		album = Album.query(Album.album_type == 'correlate').order(-Album.date) 
		template_values = {
			'album_store': album
		}
		template = JINJA_ENVIRONMENT.get_template('correlate.html')
		self.response.write(template.render(template_values))

class OddManOut(webapp2.RequestHandler):
	def get(self):
		if len(self.request.GET) and self.request.GET['cancel']:
			urlstring = self.request.GET['cancel']
			album_key = ndb.Key(urlsafe=urlstring)
			album_key.delete()
		# Order by recently added
		album = Album.query(Album.album_type == 'oddmanout').order(-Album.date)
		template_values = {
			'album_store': album
		}
		template = JINJA_ENVIRONMENT.get_template('oddmanout.html')
		self.response.write(template.render(template_values))

class Create(webapp2.RequestHandler):
	def get(self):
		album = ""
		edit = 0
		# Check whether we're creating a album or a Question
		if self.request.GET['album'] == '1':
			questions = ""
			retrieve = 0
			# If coming back from cancelling /question
			if self.request.GET.get('cancel'):
				urlstring = self.request.GET['cancel']
				album_key = ndb.Key(urlsafe=urlstring)
				album = album_key.get()
				questions = Question.query(ancestor=album_key).order(-Question.date).fetch()
				retrieve = 1
			else:
				album = Album(album_type=self.request.GET.get('type'))
				album.album_id = album.put().id()
				album.put()
				self.response.write(str(album.album_id))
			template_values = {
				'album': album,
				'album_type': album.album_type,
				'questions': questions,
				'edit': edit,
				'retrieve': retrieve
			}
			template = JINJA_ENVIRONMENT.get_template('create.html')
			time.sleep(0.2)
			self.response.write(template.render(template_values))
		else:
			# Create a new Question with edit = 0 to indicate new entry
			urlstring = self.request.GET['id']
			album_key = ndb.Key(urlsafe=urlstring)
			album = album_key.get()
			template_values = {
				'album': album,
				'album_type': album.album_type,
				'edit': edit
			}
			template = JINJA_ENVIRONMENT.get_template('question.html')
			self.response.write(template.render(template_values))

class Edit(webapp2.RequestHandler):
	def get(self):	
		urlstring = ""
		edit = 1
		retrieve = 0
		if self.request.GET.get('album') == '1':
			# If coming back from cancelling in /question
			if self.request.GET.get('cancel'):
				urlstring = self.request.GET['cancel']
				retrieve = 1
			else:
				urlstring = self.request.GET['id']
			# Load create but now as an edit page (edit = 1)
			album_key = ndb.Key(urlsafe=urlstring)
			album = album_key.get()
			questions = Question.query(ancestor=album_key).order(-Question.date).fetch()
			template_values = {
				'album': album,
				'album_type': album.album_type,
				'questions': questions,
				'edit': edit,
				'retrieve': retrieve
			}
			template = JINJA_ENVIRONMENT.get_template('create.html')
			self.response.write(template.render(template_values))
		else:
			urlstring = self.request.GET['id']
			question_key = ndb.Key(urlsafe=urlstring)
			question = question_key.get()
			album = question_key.parent().get()
			template_values = {
				'album': album,
				'album_type': album.album_type,
				'question': question,
				'edit': edit,
				'retrieve': retrieve
			}
			template = JINJA_ENVIRONMENT.get_template('editquestion.html')
			self.response.write(template.render(template_values))

class ImageRequest(webapp2.RequestHandler):
	def get(self):
		question_url = self.request.GET['id']
		question_key = ndb.Key(urlsafe=question_url)
		question = question_key.get()
		image_id = self.request.GET['image_id']
		if question.images:
			self.response.headers['Content-Type'] = "image/jpg"
			self.response.write(question.images[int(image_id)].image)
		else:
			self.error(404)

class GoogleImage(webapp2.RequestHandler):
	def get(self):
		# Grab Image object from datastore
		image_url = self.request.GET['id']
		image_key = ndb.Key(urlsafe=image_url)
		image = image_key.get()
		if image:
			self.response.headers['Content-Type'] = "image/jpg"
			self.response.write(image.image)
		else:
			self.error(404)

class Store(webapp2.RequestHandler):
    def post(self):
		# Grab album from url
		urlstring = self.request.POST['album']
		album_key = ndb.Key(urlsafe=urlstring)
		album = album_key.get()
		# Check whether we're storing a album or a Question
		if self.request.GET['album'] == '1':
			album.title = self.request.POST['albumTitle']
			album.category = self.request.POST['categoryTitle']
			album.put()
			time.sleep(0.1)
			# Save album and redirect to edit if the user clicks on 'Save and continue editing'
			# Else, save album and go back to the main page which lists all albums
			if self.request.POST.get('stay') == '1':
				self.redirect('/edit?album=1&amp;id='+urlstring)
			else:
				if album.album_type == 'match':
					self.redirect('/match')
				elif album.album_type == 'correlate':
					self.redirect('/correlate')
				else:
					self.redirect('/oddmanout')
		else:
			# Create Question with the album as parent for strong consistency
			question = ""
			new = "1"
			if self.request.POST['question'] == "":
				question = Question(parent=album_key)
				question.question_id = question.put().id()
			else:
				new = "0"
				question_url = self.request.POST['question']
				question_key = ndb.Key(urlsafe=question_url)
				question = question_key.get()
			question.title = self.request.get('title')
			question.fact = self.request.get('fact')
			question.effect = self.request.get('revealEffect')
			question.difficulty = self.request.get('difficulty')
			# Create answer choices
			answer = int(self.request.get('correct_answer'))
			input_images = self.request.get('image', allow_multiple=True)
			num_images = 4
			if album.album_type == 'correlate':
				num_images = 5
			image_list = []
			for i in range(num_images):
				img = ""
				input_img = input_images[i]
				# If old retrieve the Image
				if new == "0":
					img = question.images[i]
				else:
					img = Image()
				# Resize image
				if input_img:
					op_img = images.Image(input_img)
					op_img.resize(width=256, height=256, crop_to_fit=True)
					result_img = op_img.execute_transforms(output_encoding=images.JPEG)
					img.image = result_img
				# Set the title and correct fields
				if answer == i:
					img.title = "correct_answer_"+str(i)
					img.correct = True
				else:
					img.title = "incorrect_answer_"+str(i)
					img.correct = False
			 	# If old Question, free up the old Image and put in new Image 
				if new == "0":
					question.images.pop(i)
					question.images.insert(i, img)
				else:
					question.images.append(img)

			question.put()
			# Query all Question(s) for the album in recently added order for /create
			# Retrieve previously input values, and indicate whether this is a new album (edit)
			questions = Question.query(ancestor=album_key).order(-Question.date).fetch()
			retrieve = 1
			edit = self.request.GET['edit']
			template_values = {
				'album': album,
				'album_type': album.album_type,
				'questions': questions,
				'edit': edit,
				'retrieve': retrieve
			}
			template = JINJA_ENVIRONMENT.get_template('create.html')
			self.response.write(template.render(template_values))

class Delete(webapp2.RequestHandler):
	def get(self):
		# Delete the album/question by id
		# TODO Support multiple row deletions
		if self.request.GET['album'] == '0':
			question_url = self.request.GET['id']
			question_key = ndb.Key(urlsafe=question_url)
			question_key.delete()
		else:
			album_url = self.request.GET['id']
			album_key = ndb.Key(urlsafe=album_url)
			questions = Question.query(ancestor=album_key).order(-Question.date).fetch()
			for question in questions:
				question.key.delete()
			album_key.delete()

app = webapp2.WSGIApplication([('/', Home),
								('/auth', Auth),
								('/admin', Admin),
								('/match', Match),
								('/correlate', Correlate),
								('/oddmanout', OddManOut),
								('/create', Create),
								('/edit', Edit),
								('/upload', Store),
								('/delete', Delete),
								('/getimage', ImageRequest),
								('/getgimage', GoogleImage)],
								debug=False)

