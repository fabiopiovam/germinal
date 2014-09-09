function get_carousel_indicators(carousel_id) {
	$('.carousel-indicators', carousel_id).html('');
	$('.carousel-inner > div', carousel_id).each(function(index) {
		$('.carousel-indicators', carousel_id).append('<li data-target="'+ carousel_id +'" data-slide-to="'+ index +'"></li>');
	});
	$('.carousel-indicators li:first', carousel_id).addClass('active');
}
