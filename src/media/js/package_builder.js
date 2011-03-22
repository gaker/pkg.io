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
	
	
	// Iteration 823098589409 of death ... works for now
	
	var Hooks = (function() {
		
		var container = $('#extension_hook_options'),
			hook_checks = $('input[name="extension_hooks[]"]'),
			hook_inputs = [];
		
		// We want to maintain the same order for the textfields as
		// we do for the checkboxes, sooo .... we keep the checkbox
		// index (which is constant) for each checkbox we add in a
		// sorted array (hook_inputs).
		
		return {
			add: function(check_el) {
				var idx = hook_checks.index(check_el),
					value = check_el.value,
					prev, str = '';
				
				str = '<dt><label for="extension_hook_'+value+'">'+value+'</label></dt>' +
					  '<dd><input type="text" name="extension_hook_'+value+'" id="extension_hook_'+value+'"></dd>';
				
				// Add the original index to our hook input array and re-sort.
				hook_inputs.push(idx);
				hook_inputs.sort(function(a, b) {
					return a - b;
				});
				
				// Now extract the new index relative to the input elements
				// already shown
				prev = hook_inputs.indexOf(idx);
				
				if (prev < 1) {
					container.find('dl').prepend(str);
				} else {
					container.find('dl dd').eq(prev - 1).after(str);
				}

				container.show();
			},
			
			remove: function(check_el) {
				var idx = hook_checks.index(check_el), dd;
				idx = hook_inputs.indexOf(idx);
				
				if (idx !== -1) {
					hook_inputs.splice(idx, 1);
				}
				
				// Remove the dt and dd that make up our text input
				dd = $('#extension_hook_'+check_el.value).parent();
				dd.prev().remove();
				dd.remove();
				
				if ( ! this.count()) {
					container.hide()
				}
			},
			
			count: function() {
				return hook_inputs.length;
			}
		};
		
	})();
	
	$('input[name="extension_hooks[]"]').change(function () {
		
		if (this.checked === false) {
			Hooks.remove(this);
		} else {
			Hooks.add(this);
		}
	});
	
	
	var reload = false,
		form = $('form');
		
	form.submit(function() {
		if (reload) return true;
		
		$.post(this.action, $(this).serialize(), function(result) {
			
			if (result.indexOf('<') !== -1) {
				// darn, something went wrong @todo better solution than running it again
				reload = true;
				form.trigger('submit');
				return;
			}
			
			window.location = '/get_package/'+result;
		});
		
		return false;
		
	});
})(jQuery);