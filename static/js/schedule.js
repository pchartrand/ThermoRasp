function drawSchedule(){
    d3.json('schedule', function(data) {
        for (var i = 0; i < data.length; i++) {
            data[i] = MG.convert.date(data[i], 'date','%Y-%m-%d %H:%M');
        }

        MG.data_graphic({
            title: "Températures 2019-03-08 16:17:16",
            description: "Chauffage pour la semaine",
            data: data,
            width: 1000,
            height: 600,
            point_size: 4,
            target: '#temperatures',
            legend: [ 'thermostat', 'température' ],
            legend_target: '.legend',
            //aggregate_rollover: true,
            colors: ['#00DD00', '#0000DD','#DD0000', '#BB00BB','#00BBBB','#BBBB00'],
            european_clock: true
        });
    });
};

drawSchedule();