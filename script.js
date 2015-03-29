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



$(document).ready(function(e) {
	
	$('.sheet').click(function(e) {
		$(this).remove()
	});

	$('.sheet').hover(
		function(e) {
			console.log('Hover in');
			// $(this).animate({backgroundColor: '#ECB021'}, 500);
			$(this).css({backgroundColor: '#ECB021'});
	},  function(e) {
			console.log('Hover out');
			// $(this).animate({backgroundColor: '#71D3F8'}, 500);
			$(this).css({backgroundColor: '#71D3F8'});
	});

});