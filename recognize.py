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
    	# urlstring = 
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
		

class DisplayGame(webapp2.RequestHandler):
	def get(self):
		# TODO: Examine particular id of the game, and retrieve the Game
		# game = Game.query().order(-Game.date) # Order by recently added
		# template_values = {	
		# 	'game_store': game
		# }
		# template = JINJA_ENVIRONMENT.get_template('create.html')
		self.response.write("id: "+self.request.GET['id'])
		# self.response.write(template.render(template_values))

class CreateGame(webapp2.RequestHandler):
	def get(self):
		game = ""
		new = 1
	
		if self.request.GET.get('new'):
			game = Game()
			game.put()
		elif len(self.request.GET) and 'cancel' in self.request.GET:
			urlstring = self.request.GET['cancel']
			game_key = ndb.Key(urlsafe=urlstring)
			game = game_key.get()
			new = 0
			# self.response.write("hello")

		template_values = {
			'game': game,
			'new': new
		}

		template = JINJA_ENVIRONMENT.get_template('create.html')
		self.response.write(template.render(template_values))

class EditGame(webapp2.RequestHandler):
	def get(self):
		urlstring = self.request.GET['id']
		# self.response.write('id: '+urlstring)
		game_key = ndb.Key(urlsafe=urlstring)
		game = game_key.get()

		questions = Question.query(ancestor=game_key).order(-Question.date).fetch()
		# self.response.write("question: "+str(questions))
		template_values = {
			'game': game,
			'questions': questions
		}
		template = JINJA_ENVIRONMENT.get_template('create.html')
		self.response.write(template.render(template_values))

class CreateQuestion(webapp2.RequestHandler):
	def get(self):
		# TODO Need to acquire game passed from Match
		# game = Game.query().order(-Game.date) # Order by recently added
		# for g in game:
		# 	self.response.write("recent game: "+str(g))
		# game = ""
		urlstring = self.request.GET['id']
		# if urlstring:
		game_key = ndb.Key(urlsafe=urlstring)
		game = game_key.get()

		template_values = {	
			'game': game
		}
		template = JINJA_ENVIRONMENT.get_template('question.html')
		self.response.write(template.render(template_values))

class StoreQuestion(webapp2.RequestHandler):
	def post(self):
		urlstring = self.request.POST['game']
		game_key = ndb.Key(urlsafe=urlstring)
		game = game_key.get()

		question = Question(title=self.request.get('question'), parent=game_key)
		title = self.request.get('question')
		answer = self.request.get('correct_answer')
		images = self.request.get('image', allow_multiple=True)
		image_list = []
		# self.response.out.write("title: "+game.title+" question: "+question.title+"\nanswers: "+str(answer) 
		#	+ " images: "+str(len(images)))
		for i in range(1):
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
		self.redirect('/edit?id='+urlstring)

class StoreGame(webapp2.RequestHandler):
    def post(self):
		""" TODO 
		"""
		urlstring = self.request.POST['game']
		game_key = ndb.Key(urlsafe=urlstring)
		game = game_key.get()
		game.title = self.request.POST['gameTitle']
		game.category = self.request.POST['categoryTitle']
		game.put()

		# time.sleep(0.1)
		self.redirect('/match')

app = webapp2.WSGIApplication([('/upload', StoreGame),
							   ('/uploadq', StoreQuestion),
							   ('/match', MainPage),
							   ('/match/view', DisplayGame), # TODO: Combine Display and Create
							   ('/create', CreateGame),
							   ('/edit', EditGame),
							   ('/question', CreateQuestion)],
								debug=True)

# TODO: A tidier implementation once above is working for /match
# app = webapp2.WSGIApplication([('/upload', StoreGame),
# 							   ('/match', MainPage),
#    						   ('/correlate', MainPage),
# 							   ('/oddmanout', MainPage),
# 							   ('/view', DisplayGame), # TODO: Combine Display and Create
# 							   ('/create', CreateGame),
# 							   ('/question', CreateQuestion)],
# 								debug=True)