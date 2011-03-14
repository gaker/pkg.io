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
 * {{ package_name }} Accessory
 *
 * @package		ExpressionEngine
 * @subpackage	Addons
 * @category	Accessory
 * @author		{{ author }}
 * @link		{{ author_url }}
 */

class {{ ucfirst(package_short_name) }}_acc {
	
	public $name			= '{{ package_name }}';
	public $id				= '{{ package_short_name }}';
	public $version			= '{{ version }}';
	public $description		= '{{ dequote(description) }}';
	public $sections		= array();
	
	/**
	 * Set Sections
	 */
	public function set_sections()
	{
		$EE =& get_instance();
		
		{% for section in sections %}
		$this->sections['{{ dequote(section['title']) }}'] = $EE->load->view('accessory_{{ section['short_title'] }}');
		{% end %}
	}
	
	// ----------------------------------------------------------------
	
}

/* End of file acc.{{ package_short_name }}.php */
/* Location: /system/expressionengine/third_party/{{ package_short_name }}/acc.{{ package_short_name }}.php */