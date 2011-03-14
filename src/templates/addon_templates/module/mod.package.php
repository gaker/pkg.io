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
 * {{ package_name }} Module Front End File
 *
 * @package		ExpressionEngine
 * @subpackage	Addons
 * @category	Module
 * @author		{{ author }}
 * @link		{{ author_url }}
 */

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
	 * Start on your custom code here...
	 */
	
}
/* End of file mod.{{ package_short_name }}.php */
/* Location: /system/expressionengine/third_party/{{ package_short_name }}/mod.{{ package_short_name }}.php */