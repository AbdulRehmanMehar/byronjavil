// supervisor-app.js

var order_type_vm = new Vue({
    el: '#order-type-app',

    data: {
        visible: true,
    },

    ready: function(){

    },

    methods: {

        hide: function(){
            this.visible = false;
        },

        show: function(){
            this.visible = false;
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