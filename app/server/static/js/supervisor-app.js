// supervisor-app.js

var order_type_vm = new Vue({
    el: '#order-type-app',

    data: {
        visible: true,
        orderTypes: [],
        apiKey: null,
    },

    ready: function(){
    },

    methods: {

        hide: function(){
            this.visible = false;
        },

        show: function(){
            this.visible = false;
        },

        setKey: function(key){
            this.apiKey = key;
        },

        fetchOrderTypes: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/supervisor/order-type', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.orderTypes = res.data;
                }, function(err){
                    console.log(err);
                })
        }
    }
})

var users_vm = new Vue({
    el: '#users-app',

    data: {
        visible: true,
        users: [],
        apiKey: null,
    },

    ready: function(){
    },

    methods: {

        hide: function(){
            this.visible = false;
        },

        show: function(){
            this.visible = false;
        },

        setKey: function(key){
            this.apiKey = key;
        },

        fetchUsers: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/supervisor/users', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.users = res.data;
                }, function(err){
                    console.log(err);
                })
        }
    }
})

var vm = new Vue({

    el: '#app',

    data: {
        apiKey: null,
        username: null,

        users: [],
        types: [],
    },

    ready: function(){
        order_type_vm.setKey(this.apiKey);
        order_type_vm.fetchOrderTypes();
    },

    methods: {

        // Fetch methods
        show: function(app){
            console.log(app);
            if (app == 'order-type'){
                order_type_vm.toggleShow();
            }

        },

        fetchUsers: function(){

        },

        fetchTypes: function(){

        },

        fetchOrders: function(){

        }

        // Post methods


        // Put methods

    }
})