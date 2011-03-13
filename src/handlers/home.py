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
        
        
        if form.get_field('pkg_accessory'):
            form.add_field('accessory_sections_num')
            value = form.get_field('accessory_sections_num')
            
            if value.isdigit() and 0 < int(value) < 4:
                for k in xrange(1, int(value) + 1):
                    form.add_field('accessory_%d_title' % k)
                    form.add_field('accessory_%d_content' % k)
        
        if form.get_field('pkg_plugin'):
            form.add_field('plugin_instructions')
        
        if form.get_field('pkg_module'):
            form.add_field('module_has_control_panel', '', '0')
            form.add_field('module_description', 'required')
        
        if form.get_field('pkg_extension'):
            form.add_field('extension_has_settings', '', 0)
        
        errors = form.validate()
        
        if errors is not True:
            self.render('home.html', form_error=self.error_function(errors),
                                     set_value=form.get_field)
            return
        
        # WOOT building time
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