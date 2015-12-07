import webapp2


import os
import time
import jinja2

from google.appengine.ext import ndb

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

		game = Game.query().order(-Game.date) # Order by recently added
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

		game = Game.query().order(-Game.date) # Order by recently added
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

		game = Game.query().order(-Game.date) # Order by recently added
		template_values = {
			'game_store': game
		}
		template = JINJA_ENVIRONMENT.get_template('oddmanout.html')
		self.response.write(template.render(template_values))

class Create(webapp2.RequestHandler):
	def get(self):
		game = ""
		edit = 0
		if self.request.GET['game'] == '1':
			questions = ""
			retrieve = 0
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
		retrieve = 0
		urlstring = ""
		if self.request.GET.get('cancel'):
			urlstring = self.request.GET['cancel']
			retrieve = 1
		else:
			urlstring = self.request.GET['id']

		game_key = ndb.Key(urlsafe=urlstring)
		game = game_key.get()

		questions = Question.query(ancestor=game_key).order(-Question.date).fetch()
		edit = 1

		template_values = {
			'game': game,
			'questions': questions,
			'edit': edit,
			'retrieve': retrieve
		}
		template = JINJA_ENVIRONMENT.get_template('create.html')
		self.response.write(template.render(template_values))

class Store(webapp2.RequestHandler):
    def post(self):
		# Grab Game from url
		urlstring = self.request.POST['game']
		game_key = ndb.Key(urlsafe=urlstring)
		game = game_key.get()

		if self.request.GET['game'] == '1':
			# Set its title and category from form in /question
			game.title = self.request.POST['gameTitle']
			game.category = self.request.POST['categoryTitle']
			game.put()
			time.sleep(0.1)
			self.redirect('/match')
		else:
			# Create Question with the Game as parent for strong consistency
			question = Question(title=self.request.get('question'), parent=game_key)
			title = self.request.get('question')
			answer = self.request.get('correct_answer')
			images = self.request.get('image', allow_multiple=True)
			image_list = []
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
			self.redirect('/edit?id='+urlstring)

app = webapp2.WSGIApplication([('/', Home),
								('/admin', Admin),
								('/match', Match),
								('/correlate', Correlate),
								('/oddmanout', OddManOut),
								('/create', Create), # TODO Incorporate creating Question
								('/edit', Edit),
								('/upload', Store)], # TODO Incorporate storing Question
								debug=False)