import os.path
import re
import unicodedata

from tornado import template

class PackageBuilder:
    """Manage the contents of a package.
    
    Our template files are named after the file they will create,
    such as `acc.package.php` for the accessory template. This way we
    already adherte to the required naming conventions. When we use
    the file we simply need to get rid of package and drop in the short name.
    
    To make this a little more flexible the class is seeded with a
    dict that holds the templates with the placholder name ("package"
    in the above example) wrapped in braces: `acc.{package}.php`
    
    In other words:
    1. Ignore braces themselves: acc.package.php
    2. Grab that file as the template to use
    3. Replace the brace contents with what is required. In this case
       we need the shortname: acc.shortname.php
    4. Parse the template
    5. Save the parsed template acc.shortname.php (*)
    
    * This class does no actual writing or saving (@see get_files()).
    """
    
    def __init__(self, short_name):
        self._files = []
        self.short_name = short_name
    
    def seed_namespace(self, settings):
        self.settings = settings
    
    def seed_loader(self, path, templates):
        self._loader = _Loader(path)
        self._templates = templates

    def get_files(self):
        return self._files

    def add_accessory(self, settings):
        args = self.settings
        args.update(settings)
                
        # first the views - we'll need their titles
        for section in args['sections']:
            title = section['title']
            short_title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore')
            short_title = unicode(re.sub('[^\w\s-]', '', short_title).strip().lower())
            short_title = re.sub('[-\s]+', '_', short_title)
            
            data = {'content': section['content']}
            self._add('view', data, 'accessory_{0}'.format(short_title))
            
            section['short_title'] = short_title
        
        self._add('accessory', args);
        

    def add_extension():
        return
        
    def add_plugin(self, settings):
        args = self.settings
        args.update(settings)
        
        self._add('plugin', args)
        
    def add_module(self, settings):
        args = self.settings
        args.update(settings)
        
        self._add('mcp', args)
        self._add('mod', args)
        self._add('upd', args)
    
    def _add(self, tmpl, args, format='{0}'):
        path = self._templates[tmpl]
        
        fname = re.sub("\{.+?\}", format, path).format(self.short_name)
        path = re.sub("[{}]", '', path)
        
        t = self._loader.load(path)
        self._files.append( [fname, t.generate(**args)] )
    

class _Loader(template.Loader):
    ''' Basically a verbatim copy of the tornado loader's
    load method except for the compress_whitespace flag'''
    
    def load(self, name, parent_path=None):
        name = self.resolve_path(name, parent_path=parent_path)
        if name not in self.templates:
            path = os.path.join(self.root, name)
            f = open(path, "r")
            self.templates[name] = template.Template(f.read(), 
                                                     name=name, loader=self,
                                                     compress_whitespace=False)
            f.close()
        return self.templates[name]