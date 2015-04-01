/*
 * script.js
 * ...
 *
 * Jonatan H Sundqvist
 * March 30 2015
 *
 *
 * TODO | - 
 *        - 
 *
 * SPEC | -
 *        -
 *
 */


cache = { earliest: 0 }


function addEntryListeners() {
	
	/*  */

	$('.sheet').click(function(e) {
		$(this).parent().animate({marginLeft: '2000pt'}, { duration: 1500, complete: function() { $(this).remove(); } });
		// $(this).parent().remove()
	});


	$('.sheet').hover(
		function(e) {
			$(this).addClass('highlight');
			// console.log('Hover in');
			// $(this).animate({backgroundColor: '#ECB021'}, 500);
			// $(this).css({backgroundColor: '#ECB021'});
	},  function(e) {
			$(this).removeClass('highlight');
			// console.log('Hover out');
			// $(this).animate({backgroundColor: '#71D3F8'}, 500);
			// $(this).css({backgroundColor: '#71D3F8'});
	});

}


function poll(delay, success, options) {

	// Polls the (a?) server asynchronously for updates with the given frequency (1000/delay mHz).
	// The success callback is invoked with each response.

	// TODO: Make this a general-purpose function for async polling
	// TODO: Use promises (?)
	// TODO: Customise queries and poll behaviour (especially url) (make options a callable?)
	defaults = { success: function(data, status, xhr) { success(data, status, xhr); setTimeout(wrapper, delay); } }

	function wrapper() {
		$.ajax($.extend({}, defaults, options()));
	}

	setTimeout(wrapper, delay);

}


function appendEntries(data, status, xhr) {

	/*  */

	$.each(data, function(index, entry) {
		// TODO: Move-in animation
		console.log(entry);
		$('body').append(data[index]['contents']);
	});

	if (data.length > 0) {
		// TODO: Less fragile way of avoiding duplicates
		cache['earliest'] = Math.max.apply(null, data.map(function(entry) { return Date.parse(entry['date'] + ' UTC+0200')/1000; }));
		console.log('Updated earliest: %fms', cache['earliest'])
	}
	
	addEntryListeners();

}


$(document).ready(function(e) {
	
	/*  */
	addEntryListeners();
	poll(2000, appendEntries, function() {
		return { dataType: 'json',
			     url: 'api.esp?author=Jonatan%20H%20Sundqvist&earliest=' + String(cache['earliest']),
			     data: {} // TODO: How to access this parameter (self.rfile probably)
		}
	});

	// $('#reload').click(function(event) { loadNewEntries() });

});