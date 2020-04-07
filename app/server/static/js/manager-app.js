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

                    console.log(orders)

                    $('#orders-table').DataTable({
                        data: orders,
                        dom: 'Bfrtip',
                        buttons: [
                            'copy', 'csv', 'excel', 'pdf', 'print'
                        ]
                    } );
                }, function(err){
                    console.log(err);
                })

            

        }

        // Post methods


        // Put methods

    }
})