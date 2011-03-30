
import base64
import httplib
import tornado.web

try:
    import cPickle as pickle
except ImportError:
    import pickle

    def delist_arguments(args):
        """
        Takes a dictionary, 'args' and de-lists any single-item lists then
        returns the resulting dictionary.

        In other words, {'foo': ['bar']} would become {'foo': 'bar'}

        http://code.activestate.com/recipes/576958-method-based-url-dispatcher-for-the-tornado-web-se/
        """
        for arg, value in args.items():
            if len(value) == 1:
                args[xhtml_escape(arg)] = xhtml_escape(value[0])
        return args

class BaseHandler(tornado.web.RequestHandler):
    
    def _map(self):
        """This function maps """
        args = None
        # Sanitize argument lists:
        if self.request.arguments:
            args = delist_arguments(self.request.arguments)
        
        # ditch the query string as it's in args now
        path = self.request.uri.split('?')[0].split('/')
        path.pop()
        path.pop(0)

        # segment_2 of the URI is the method to call
        try:
            method = path[1]
        except IndexError:
            method = 'index'

        if method.startswith('_'):
            raise tornado.web.HTTPError(404)
        
        func = getattr(self, '%s_action' % method, None)

        if func:
            if args:
                return func(**args)
            else:
                return func()
        else:
            raise tornado.web.HTTPError(404)
    
    def get_argument(self, name, default=False, strip=True):
        """COPYING THEIR DAMN METHOD TO BUGFIX! ARGH!"""
        
        args = self.get_arguments(name, strip=strip)
        if not args:
            if default is False:
                raise HTTPError(404, "Missing argument %s" % name)
            return default
        
        if name[-2:] == '[]':
            return args
        
        return args[-1]
    
    @tornado.web.addslash
    def get(self):
        return self._map()
    
    def post(self):
        return self._map()
        
    def head(self):
        return self._map()
    
    def get_error_html(self, status_code, **kwargs):
        ''' Overrides the parent get_error_html method, which doesn't do too
            much.
            
            As per the method in tornado.web, if there is an uncaught
            exception, it will be in kwargs['exception']
            
            ``Required Template`` 
                error.html
            
            **Context**
            
            ``code``
                Error code reported
            
            ``message``
                Error Message sent
        '''
        context = {
            'code': status_code,
            'message': httplib.responses[status_code]
        }

        return self.render_string('error.html', **context)

    def get_current_user(self):
        ''' Overrides Tornado's default get_current_user method '''
        pass
    
    def get_user_locale(self):
        ''' This needs to be extended for user-configurable
            locale management '''
        return None

    def set_flashdata(self, cookie_name, message):
        """ Sets a flashdata cookie
            
            Tornado gets upset at spaces in the contents of the cookie,
            so it seems reasonable, and quickest to just replace spaces
            with the underscores.
            
            **Parameters:**
            
            ``cookie_name``
                required - name of the cookie to set
            
            ``message``
                required - message string to put in the cookie."""
        
        message = base64.encodestring(pickle.dumps(message))
        self.set_cookie('success_message', message)

    def get_flashdata(self, cookie_name):
        """ Get the flashdata cookie.  Return None if the cookie exists.
            If the cookie does exist, get the contents, kill off the cookie,
            and return the contents of the cookie.
            
            **Parameters:**
            
            ``cookie_name``
                required - name of the cookie to fetch."""

        try:
            message = self.get_cookie(cookie_name, None)
            message = pickle.loads(base64.decodestring(message))
        except:
            message = None

        self.clear_cookie(cookie_name)
        
        return message

