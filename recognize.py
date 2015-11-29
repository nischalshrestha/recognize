import webapp2

import os
import time
import jinja2

from models import Game
from models import Question
from models import Image

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ImageStore(webapp2.RequestHandler):
    def post(self):
    	game = Game(title=self.request.get('game'))
    	question = Question(title=self.request.get('question'))
    	answer = self.request.POST.get('correct_answer')
    	images = self.request.get('image', allow_multiple=True)
    	image_list = []
    	question_list = []
    	# self.response.out.write("title: "+game.title+" question: "+question.title+"\nanswers: "+str(answer)
    	# 	+ " images: "+str(len(images)))
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

		# TODO: ancestor query for Game since we can't have repeated Question(s)
		game.questions = question
		game.put()

		# TODO: redirect to create i.e. redirect back to /create to refresh that page with the newly created 
		# game with its titles, and list of questions 

		time.sleep(0.1)
		self.redirect('/match')

class DisplayGame(webapp2.RequestHandler):
	def get(self):
		# TODO: Eventually query the list of Games, and their Questions to dynamically populate page
		# image = Image.query().order(-Image.date) # Order by recently added
		# template_values = {	
		# 	'image_store': image
		# }
		# template = JINJA_ENVIRONMENT.get_template('match.html')
		self.response.write("id: "+self.request.GET['id'])

class CreateGame(webapp2.RequestHandler):
	def get(self):
		# TODO: Query and pass in the Game, which has a list of Questions, which has a list of Images
		# TODO: Need to look at the particular id of the game
		game = Game.query().order(-Game.date) # Order by recently added
		template_values = {	
			'game_store': game
		}
		template = JINJA_ENVIRONMENT.get_template('create.html')
		# self.response.write("id: "+self.request.GET['id'])
		self.response.write(template.render(template_values))


class MainPage(webapp2.RequestHandler):
    def get(self):
    	# TODO: Eventually query the list of Games, and their Questions to dynamically populate page
    	game = Game.query().order(-Game.date) # Order by recently added
    	template_values = {	
    		'game_store': game
        }
        template = JINJA_ENVIRONMENT.get_template('match.html')
      	self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([('/upload', ImageStore),
							   ('/match', MainPage),
							   ('/match/view', DisplayGame), # TODO: Combine Display and Create
							   ('/create', CreateGame)],
								debug=True)