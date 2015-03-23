$(function () {
	$("#averageForm").submit(function(event) {
		$("#average").empty();
		var link = "/averagePrices?" + $("#averageForm").serialize();
		drawAveragePricesGraph(link);
		event.preventDefault();
	});
});
