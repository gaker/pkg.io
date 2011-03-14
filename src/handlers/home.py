import os.path
import tornado
import uuid

from handlers import BaseHandler
from lib.parser import Parser
from lib.validate import FormValidator
from zipfile import ZipFile, ZipInfo

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
            print errors
            self.render('home.html', form_error=self.error_function(errors),
                                     set_value=form.get_field)
            return
        
        
        # WOOT start building
        
        files = []
        short_name = form.get_field('package_short_name')
        
        p = Parser()
        
        
        parser_templates = os.path.join(self.get_template_path(), 'addon_templates/')
        parser_defaults = {
            'author': form.get_field('author'),
            'author_url': form.get_field('author_url'),
            'docs_url': form.get_field('docs_url'),
            'package_name': form.get_field('package_name'),
            'package_short_name': form.get_field('package_short_name'),
            'version': form.get_field('version')
        }
        
        if form.get_field('pkg_accessory'):        
            args = parser_defaults
            args.update({
                'accessory_description': "I be describing",
                'sections': []
            })
            
            p.set_package_type('accessory')
            p.set_template(os.path.join(parser_templates, 'accessory/acc.package.php'))
            files.append( ['acc.'+short_name+'.php', p.parse(args)] )
        
                
        # All files must have that first subdirectory in their path
        # so that the archive extracts cleanly with that name
        
        zippath = os.path.join(os.path.dirname(__file__), "../../zips/"+str(uuid.uuid4())+".zip")
        zippath = os.path.normpath(zippath)
        
        # Zip 'er up!
        download = ZipFile(zippath, 'w')
        
        for i in files:
            download.writestr(short_name+'/'+i[0], i[1])
        
        download.close()
                
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