import tornado

from handlers import BaseHandler
from lib.builder import PackageBuilder

class HomeHandler(BaseHandler):
    
    def get(self):
        
        
        
        
        self.render('home.html')
    
    def post(self):
        ''' Pascal hath been here '''
        
        params = {
            'author': None,
            'author_url': '',
            'docs_url': '',
            'package_name': None,
            'package_short_name': None,
            'version': '1.0',
        }
        
        settings = dict((x, self.get_argument(x, deft)) for x, deft in params.iteritems())
        
        builder = PackageBuilder(settings)
        
        if not builder.validate_settings():
            print builder.get_errors()
            return
        
        # grab components
        # add to package builder
        # validate
        
        # build, build, build!
        
        
        pass