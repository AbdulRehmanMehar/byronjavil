// manager-app.js

var vm = new Vue({

    el: '#app',

    data: {
        apiKey: null,
        username: null,

        users: [],
        types: [],
    },

    ready: function(){
        this.fetchOrders();
    },

    methods: {

        // Fetch methods
        fetchUsers: function(){

        },

        fetchTypes: function(){

        },

        fetchOrders: function(){

            var apiKey = this.apiKey;
            var url = "/api/manager/orders";

            this.$http.get(url, {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    var orders = res.data.data;

                    var actives = [];
                    var finished = [];

                    for (var i=0; i<orders.length; i++){
                        if (orders[i][7] == "Submitted") {
                            finished.push(orders[i]);
                        } else {
                            actives.push(orders[i]);
                        }
                    }

                    $('#active-orders-table').DataTable({
                        data: actives,
                        dom: 'Bfrtip',
                        buttons: [
                            'copy', 'csv', 'excel', 'pdf', 'print'
                        ],
                        "createdRow": function(row, data, dataIndex){
                            console.log(data);
                            if( data[7] ==  'Ready to submit'){
                                $(row).addClass('blueClass');
                            }
                        }
                    });

                    $('#finished-orders-table').DataTable({
                        data: finished,
                        dom: 'Bfrtip',
                        buttons: [
                            'copy', 'csv', 'excel', 'pdf', 'print'
                        ],
                        "createdRow": function(row, data, dataIndex){
                            console.log(data);
                            if( data[7] ==  'Ready to submit'){
                                $(row).addClass('blueClass');
                            }
                        }
                    });
                }, function(err){
                    console.log(err);
                })

            

        }

        // Post methods


        // Put methods

    }
})