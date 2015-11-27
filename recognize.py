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
    	album = Question()

    	for i in range(4):
    		img = Image()
    		img.image = self.request.get('img_'+str(i))
    		if self.request.get("correct_answer_"+str(i)):
    			img.title = "correct_answer_"+str(i)
    			img.correct = True
    		else:
    			img.title = "incorrect_answer_"+str(i)
    			img.correct = False
    		img.put()

		# self.response.out.write("key1: "+str(img1_key.id())+" title: "+img1.title+" correct? "+self.request.get("correct_answer_1"))
		time.sleep(0.1)
		self.redirect('/match')

class MainPage(webapp2.RequestHandler):
    def get(self):
    	# TODO: Eventually query the list of Games, and their Questions to dynamically populate page

    	image = Image.query().order(-Image.date) # Order by recently added

    	template_values = {	
    		'image_store': image
        }
        template = JINJA_ENVIRONMENT.get_template('match.html')
      	self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([('/upload', ImageStore), 
							   ('/match', MainPage)],
								debug=True)