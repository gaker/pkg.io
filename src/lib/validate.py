import re

class FormValidator(object):
        
    fields = {}
    field_rules = []
    
    def __init__(self, cls):
        self.fields = {}
        self.field_rules = []
        
        self._validation_rules = False
        self._request_cls = cls
    
    def add_field(self, field_name, rule='', default=''):
        rules = rule.split('|')
        
        # populate
        self.fields[field_name] = self._request_cls.get_argument(field_name, default)
        
        if not rule:
            return
        
        for r in rule.split('|'):
            self.field_rules.append([field_name, r])
    
    def get_field(self, field_name, in_type='text', val=''):
        if not field_name in self.fields:
            return ''

        if in_type is 'text':
            return self.fields[field_name]
        elif in_type is 'check':
            if self.fields[field_name]:
                return 'checked="checked"'
        elif in_type is 'select':
            if self.fields[field_name] == val:
                return 'selected="selected"'        
        return ''
        
    def validate(self):
        
        errors = {}
        
        for ruleset in self.field_rules:
            name = ruleset[0]
            rule = ruleset[1]
            value = self.fields[name]
            
            if name in errors:
                continue
            
            if self.get_validator(rule).match(value) == None:
                errors[name] = self.get_human_error(rule)
        
        if len(errors):
            return errors
        
        return True
    
    def get_validator(self, rule):
        if not self._validation_rules:
            self._validation_rules = {
                'required': re.compile('.+'),
                'float': re.compile('\d+(\.\d+)?'),
                'plain_string': re.compile('[a-zA-Z0-9 _-]'),   # @todo unicode chars?
                'segment': re.compile('[a-z0-9_]+'),            # shortname needs to be a valid url segment, feel free to rename this
                'url': re.compile('\(?http://[-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|]') # hate urls - hate them - no guarantees (source: http://www.codinghorror.com/blog/2008/10/the-problem-with-urls.html)
            }
            
        return self._validation_rules[rule]
    
    def get_human_error(self, rule):
        errors = {
            'required': u'Required Field',
            'float': u'Must be a version string',
            'plain_string': u'Must be plain text',
            'segment': u'Can only contain lowercase alphanumeric characters and underscores',
            'url': u'Must be a valid url'
        }
        
        return errors[rule]