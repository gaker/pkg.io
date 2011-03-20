<?php  if ( ! defined('BASEPATH')) exit('No direct script access allowed');

/**
 * ExpressionEngine - by EllisLab
 *
 * @package		ExpressionEngine
 * @author		ExpressionEngine Dev Team
 * @copyright	Copyright (c) 2003 - 2011, EllisLab, Inc.
 * @license		http://expressionengine.com/user_guide/license.html
 * @link		http://expressionengine.com
 * @since		Version 2.0
 * @filesource
 */
 
// ------------------------------------------------------------------------

/**
 * {{ package_name }} Plugin
 *
 * @package		ExpressionEngine
 * @subpackage	Addons
 * @category	Plugin
 * @author		{{ author }}
 * @link		{{ author_url }}
 */

$plugin_info = array(
	'pi_name'		=> '{{ package_name }}',
	'pi_version'	=> '{{ version }}',
	'pi_author'		=> '{{ author }}',
	'pi_author_url'	=> '{{ author_url }}',
	'pi_description'=> '{{ dequote(description) }}',
	'pi_usage'		=> {{ ucfirst(package_short_name) }}::usage()
);


class {{ ucfirst(package_short_name) }} {

	public $return_data;
    
	/**
	 * Constructor
	 */
	public function __construct()
	{
		$this->EE =& get_instance();
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