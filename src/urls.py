# from handlers.error import ErrorHandler
from handlers.package import PackageHandler
from handlers.package import GetPackageHandler

from handlers import BaseHandler

url_list = [
    (r'/', PackageHandler),
    (r'/get_package/', GetPackageHandler),
    (r'/.*/?', BaseHandler)
]