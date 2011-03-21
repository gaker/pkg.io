import urls

import os

import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.locale 
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)
define("debug", default=True, help="run tornado in debug mode", type=bool)

BASEPATH = os.path.abspath(os.path.dirname(__file__))

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            xheaders=True,
            xsrf_cookie=True,
            debug=options.debug,
            template_path=os.path.join(BASEPATH, 'templates'),
            static_path=os.path.join(BASEPATH, 'static'),
            cookie_secret="$@(*YFDKHjdsaf afslkajhsdfghkasjdgtais)/Vo=",
            login_url="/auth/login",
        )
        tornado.web.Application.__init__(self, urls.url_list, **settings)

def main():
    tornado.options.parse_command_line()
    tornado.locale.load_gettext_translations(
            os.path.join(os.path.dirname(__file__), "locale"), 'global')
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
