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
		retrieve = 0 
		urlstring = ""
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
		# Check whether we're storing a Game or a Question
		if self.request.GET['game'] == '1':
			game.title = self.request.POST['gameTitle']
			game.category = self.request.POST['categoryTitle']
			game.put()
			time.sleep(0.1)
			# Save game and redirect to edit if the user clicks on 'Save and continue editing'
			# Else, save game and go back to the main page which lists all Games
			if self.request.POST.get('stay') == '1':
				self.redirect('/edit?id='+urlstring)
			else:
				self.redirect('/match')
		else:
			# Create Question with the Game as parent for strong consistency
			question = Question(title=self.request.get('question'), fact=self.request.get('fact'), parent=game_key)
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