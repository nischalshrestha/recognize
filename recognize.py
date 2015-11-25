import webapp2

import os
import jinja2

from models import Album
from models import Image

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
    	# TODO: Eventually query the list of Games, and their Albums to dynamically populate page
    	# Eg values
    	template_values = {
            'title1': 'Orange Tabbies!',
            'category1': 'Cats',
            'title2': 'German Shepherds!',
            'category2': 'Dogs'
        }
        template = JINJA_ENVIRONMENT.get_template('match.html')
      	self.response.write(template.render(template_values))

class ImageStore(webapp2.RequestHandler):
    def post(self):
		img1 = Image()
		img1.image = self.request.get('img_1')
		if self.request.get("correct_answer_1"):
			img1.title = "correct_answer"
			img1.correct = True
		else:
			img1.title = "incorrect_answer_1"
			img1.correct = False

		# img2 = Image(image=self.request.get('img_2'), title=self.request.title)
		# img3 = Image(image=self.request.get('img_3'), title=self.request.title)
		# album = Album(title="Cats", images=[img1, img2, img3])
		# album.put()
		# album.put()
		img1_key = img1.put()
		# img2.put()
		# img3.put()
		# self.response.out.write("key: "+str(img1_key.id())+" title: "+img1.title+" correct? "+self.request.get("correct_answer_1"))
		self.redirect(self.request.referer)

app = webapp2.WSGIApplication([('/upload', ImageStore), 
							   ('/match', MainPage)],
								debug=True)