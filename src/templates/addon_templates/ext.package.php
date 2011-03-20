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
 * {{ package_name }} Extension
 *
 * @package		ExpressionEngine
 * @subpackage	Addons
 * @category	Extension
 * @author		{{ author }}
 * @link		{{ author_url }}
 */

class {{ ucfirst(package_short_name) }}_ext {
	
	public $settings 		= array();
	public $description		= '{{ dequote(description) }}';
	public $docs_url		= '{{ docs_url }}';
	public $name			= '{{ package_name }}';
	public $settings_exist	= '{{ settings_exist }}';
	public $version			= '{{ version }}';
	
	private $EE;
	
	/**
	 * Constructor
	 *
	 * @param 	mixed	Settings array or empty string if none exist.
	 */
	public function __construct()
	{
		$this->EE =& get_instance();
	}
	
	// ----------------------------------------------------------------------
	
	/**
	 * Activate Extension
	 *
	 * This function enters the extension into the exp_extensions table
	 *
	 * @see http://codeigniter.com/user_guide/database/index.html for
	 * more information on the db class.
	 *
	 * @return void
	 */
	public function activate_extension()
	{
		$this->settings = array();
		
		$data = array(
			'class'		=> __CLASS__,
			'method'	=> '', // Add your method name here.
			'hook'		=> '',
			'settings'	=> serialize($this->settings),
			'version'	=> $this->version,
			'enabled'	=> 'y'
		);
		
		$this->EE->db->insert('extensions', $data);		
	}
	
	// ----------------------------------------------------------------------

	/**
	 * Disable Extension
	 *
	 * This method removes information from the exp_extensions table
	 *
	 * @return void
	 */
	function disable_extension()
	{
		$this->EE->db->where('class', __CLASS__);
		$this->EE->db->delete('extensions');
	}

	// ----------------------------------------------------------------------

	/**
	 * Update Extension
	 *
	 * This function performs any necessary db updates when the extension
	 * page is visited
	 *
	 * @return 	mixed	void on update / false if none
	 */
	function update_extension($current = '')
	{
		if ($current == '' OR $current == $this->version)
		{
			return FALSE;
		}
	}	
	
	// ----------------------------------------------------------------------
}

/* End of file ext.{{ package_short_name }}.php */
/* Location: /system/expressionengine/third_party/{{ package_short_name }}/ext.{{ package_short_name }}.php */

