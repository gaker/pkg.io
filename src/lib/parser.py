import re

class Parser(object):

    def set_package_type(self, package_type):
        self.package_type = package_type
    
    def set_template(self, template):
        self.template = template
    
    def parse(self, data):        
        if self.package_type == 'accessory':
            a = Accessory()
            a.render(self.template, data)
    
class Accessory(Parser):
    
    def render(self, template, data):
        # Grab the template file
        self.data = data
        # print self.data
        out = None
        
        tag_re = re.compile('(\{\{(.+?)\}\})');


        for line in open(template):
            # Parse {{ vars }}
            match = tag_re.search(line)
            if match is not None:
                out = self._parse_var(line, match.groups())
                print out
            # out = self._parse_var(line.rstrip())
        # print out
    def _parse_var(self, line, var):
        old_var = var[0].strip()
        new_var = self.data.get(var[1].strip())

        return line.replace(old_var, new_var)
        
args = {
    'accessory_name': 'My Accessory',
    'accessory_short_name': 'my_accessory',
    'author': 'Greg Aker',
    'accessory_version': '1.0',
    'accessory_description': 'test',
    'sections': {
        'title': 'Section 1',
        'contents': 'hi!'
    } 
}

p = Parser()
p.set_package_type('accessory')
p.set_template('/Volumes/Development/Projects/pkg.io/src/templates/addon_templates/accessory/acc.package.php')
p.parse(args)


# p = Parser('accessory', '', **args)
# print dir(p)