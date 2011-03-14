<?php

class {{ ucfirst(package_short_name) }}s_acc {
	
	public $name			= '{{ package_name }}';
	public $id				= '{{ package_short_name }}';
	public $version			= '{{ version }}';
	public $description		= '{{ escape(description) }}';
	public $sections		= array();
	
	/**
	 * Construct
	 */
	public function __construct()
	{
		$this->EE =& get_instance();
	}
	
	// ----------------------------------------------------------------
	
	/**
	 * Set Sections
	 *
	 */
	public function set_sections()
	{
		{% for section in sections %}
		$this->sections['{{ section['title'] }}'] = '{{ section['content'] }}';
		{% end %}
	}
	
	// ----------------------------------------------------------------
	
}