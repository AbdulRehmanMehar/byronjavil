// data-app.js

var vm = new Vue({

    el: '#app',

    data: {
        apiKey: null,
        username: null,

        orders: [],
    },

    ready: function(){
        this.fetchOrders();
    },

    methods: {

        fetchOrders: function(){
            var apiKey = this.apiKey;

            this.$http.get('/api/data/orders', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.orders = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        viewOrder: function(index){
            var id = this.orders[index].id;
            location.href = "/data/orders/" + id;
        }

    }
})