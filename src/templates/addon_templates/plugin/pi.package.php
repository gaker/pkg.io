<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

$plugin_info = array(
	'pi_name'		=> '{{ package_name }}',
	'pi_version'	=> '{{ version }}',
	'pi_author'		=> '{{ author }}',
	'pi_author_url'	=> '{{ author_url }}',
	'pi_description'=> '{{ description }}',
	'pi_usage'		=> {{ ucfirst(package_short_name) }}::usage()
);


class {{ ucfirst(package_short_name) }} {

	var $return_data;
    
	/**
	 * Constructor
	 */
	function __construct()
	{
		
	}
	
	// ----------------------------------------------------------------
	
	/**
	 * Plugin Usage
	 */
	static function usage()
	{
		ob_start();
?>
{{ instructions }}
<?php
		$buffer = ob_get_contents();
		ob_end_clean();
		return $buffer;
	}
}


/* End of file pi.{{ package_short_name }}.php */
/* Location: /system/expressionengine/third_party/{{ package_short_name }}/pi.{{ package_short_name }}.php */