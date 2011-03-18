(function($) {
	
	$('#choose_ur_pkg input[type=checkbox]').click(function () {
		// @todo Disable inputs if module or plugin is checked.
		
		var section = this.name.substring(4);
		$('#'+section).toggle();
	})
	.filter(':checked').triggerHandler('click');
	
	$('#accessory_sections_num').change(function () {
		var num = this.value;
		$('#accessory_2').toggle(num > 1);
		$('#accessory_3').toggle(num > 2);
	})
	.triggerHandler('change');
	
	var shortname = $('input[name=package_short_name]').get(0);
	
	$('input[name=package_name]').blur(function() {
		var val = this.value.replace(/\s+/gi, '_');
		val = val.replace(/[^a-z0-9_]/gi, '');
		shortname.value = val.toLowerCase();
	});
	
	$('input, textarea').bind('click focus', function() {
		if (this.placeholder && ! this.value) {
			this.value = this.placeholder;
			setTimeout($.proxy(this, 'select'), 0);
		}
	});
	
})(jQuery);