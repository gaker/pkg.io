

class PackageBuilder(object):
    
    version = 1.0
    
    settings = {}
    components = {}
    
    def __init__(self, settings):
        self.settings = settings
    
    def add_component(self, name, settings):
        self.components[name] = settings
    
    
    # ----------------------- This really needs work :P ------------------------
    
    def validate_settings(self):
        errors = {
            'count': 0,
            'messages': {}
        };
        
        for key, value in self.settings.iteritems():
            errors['messages'][key] = [];
            
            if value is None:
                errors['messages'][key].append('%s is a required field' % key)
                errors['count'] = errors['count'] + 1
            
            if key is 'package_name' or key is 'author':
                print 'todo'
                # check chars
            elif key is 'package_short_name':
                print 'todo'
                # check chars
            elif key is 'version':
                print 'todo'
                # check version string
            elif key is 'author_url' or key is 'docs_url':
                print 'todo'
                # check valid url
        
        self.errors = errors
        
        if errors['count']:
            return False
        
        return True
    
    def get_errors():
        return self.errors;