<?php

class %(package_name)s_acc {
	
	public $name			= '{{ package_name }}';
	public $id				= '{{ package_short_name }}';
	public $version			= '{{ version }}';
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