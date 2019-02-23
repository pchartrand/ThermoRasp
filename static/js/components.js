var statusComponent = new Vue({
    el: '#status',
    data: {
        'temperature': '',
        'target': '',
        'heating': '',
        'automatic': ''
    },
    methods: {
      poll: function () {
        axios.get('/status')
        .then(function (response) {
        // handle success
        statusComponent.$data.temperature = response.data.temperature
        statusComponent.$data.target = response.data.target
        statusComponent.$data.heating = response.data.heating
        statusComponent.$data.automatic = response.data.automatic
        //console.log(response.data);
        })
        .catch(function (error) {
        // handle error
        console.log(error);
        })
        .then(function () {
        // always executed
        });
      }
    }
});
statusComponent.poll();

