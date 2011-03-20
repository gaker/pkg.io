from handlers.error import ErrorHandler
from handlers.home import HomeHandler

# from handlers import BaseHandler

url_list = [
    (r'/', HomeHandler),
    (r'/.*/?', ErrorHandler)
]