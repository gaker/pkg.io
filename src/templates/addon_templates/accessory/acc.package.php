<?php

class %(package_name)s_acc {
	
	public $name			= '{{ accessory_name }}';
	public $id				= '{{ accessory_short_name }}';
	public $version			= '{{ accessory_version }}';
	public $description		= '{{ accessory_description }}';
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

	}
	
	// ----------------------------------------------------------------
	
	{% for section in sections %}
	
	/**
	 *
	 *
	 */
	
	{% end %}
}