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
    	game = Game()
    	title = self.request.get('game')
    	question = Question()
    	image_list = []

    	for i in range(4):
    		img = Image()
    		img.image = self.request.get('img_'+str(i))
    		if self.request.get("correct_answer_"+str(i)):
    			img.title = "correct_answer_"+str(i)
    			img.correct = True
    		else:
    			img.title = "incorrect_answer_"+str(i)
    			img.correct = False
    		image_list.append(img)
		question.title = title
		question.images = image_list
		game.title = title
		game.questions.append(question)
		game.put()

		# self.response.out.write("key1: "+str(img1_key.id())+" title: "+img1.title+" correct? "+self.request.get("correct_answer_1"))
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
		# TODO: Eventually query the list of Games, and their Questions to dynamically populate page

		# TODO: Query and pass in the Game, which has a list of Questions, which has a list of Images
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