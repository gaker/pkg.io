import re

class Parser(object):

    def set_package_type(self, package_type):
        self.package_type = package_type
    
    def set_template(self, template):
        self.template = template
    
    def parse(self, data):        
        if self.package_type == 'accessory':
            a = Accessory()
            return a.render(self.template, data)
    
class Accessory(Parser):
    
    def render(self, template, data):
        # Grab the template file
        self.data = data
        out = ''
        
        tag_re = re.compile('(\{\{(.+?)\}\})');

        for line in open(template):
            # Parse {{ vars }}
            match = tag_re.search(line)
            if match is not None:
                out += self._parse_var(line, match.groups())
            else:
                out += line
            # out = self._parse_var(line.rstrip())
        return out
    
    def _parse_var(self, line, var):
        old_var = var[0].strip()
        new_var = self.data.get(var[1].strip())

        return line.replace(old_var, new_var)


# p = Parser('accessory', '', **args)
# print dir(p)