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
	public $description		= '{{ dequote(ext_description) }}';
	public $docs_url		= '{{ dequote(docs_url) }}';
	public $name			= '{{ dequote(package_name) }}';
	public $settings_exist	= '{{ has_cp }}';
	public $version			= '{{ dequote(version) }}';
	
	private $EE;
	
	/**
	 * Constructor
	 *
	 * @param 	mixed	Settings array or empty string if none exist.
	 */
	public function __construct($settings = '')
	{
		$this->EE =& get_instance();
		$this->settings = $settings;
	}{% if has_cp == 'y' %}
	
	// ----------------------------------------------------------------------
	
	/**
	 * Settings Form
	 *
	 * If you wish for ExpressionEngine to automatically create your settings
	 * page, work in this method.  If you wish to have fine-grained control
	 * over your form, use the settings_form() and save_settings() methods 
	 * instead, and delete this one.
	 *
	 * @see http://expressionengine.com/user_guide/development/extensions.html#settings
	 */
	public function settings()
	{
		return array(
			
		);
	}
	
	{% end %}// ----------------------------------------------------------------------
	
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
		// Setup custom settings in this array.
		$this->settings = array();
		{% if len(hooks) == 1 %}{% for hook in hooks.items() %}
		$data = array(
			'class'		=> __CLASS__,
			'method'	=> '{{ hook[1] }}',
			'hook'		=> '{{ hook[0] }}',
			'settings'	=> serialize($this->settings),
			'version'	=> $this->version,
			'enabled'	=> 'y'
		);{% end %}

		$this->EE->db->insert('extensions', $data);			
		{% elif len(hooks) > 1 %}
		$hooks = array({% for hook in hooks.items() %}
			'{{ hook[0] }}'	=> '{{ hook[1] }}',{% end %}
		);

		foreach ($hooks as $hook => $method)
		{
			$data = array(
				'class'		=> __CLASS__,
				'method'	=> $method,
				'hook'		=> $hook,
				'settings'	=> serialize($this->settings),
				'version'	=> $this->version,
				'enabled'	=> 'y'
			);

			$this->EE->db->insert('extensions', $data);			
		}{% else %}
		// No hooks selected, add in your own hooks installation code here.{% end %}
	}	

	// ----------------------------------------------------------------------{% for hook in hooks.items() %}
	
	/**
	 * {{ hook[1] }}
	 *
	 * @param 
	 * @return 
	 */
	public function {{ hook[1] }}()
	{
		// Add Code for the {{ hook[0] }} hook here.  
	}

	// ----------------------------------------------------------------------{% end %}

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