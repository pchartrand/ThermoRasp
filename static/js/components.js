var statusComponent = new Vue({
    el: '#status',
    data: {
        'temperature': '',
        'target': '',
        'heating': '',
        'automatic': ''
    },
    methods: {
      setMode: function (){
        var key;
        if (statusComponent.$data.automatic){
            key = 'manual';
        }else{
            key = 'automatic'
        }
        var action = '/'+ key;
        axios.post(action, {action: true}, {headers: {'Content-Type': 'application/json'}})
        .then(function (response) {
            if (key == 'automatic'){
                statusComponent.$data.automatic = true;
            }else{
                statusComponent.$data.automatic = false;
            }
            console.log('INFO '+response.status);
        })
        .catch(function(error){
            console.log('WARN ' + error);
        })
        .then(function () {
            // always executed
            console.log('INFO setMode ' + key + ' done');
        });
      },
      setTarget: function (){
        axios.put('/target', {target: statusComponent.$data.target}, {headers: {'Content-Type': 'application/json'}})
        .then(function (response) {
            statusComponent.$data.temperature = response.data.temperature
            statusComponent.$data.target = response.data.target
            statusComponent.$data.heating = response.data.heating
            statusComponent.$data.automatic = response.data.automatic
            console.log('INFO '+response.status);
        })
        .catch(function(error){
            console.log('WARN ' + error);
        })
        .then(function () {
            // always executed
            console.log('INFO setTarget done');
        });
      },
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

