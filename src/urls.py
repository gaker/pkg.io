# from handlers.error import ErrorHandler
from handlers.package import PackageHandler
from handlers.package import GetPackageHandler

from handlers import BaseHandler

url_list = [
    (r'/', PackageHandler),
    (r'/get_package/([a-zA-Z0-9-]+)/?', GetPackageHandler),
    (r'/.*/?', BaseHandler)
]