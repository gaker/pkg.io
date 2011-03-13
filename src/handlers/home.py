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
        
        # Basic Settings
        form.add_field('author', 'required|plain_string')
        form.add_field('author_url', 'url')
        form.add_field('docs_url', 'url')
        form.add_field('package_name', 'required|plain_string')
        form.add_field('package_short_name', 'required|segment')
        form.add_field('version', 'float', '1.0')
        
        
        # Components
        form.add_field('pkg_accessory')
        form.add_field('pkg_plugin')
        form.add_field('pkg_module')
        form.add_field('pkg_extension')
        
        
        if form.get_field('pkg_plugin'):
            form.add_field('plugin_instructions')
        
        
        
        errors = form.validate()
        
        if errors is not True:
            self.render('home.html', form_error=self.error_function(errors),
                                     set_value=form.get_field)
            return
        
        print form.fields()
                
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