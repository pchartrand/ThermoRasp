var app = new Vue({
    el: '#app',
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
        app.$data.temperature = response.data.temperature
        app.$data.target = response.data.target
        app.$data.heating = response.data.heating
        app.$data.automatic = response.data.automatic
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
app.poll();

