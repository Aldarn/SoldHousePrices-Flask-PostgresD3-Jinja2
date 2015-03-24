//
// Copyright 2015 Benjamin David Holmes, All rights reserved.
//

$(function () {
	$("#averageForm").submit(function(event) {
		$("#average").empty();
		var link = "/averagePrices?" + $("#averageForm").serialize();
		drawAveragePricesGraph(link);
		event.preventDefault();
	});
});
