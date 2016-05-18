from tornado.web import URLSpec as url
from rabbitChat.apps.main.views import IndexHandler

urls = [
    url(r"/", IndexHandler),
]
