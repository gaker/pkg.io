
import base64
import httplib
import tornado.web

try:
    import cPickle as pickle
except ImportError:
    import pickle

class BaseHandler(tornado.web.RequestHandler):
    
    def head(self):
        ''' Why not allow HEAD requests '''
        return self.get()
    
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

