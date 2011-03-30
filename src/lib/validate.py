from handlers import BaseHandler
from tornado import locale

import re
from urlparse import urlparse, urlunparse

class FormValidator(BaseHandler):
    
    def __init__(self, cls):
        self.fields = {}
        self.field_rules = []
        
        self._validation_rules = False
        self._request_cls = cls
        
        self.user_locale = locale.get(self.get_user_locale())        
    
    def add_field(self, field_name, rule='', default=''):
        rules = rule.split('|')
        value = self._request_cls.get_argument(field_name, default)
        
        # populate
        self.fields[field_name] = value
        
        if not rule:
            return
        
        # not required and default value, skip validation
        if "required" not in rules and value == default:
            return
        
        for r in rules:
            self.field_rules.append([field_name, r])
    
    def get_field(self, field_name, in_type='text', val=''):
        if not field_name in self.fields:
            return ''

        if in_type == 'text':
            return self.fields[field_name]
        elif in_type == 'check':
            value = self.fields[field_name]
            
            if isinstance(value, list):
                if val in value:
                    return 'checked="checked"'
            elif value:
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
            
            actor = self.get_validator(rule)
            
            if callable(actor):
                self.fields[name] = actor(value)
                continue
            
            if actor.match(value) == None:
                errors[name] = self.get_human_error(rule)
        
        if len(errors):
            return errors
        
        return True
    
    def get_validator(self, rule):
        if not self._validation_rules:
            self._validation_rules = {
                'required': re.compile('.+'),
                'float': re.compile('\d+(\.\d+)?'),
                'plain_string': re.compile('[a-zA-Z0-9 _-]'), # @todo unicode chars?
                'segment': re.compile('[a-z0-9_]+'), # shortname needs to be a valid url segment, feel free to rename this
                'url': re.compile(r'^(?:http|ftp)s?://' # http:// or https://
                                  r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                                  r'localhost|' #localhost...
                                  r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                                  r'(?::\d+)?' # optional port
                                  r'(?:/?|[/?]\S+)$', re.IGNORECASE), # hate urls - hate them - no guarantees (source: http://www.codinghorror.com/blog/2008/10/the-problem-with-urls.html)
                
                'prep_url': _prep_url
            }
            
        return self._validation_rules[rule]
    
    def get_human_error(self, rule):
        
        _ = self.user_locale.translate
        
        errors = {
            'required': _(u'Required Field'),
            'float': _(u'Must be a version string'),
            'plain_string': _(u'Must be plain text'),
            'segment': _(u'Can only contain lowercase alphanumeric characters and underscores'),
            'url': _(u'Must be a valid url')
        }
        
        return errors[rule]


# Private validation functions
# @todo, these shouldn't need to be hardcoded in the validation rules dict

def _prep_url(s):
    if s.find('://') != -1:
        return s
    return 'http://'+s

