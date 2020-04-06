// admin-app.js

var vm = new Vue({

    el: '#app',

    data: {
        apiKey: null,
        username: null,
        
        types: [],

        order_type: "",
        customer: {},
        order: {},
    },

    ready: function(){
        order_type_vm.setKey(this.apiKey);
        users_vm.setKey(this.apiKey);
        customers_vm.setKey(this.apiKey);
        
        order_type_vm.fetchOrderTypes();
        users_vm.fetchUsers();
        customers_vm.fetchCustomers();
        
        this.show('order-type');
    },

    methods: {

        show: function(app){
            this.hide();
            
            if (app == 'order-type'){
                order_type_vm.show();
            }

            if (app == 'users'){
                users_vm.show();
            }

            if (app == 'customers'){
                customers_vm.show();
            }

        },

        hide: function(){
            order_type_vm.hide();
            users_vm.hide();
            customers_vm.hide();
        }

    }
})