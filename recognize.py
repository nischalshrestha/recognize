import webapp2

from models import Album
from models import Image

# class MainPage(webapp2.RequestHandler):
#     def get(self):
#         self.response.headers['Content-Type'] = 'text/plain'
#         self.response.write('Hello, World!')

class Guestbook(webapp2.RequestHandler):
    def post(self):
		img1 = Image(image=self.request.get('img_1'))
		img2 = Image(image=self.request.get('img_2'))
		img3 = Image(image=self.request.get('img_3'))
		album = Album(title="Cats", images=[img1, img2, img3])
		# album.put()
		album.put()
		self.redirect(self.request.referer)

app = webapp2.WSGIApplication([('/upload', Guestbook)],
                              debug=True)