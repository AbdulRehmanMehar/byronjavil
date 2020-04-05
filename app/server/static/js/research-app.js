// research-app.js

var vm = new Vue({

    el: '#app',

    data: {
        apiKey: null,
        username: null,

        orders: [],
    },

    ready: function(){

    },

    methods: {

        // Fetch methods
        fetchOrders: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/research/orders', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.orders = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        // Post methods
        viewOrder: function(){
            location.href = "/research/orders/" + id;
        }
        
        // Put methods

    }
})