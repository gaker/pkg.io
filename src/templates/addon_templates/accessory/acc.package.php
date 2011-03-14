<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class {{ ucfirst(package_short_name) }}_acc {
	
	public $name			= '{{ package_name }}';
	public $id				= '{{ package_short_name }}';
	public $version			= '{{ version }}';
	public $description		= '{{ escape(description) }}';
	public $sections		= array();
	
	/**
	 * Constructor
	 */
	public function __construct()
	{
		$this->EE =& get_instance();
	}
	
	// ----------------------------------------------------------------
	
	/**
	 * Set Sections
	 */
	public function set_sections()
	{
		{% for section in sections %}
		$this->sections['{{ section['title'] }}'] = '{{ section['content'] }}';
		{% end %}
	}
	
	// ----------------------------------------------------------------
	
}

/* End of file acc.{{ package_short_name }}.php */
/* Location: /system/expressionengine/third_party/{{ package_short_name }}/acc.{{ package_short_name }}.php */