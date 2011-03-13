import tornado

from handlers import BaseHandler

class HomeHandler(BaseHandler):
    
    def get(self):
        
        
        
        
        self.render('home.html')
    
    def post(self):
        ''' Pascal, please work here '''
        pass