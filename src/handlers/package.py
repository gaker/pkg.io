import os.path
import re
import tornado
import tornado.options
import uuid

from handlers import BaseHandler
from lib.builder import PackageBuilder
from lib.validate import FormValidator
from tornado.options import options
from zipfile import ZipFile, ZipInfo

class PackageHandler(BaseHandler):
    
    def get(self):
        self.render('packages/package_form.html', 
                    form_error=self.blank_callback,
                    set_value=self.blank_callback,
                    hooks=self.get_hooks(),
                    mappings={},
                    packages_selected=True)
    
    def post(self):
        ''' This is a productive method.'''
        
        self.build_package = False
        self.need_lang_file = False
        self.lang_type = []
        
        form = FormValidator(self)
        # all_hooks = self.get_hooks()
        
        # Basic Settings
        form.add_field('author', 'required|plain_string')
        form.add_field('author_url', 'prep_url|url')
        form.add_field('docs_url', 'prep_url|url')
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
            self.build_package = True
            form.add_field('accessory_description', 'required')
            form.add_field('accessory_sections_num')
            value = form.get_field('accessory_sections_num')
            
            if value.isdigit() and 0 < int(value) < 4:
                accessory_sections = int(value)
                
                for k in xrange(1, int(value) + 1):
                    form.add_field('accessory_%d_title' % k, 'required')
                    form.add_field('accessory_%d_content' % k)
        
        if form.get_field('pkg_plugin'):
            self.build_package = True
            form.add_field('plugin_description', 'required')
            form.add_field('plugin_instructions', 'required')
        
        if form.get_field('pkg_module'):
            self.build_package = True
            form.add_field('module_has_control_panel', '', '0')
            form.add_field('module_description', 'required')
        
        hooks = self.get_hooks()
        mappings = {}
        
        if form.get_field('pkg_extension'):
            self.build_package = True
            form.add_field('extension_has_settings', '', 0)
            form.add_field('extension_description', 'required')
            form.add_field('extension_hooks[]', '', [])
            
            checked_hooks = form.get_field('extension_hooks[]')
            for hook_name in checked_hooks:
                if hook_name in hooks:
                    form.add_field('extension_hook_'+hook_name, '', '')
                    mappings[hook_name] = form.get_field('extension_hook_'+hook_name)
        
        errors = form.validate()

        if self.build_package is False and errors is True:
            errors = {}
        
        if errors is not True:
            self.render('packages/package_form.html', 
                        form_error=self.error_function(errors),
                        set_value=form.get_field,
                        hooks=hooks,
                        mappings=mappings,
                        packages_selected=self.build_package)
            return
            
        # WOOT start building
        
        files = []
        short_name = form.get_field('package_short_name')
        
        template_path = os.path.join(self.get_template_path(),
                                    'addon_templates/')

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
            'accessory': 'acc.{package}.php',
            'plugin': 'pi.{package}.php',
            'ext': 'ext.{package}.php',
            'mcp': 'mcp.{package}.php',
            'mod': 'mod.{package}.php',
            'upd': 'upd.{package}.php',
            'view': 'views/{view}.php',
            'lang': 'language/english/lang.{package}.php'
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
                'description': form.get_field('accessory_description'),
                'sections': sections
            })

        # Build plugin
        if form.get_field('pkg_plugin'):
            build.add_plugin({
                'description': form.get_field('plugin_description'),
                'instructions': form.get_field('plugin_instructions')
            })
        
        # Build module
        if form.get_field('pkg_module'):
            select_cp = ['n', 'y']
            has_cp = int(form.get_field('module_has_control_panel'))
            
            self.need_lang_file = True
            self.lang_type.append('module')
            
            build.add_module({
                'has_cp': select_cp[has_cp],
                'module_description': form.get_field('module_description') 
            })
        
        if form.get_field('pkg_extension'):
            select_cp = ['n', 'y']
            has_cp = int(form.get_field('extension_has_settings'))
            
            if has_cp == 1:
                self.need_lang_file = True
                self.lang_type.append('extension')
            
            build.add_extension({
                'has_cp': select_cp[has_cp],
                'ext_description': form.get_field('extension_description'),
                'hooks': mappings
            })
        
        if self.need_lang_file is True:
            build.add_lang_file({
                'types': self.lang_type
            })
        
        
        # All files must have that first subdirectory in their path
        # so that the archive extracts cleanly with that folder name
        
        filename = str(uuid.uuid4())

        # Zip 'er up!
        zippath = os.path.join(options.zips_dir, '%s.zip' % filename)
        download = ZipFile(zippath, 'w')
        
        for i in build.get_files():
            download.writestr('%s/%s' % (short_name, i[0]), i[1])
        
        download.close()
        
        self.set_header("Content-Type", "text/plain")
        self.write(filename)
        
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
    
    def get_hooks(self):
        hooks = ["channel_entries_query_result", "channel_entries_tagdata", "channel_entries_row", "channel_entries_tagdata_end", "channel_module_calendar_start", "channel_module_categories_start", "channel_module_category_heading_start", "channel_module_create_pagination", "channel_module_fetch_pagination_data",
                "comment_entries_comment_format", "comment_entries_tagdata", "comment_form_end", "comment_form_hidden_fields", "comment_form_tagdata", "comment_preview_comment_format", "comment_preview_tagdata", "cp_css_end", "cp_js_end", "cp_member_login", "cp_member_logout", "cp_members_member_create",
                "cp_members_member_create_start", "cp_members_member_delete_end", "cp_members_validate_members", "create_captcha_start", "delete_comment_additional", "delete_entries_loop", "delete_entries_start", "entry_submission_end", "entry_submission_ready", "entry_submission_start", "edit_template_start",
                "edit_wiki_article_end", "edit_wiki_article_form_end", "edit_wiki_article_form_start", "email_module_send_email_end", "email_module_tellafriend_override", "entry_submission_absolute_end", "entry_submission_redirect", "foreign_character_conversion_array", "form_declaration_modify_data",
                "form_declaration_return", "forum_submission_form_start", "forum_submission_form_end", "forum_submission_page", "forum_submit_post_start", "forum_submit_post_end", "forum_threads_template", "forum_thread_rows_absolute_end", "forum_thread_rows_loop_start", "forum_thread_rows_loop_end",
                "forum_thread_rows_start", "forum_topics_absolute_end", "forum_topics_loop_start", "forum_topics_loop_end", "forum_topics_start", "insert_comment_end", "insert_comment_insert_array", "insert_comment_preferences_sql", "insert_comment_start", "login_authenticate_start", "main_forum_table_rows_template",
                "member_edit_preferences", "member_manager", "member_member_login_multi", "member_member_login_single", "member_member_login_start", "member_member_logout", "member_member_register", "member_member_register_start", "member_register_validate_members", "member_update_preferences", "simple_commerce_evaluate_ipn_response",
                "simple_commerce_perform_actions_end", "simple_commerce_perform_actions_start", "sessions_end", "sessions_start", "publish_form_channel_preferences", "publish_form_entry_data", "typography_parse_type_end", "typography_parse_type_start", "update_comment_additional", "update_multi_entries_loop", "update_multi_entries_start",
                "update_template_end", "wiki_article_end", "wiki_article_start", "wiki_special_page", "wiki_start"]
        hooks.sort()
        return hooks

## --------------------------------------------------------------------

class GetPackageHandler(BaseHandler):
    
    def _validate_zip(self, file_id=None):
        if re.match('[A-Za-z0-9-]+', file_id) == None:
            raise tornado.web.HTTPError(404)
        
        zippath = os.path.join(options.zips_dir, '%s.zip' % file_id)
        
        if not os.path.exists(zippath):
            raise tornado.web.HTTPError(404)   
        
        return zippath
    
    def get(self, file_id=None):
        
        zippath = self._validate_zip(file_id)        
        
        self.render('packages/get_package.html')
        
        
           
    def post(self, file_id=None):
        
        zippath = self._validate_zip(file_id)
        
        with open(zippath, 'rb') as f:
            content = f.read()
                
        self.set_header("Content-Type", "application/octet-stream")
        self.set_header("Content-Length", os.path.getsize(zippath))
        self.set_header("Content-Disposition", 
                        "attachment; filename=pkgio_package.zip")
        self.write(content)
        
