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


function poll(frequency) {

	/* Polls the (a?) server asynchronously for updates */

	// TODO: Make this a general-purpose function for async polling
	// TODO: Use promises (?)

}


$(document).ready(function(e) {
	
	addEntryListeners();

	$('#reload').click(function(event) {
		$.ajax({
			dataType: 'json',
			url: 'api.esp?author=Jonatan%20H%20Sundqvist',
			data: {}, // TODO: How to access this parameter
			success: function(data, status, xhr) {

				$.each(data, function(index, entry) {
					// TODO: Move-in animation
					console.log(entry);
					$('body').append(data[index]['contents']);
				});

				addEntryListeners();

			}
		})

	});

});