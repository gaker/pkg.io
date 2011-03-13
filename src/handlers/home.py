import tornado

from handlers import BaseHandler
from lib.validate import FormValidator

class HomeHandler(BaseHandler):
    
    def get(self):
        
        
        
        
        self.render('home.html', form_error=self.blank_callback,
                                 set_value=self.blank_callback)
    
    def post(self):
        ''' Pascal hath been here '''
        
        
        form = FormValidator(self)
        
        form.add_field('author', 'required|plain_string');
        form.add_field('author_url', 'url');
        form.add_field('docs_url', 'url');
        form.add_field('package_name', 'required|plain_string');
        form.add_field('package_short_name', 'required|segment');
        form.add_field('version', 'float', '1.0');
        
        errors = form.validate()
        
        if errors is not True:
            self.render('home.html', form_error=self.error_function(errors),
                                     set_value=form.get_field)
            return
        
        print form.fields()
        
        
        # params = {
        #     'author': None,
        #     'author_url': '',
        #     'docs_url': '',
        #     'package_name': None,
        #     'package_short_name': None,
        #     'version': '1.0',
        # }
        # 
        # settings = dict((x, self.get_argument(x, deft)) for x, deft in params.iteritems())
        # 
        # builder = PackageBuilder(settings)
        # 
        # if not builder.validate_settings():
        #     print builder.get_errors()
        #     return
        
        # grab components
        # add to package builder
        # validate
        
        # build, build, build!
        
        
        pass
    
    def blank_callback(*args, **kwargs):
        return ''
    
    def error_function(self, errors=False):
        def show_error(fieldname, template):
            if fieldname in errors:
                return template.format(error=errors[fieldname])
            return ''
        return show_error