import webapp2

import os
import time
import jinja2

from models import Album
from models import Image

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ImageStore(webapp2.RequestHandler):
    def post(self):
		img1 = Image()
		img1.image = self.request.get('img_1')
		img1.category = self.request.get('game')
		if self.request.get("correct_answer_1"): #TODO make this process a loop
			img1.title = "correct_answer_1"
			img1.correct = True
		else:
			img1.title = "incorrect_answer_1"
			img1.correct = False

		img2 = Image()
		img2.image = self.request.get('img_2')
		img2.category = self.request.get('game')
		if self.request.get("correct_answer_2"):
			img2.title = "correct_answer_2"
			img2.correct = True
		else:
			img2.title = "incorrect_answer_2"
			img2.correct = False

		# img3 = Image(image=self.request.get('img_3'), title=self.request.title)
		# album = Album(title="Cats", images=[img1, img2, img3])
		# album.put()
		# album.put()
		img1_key = img1.put()
		img2_key = img2.put()
		# img3.put()
		# self.response.out.write("key1: "+str(img1_key.id())+" title: "+img1.title+" correct? "+self.request.get("correct_answer_1")+
		# 						"\nkey2: "+str(img2_key.id())+" title: "+img2.title+" correct? "+self.request.get("correct_answer_2"))
		time.sleep(0.1)
		self.redirect('/match')

class MainPage(webapp2.RequestHandler):
    def get(self):
    	# TODO: Eventually query the list of Games, and their Albums to dynamically populate page

    	image = Image.query().order(-Image.date) # Order by recently added

    	# self.response.write(image2.title)
    	template_values = {	
    		'image_store': image
        }
        template = JINJA_ENVIRONMENT.get_template('match.html')
      	self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([('/upload', ImageStore), 
							   ('/match', MainPage)],
								debug=True)