import webapp2

import os
import time
import jinja2

from google.appengine.ext import ndb
# from google.appengine.api import images
# from google.appengine.ext import blobstore

from models import Game
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

class Admin(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('admin.html')
		self.response.write(template.render(template_values))

class Match(webapp2.RequestHandler):
	def get(self):
		if len(self.request.GET) and self.request.GET['cancel']:
			urlstring = self.request.GET['cancel']
			game_key = ndb.Key(urlsafe=urlstring)
			game_key.delete()
		# Order by recently added
		game = Game.query().order(-Game.date)
		template_values = {
			'game_store': game
		}
		template = JINJA_ENVIRONMENT.get_template('match.html')
		self.response.write(template.render(template_values))

class Correlate(webapp2.RequestHandler):
	def get(self):
		if len(self.request.GET) and self.request.GET['cancel']:
			urlstring = self.request.GET['cancel']
			game_key = ndb.Key(urlsafe=urlstring)
			game_key.delete()
		# Order by recently added
		game = Game.query().order(-Game.date) 
		template_values = {
			'game_store': game
		}
		template = JINJA_ENVIRONMENT.get_template('correlate.html')
		self.response.write(template.render(template_values))

class OddManOut(webapp2.RequestHandler):
	def get(self):
		if len(self.request.GET) and self.request.GET['cancel']:
			urlstring = self.request.GET['cancel']
			game_key = ndb.Key(urlsafe=urlstring)
			game_key.delete()
		# Order by recently added
		game = Game.query().order(-Game.date)
		template_values = {
			'game_store': game
		}
		template = JINJA_ENVIRONMENT.get_template('oddmanout.html')
		self.response.write(template.render(template_values))

class Create(webapp2.RequestHandler):
	def get(self):
		game = ""
		edit = 0
		# Check whether we're creating a Game or a Question
		if self.request.GET['game'] == '1':
			questions = ""
			retrieve = 0
			# If coming back from cancelling /question
			if self.request.GET.get('cancel'):
				urlstring = self.request.GET['cancel']
				game_key = ndb.Key(urlsafe=urlstring)
				game = game_key.get()
				questions = Question.query(ancestor=game_key).order(-Question.date).fetch()
				retrieve = 1
			else:
				game = Game()
				game.put()
			template_values = {
				'game': game,
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
			if len(self.request.GET) and 'edit' in self.request.GET:
				edit = self.request.GET['edit']
			game_key = ndb.Key(urlsafe=urlstring)
			game = game_key.get()
			template_values = {
				'game': game,
				'edit': edit
			}
			template = JINJA_ENVIRONMENT.get_template('question.html')
			self.response.write(template.render(template_values))

class Edit(webapp2.RequestHandler):
	def get(self):	
		urlstring = ""
		edit = 1
		retrieve = 0
		if self.request.GET.get('game') == '1':
			# If coming back from cancelling in /question
			if self.request.GET.get('cancel'):
				urlstring = self.request.GET['cancel']
				retrieve = 1
			else:
				urlstring = self.request.GET['id']
			# Load create but now as an edit page (edit = 1)
			game_key = ndb.Key(urlsafe=urlstring)
			game = game_key.get()
			questions = Question.query(ancestor=game_key).order(-Question.date).fetch()
			template_values = {
				'game': game,
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
			game = question_key.parent().get()
			template_values = {
				'game': game,
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
			self.response.headers['Content-Type'] = "image/png"
			self.response.write(question.images[int(image_id)].image)
		else:
			self.error(404)

class Store(webapp2.RequestHandler):
    def post(self):
		# Grab Game from url
		urlstring = self.request.POST['game']
		game_key = ndb.Key(urlsafe=urlstring)
		game = game_key.get()
		# Check whether we're storing a Game or a Question
		if self.request.GET['game'] == '1':
			game.title = self.request.POST['gameTitle']
			game.category = self.request.POST['categoryTitle']
			game.put()
			time.sleep(0.1)
			# Save game and redirect to edit if the user clicks on 'Save and continue editing'
			# Else, save game and go back to the main page which lists all Games
			if self.request.POST.get('stay') == '1':
				self.redirect('/edit?game=1&amp;id='+urlstring)
			else:
				self.redirect('/match')
		else:
			# TODO: Add logic to handle modifying an existing game
			# Create Question with the Game as parent for strong consistency
			question = Question(title=self.request.get('question'), fact=self.request.get('fact'), parent=game_key)
			title = self.request.get('question')
			answer = self.request.get('correct_answer')
			images = self.request.get('image', allow_multiple=True)
			for i in range(4):
				img = Image()
				img.image = images[i]
				if int(answer) == i:
					img.title = "correct_answer_"+str(i)
					img.correct = True
				else:
					img.title = "incorrect_answer_"+str(i)
					img.correct = False
				question.images.append(img)			
			question.put()
			# Query all Question(s) for the Game in recently added order for /create
			# Retrieve previously input values, and indicate whether this is a new game (edit)
			questions = Question.query(ancestor=game_key).order(-Question.date).fetch()
			retrieve = 1
			edit = 0
			if len(self.request.GET) and 'edit' in self.request.GET:
				edit = self.request.GET['edit']
			template_values = {
				'game': game,
				'questions': questions,
				'edit': edit,
				'retrieve': retrieve
			}
			template = JINJA_ENVIRONMENT.get_template('create.html')
			self.response.write(template.render(template_values))

class Delete(webapp2.RequestHandler):
	def get(self):
		# Delete the game/question by id
		# TODO Support multiple row deletions
		if 'id' in self.request.GET:
			urlstring = self.request.GET['id']
			entity_key = ndb.Key(urlsafe=urlstring)
			entity_key.delete()

app = webapp2.WSGIApplication([('/', Home),
								('/admin', Admin),
								('/match', Match),
								('/correlate', Correlate),
								('/oddmanout', OddManOut),
								('/create', Create),
								('/edit', Edit),
								('/upload', Store),
								('/delete', Delete),
								('/getimage', ImageRequest)],
								debug=False)

