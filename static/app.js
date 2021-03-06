$(function () {
	socket = io.connect('http://' + document.domain + ':' + location.port);
	socket.on('connect', function() {
		$('#status').text('Connecté');
    	socket.emit('client_connected', {data: 'New client!'});
	});

	socket.on('disconnect', function() {
		$('#status').text('Déconnecté');
	});

	socket.on('alert', function (data) {
    	$('#status').text('Connecté');
        $('#content').append(data + "<br />");
	});

	socket.on('gauge',function (data) {
		gauge.set(parseFloat(data));
	});

		socket.on('g',function (data) {
		g.refresh(parseFloat(data));
	})

});