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

class MainPage(webapp2.RequestHandler):
    def get(self):
    	# TODO: Determine the content based on the page: match, correlate, or oddmanout
    	# Currently: Determines the content based on just match
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

class CreateGame(webapp2.RequestHandler):
	def get(self):
		game = ""
		questions = ""
		retrieve = 0
		edit = 0

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

class EditGame(webapp2.RequestHandler):
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

class CreateQuestion(webapp2.RequestHandler):
	def get(self):
		edit = ""
		urlstring = self.request.GET['id']
		if len(self.request.GET) and 'edit' in self.request.GET:
			edit = self.request.GET['edit']

		# if urlstring:
		game_key = ndb.Key(urlsafe=urlstring)
		game = game_key.get()

		template_values = {
			'game': game,
			'edit': edit
		}

		template = JINJA_ENVIRONMENT.get_template('question.html')
		self.response.write(template.render(template_values))

class StoreQuestion(webapp2.RequestHandler):
	def post(self):
		# Obtain Game from url
		urlstring = self.request.POST['game']
		game_key = ndb.Key(urlsafe=urlstring)
		game = game_key.get()
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
		# self.redirect('/edit?id='+urlstring)

class StoreGame(webapp2.RequestHandler):
    def post(self):
		# Grab Game from url
		urlstring = self.request.POST['game']
		game_key = ndb.Key(urlsafe=urlstring)
		game = game_key.get()
		# Set its title and category from form in /question
		game.title = self.request.POST['gameTitle']
		game.category = self.request.POST['categoryTitle']
		game.put()

		time.sleep(0.1)
		self.redirect('/match')

app = webapp2.WSGIApplication([('/upload', StoreGame),
							   ('/uploadq', StoreQuestion),
							   ('/match', MainPage),
							   ('/create', CreateGame),
							   ('/edit', EditGame),
							   ('/question', CreateQuestion)],
								debug=False)

# TODO: A tidier implementation once above is working for /match
# app = webapp2.WSGIApplication([('/upload', StoreGame),
# 							   ('/match', MainPage),
#    						   ('/correlate', MainPage),
# 							   ('/oddmanout', MainPage),
# 							   ('/view', DisplayGame), # TODO: Combine Display and Create
# 							   ('/create', CreateGame),
# 							   ('/question', CreateQuestion)],
# 								debug=True)