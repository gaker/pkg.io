<?php  if ( ! defined('BASEPATH')) exit('No direct script access allowed');

$lang = array({% if 'module' in types %}	
	'{{ package_short_name }}_module_name' => 
	'{{ package_name }}',

	'{{ package_short_name }}_module_description' => 
	'{{ module_description }}',

	'module_home' => '{{ package_name }} Home',
	{% end %}
// Start inserting custom language keys/values here
	
);

/* End of file lang.{{ package_short_name }}.php */
/* Location: /system/expressionengine/third_party/{{ package_short_name }}/language/english/lang.{{ package_short_name }}.php */
