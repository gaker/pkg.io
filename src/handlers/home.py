import os.path
import tornado
import uuid

from handlers import BaseHandler
from lib.builder import PackageBuilder
from lib.validate import FormValidator
from zipfile import ZipFile, ZipInfo

class HomeHandler(BaseHandler):
    
    def get(self):
        self.render('home.html', form_error=self.blank_callback,
                                 set_value=self.blank_callback)
    
    def post(self):
        ''' This is a productive method.'''
        
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
        
        
        accessory_sections = 0
        
        if form.get_field('pkg_accessory'):
            form.add_field('accessory_sections_num')
            value = form.get_field('accessory_sections_num')
            
            if value.isdigit() and 0 < int(value) < 4:
                accessory_sections = int(value)
                
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
        
        template_path = os.path.join(self.get_template_path(), 'addon_templates/')
        template_defaults = {
            'author': form.get_field('author'),
            'author_url': form.get_field('author_url'),
            'docs_url': form.get_field('docs_url'),
            'package_name': form.get_field('package_name'),
            'package_short_name': form.get_field('package_short_name'),
            'version': form.get_field('version'),
            
            'ucfirst': unicode.capitalize,
            'dequote': lambda s: s.replace("'", "\\'")
        }
        
        templates = {
            'accessory': 'accessory/acc.{package}.php',
            'plugin': 'plugin/pi.{package}.php',
            'mcp': 'module/mcp.{package}.php',
            'mod': 'module/mod.{package}.php',
            'upd': 'module/upd.{package}.php',
            'view': 'views/{view}.php'
        }
        
        build = PackageBuilder(short_name)
        build.seed_loader(template_path, templates)
        build.seed_namespace(template_defaults)
        
        # Build accessory
        if form.get_field('pkg_accessory'):
            
            sections = []
            for k in xrange(1, accessory_sections + 1):
                sections.append({
                    'title':  form.get_field('accessory_%d_title' % k),
                    'content': form.get_field('accessory_%d_content' % k)
                })
            
            build.add_accessory({
                'description': "TODO: Ask for a description.",
                'sections': sections
            })

        # Build plugin
        if form.get_field('pkg_plugin'):
            build.add_plugin({
                'description': "TODO: Ask for a description.",
                'instructions': form.get_field('plugin_instructions')
            })
        
        # Build module
        if form.get_field('pkg_module'):
            select_cp = ['n', 'y']
            has_cp = int(form.get_field('module_has_control_panel'))
            
            build.add_module({
                'has_cp': select_cp[has_cp],
                'module_description': form.get_field('module_description') 
            })
        
        
        # All files must have that first subdirectory in their path
        # so that the archive extracts cleanly with that folder name
        
        zippath = os.path.join(os.path.dirname(__file__), "../../zips/"+str(uuid.uuid4())+".zip")
        zippath = os.path.normpath(zippath)
        
        # Zip 'er up!
        download = ZipFile(zippath, 'w')
        
        for i in build.get_files():
            download.writestr(short_name+'/'+i[0], i[1])
        
        download.close()
        return
    
    
    # Utility functions
    
    def blank_callback(*args, **kwargs):
        return ''
    
    def error_function(self, errors=False):
        def show_error(fieldname, template):
            if fieldname in errors:
                return template.format(error=errors[fieldname])
            return ''
        return show_error