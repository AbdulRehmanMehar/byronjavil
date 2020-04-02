// supervisor-app.js

var orders_vm = new Vue({
    el: '#orders-app',

    data: {
        visible: true,
        orders: [],
        apiKey: null,

        order: {
            address: "",
            username: "",
            user_id: "",
            customer: "",
            customer_id: "",
            type: "",
            state: ""
        },

        edit: false,
        editID: null
    },

    ready: function(){
    },

    methods: {

        hide: function(){
            this.visible = false;
        },

        show: function(){
            this.visible = true;
        },

        setKey: function(key){
            this.apiKey = key;
        },

        closeModal: function(){
            $('#order-create').modal('hide');
        },

        createOrder: function(){

            var form = document.getElementById('order-form');

            if (form.checkValidity() === true) {
                this.closeModal();
                this.postForm();
            }
            form.classList.add('was-validated');

        },

        updateOrder: function(){

            var form = document.getElementById('order-form');

            if (form.checkValidity() === true) {
                this.closeModal();
                this.postForm();
            }
            form.classList.add('was-validated');

        },

        fetchOrders: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/supervisor/orders', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.orders = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        postForm: function(){
            
            var apiKey = this.apiKey;

            payload = this.$get("order");

            waitingDialog.show('Sending');

            if (this.edit){

                var id = this.editID;
                this.$http.put('/api/supervisor/orders/' + id, payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        this.fetchOrders();
                        this.resetOrder()
                        waitingDialog.hide();
                    },
                    function (err) {
                        console.log(err);
                });
            }
            else {
                this.$http.post('/api/supervisor/orders', payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        this.fetchOrders();
                        this.resetOrder()
                        waitingDialog.hide();
                    },
                    function (err) {
                        console.log(err);
                });

            }
            
        },

        resetForm: function(){
            
            var form = document.getElementById('order-form');
            form.classList.remove("was-validated");
        },

        editOrder: function(index){
            
            var data = {
                company: this.orders[index].address,
                username: this.orders[index].username,
                user_id: this.orders[index].user_id,
                customer: this.orders[index].customer,
                customer_id: this.orders[index].customer_id,
                type: this.orders[index].type,
                state: this.orders[index].state
            };
            
            this.order = data;
            this.edit = true;
            this.editID = this.orders[index].id;
        },

        resetOrder: function(){
            
            var data = {
                address: "",
                username: "",
                user_id: "",
                customer: "",
                customer_id: "",
                type: "",
                state: ""
            };

            this.order = data;

            this.edit = false;
            this.editID = null;

            this.resetForm();
        },

        deleteOrder: function(index){
           
            var id = this.orders[index].id;
            var apiKey = this.apiKey;
            var self = this;
            
            bootbox.confirm({
                message: "Do you want to delete this order?",
                buttons: {
                    confirm: {
                        label: 'Yes',
                        className: 'btn-success'
                    },
                    cancel: {
                        label: 'No',
                        className: 'btn-danger'
                    }
                },
                callback: function (result) {
                    if (result == true){

                        waitingDialog.show('Sending');

                        self.$http.delete('/api/supervisor/orders/' + id, {headers: {'X-API-KEY': apiKey}})
                            .then(function (res) {
                                self.fetchOrders();
                                waitingDialog.hide();
                            },
                            function (err) {
                                console.log(err);
                                waitingDialog.hide();
                        });
                    }
                }
            });

        }

    }
})

var attachments_vm = new Vue({
    el: '#attachments-app',

    data: {
        visible: true,
        attachments: [],
        apiKey: null,
    },

    ready: function(){
    },

    methods: {

        hide: function(){
            this.visible = false;
        },

        show: function(){
            this.visible = true;
        },

        setKey: function(key){
            this.apiKey = key;
        },

        fetchAttachments: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/supervisor/attachments', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.orders = res.data;
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
        
        types: [],

        order_type: "",
        customer: {},
        order: {},
    },

    ready: function(){
        order_type_vm.setKey(this.apiKey);
        users_vm.setKey(this.apiKey);
        customers_vm.setKey(this.apiKey);
        orders_vm.setKey(this.apiKey);
        attachments_vm.setKey(this.apiKey);
        
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

            if (app == 'orders'){
                orders_vm.show();
            }

            if (app == 'attachments'){
                attachments_vm.show();
            }

        },

        hide: function(){
            order_type_vm.hide();
            users_vm.hide();
            customers_vm.hide();
            orders_vm.hide();
            attachments_vm.hide();
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