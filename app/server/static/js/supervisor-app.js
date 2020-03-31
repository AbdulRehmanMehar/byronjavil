// supervisor-app.js

var customers_vm = new Vue({
    el: '#customers-app',

    data: {
        visible: true,
        //users: [],
        apiKey: null,

        customer: {
            company: "",
            client_code: "",
            website: "",
            user: "",
            password: ""
        },

        edit: false,
        editID: null,
        
        customers: [
            {
                company: "MCL Control",
                client_code: "1214A",
                website: "https://www.mclcontrol.com",
                user: "great",
                password: "*******"
            },
            {
                company: "Intelcon",
                client_code: "5676A",
                website: "https://www.intelcon.com",
                user: "great",
                password: "*******"
            }
        ],
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
            $('#customer-create').modal('hide');
        },

        createCustomer: function(){

            var form = document.getElementById('customer-form');

            if (form.checkValidity() === true) {
                this.closeModal();
                this.postForm();
            }
            form.classList.add('was-validated');

        },

        updateCustomer: function(){

            var form = document.getElementById('customer-form');

            if (form.checkValidity() === true) {
                this.closeModal();
                this.postForm();
            }
            form.classList.add('was-validated');

        },

        fetchCustomers: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/supervisor/customers', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.customers = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        postForm: function(){
            
            var apiKey = this.apiKey;

            payload = this.$get("user");

            waitingDialog.show('Sending');

            if (this.edit){

                var id = this.editID;
                this.$http.put('/api/supervisor/customers/' + id, payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        this.fetchCustomers();
                        this.resetCustomer()
                        waitingDialog.hide();
                    },
                    function (err) {
                        console.log(err);
                });
            }
            else {
                this.$http.post('/api/supervisor/customers', payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        this.fetchCustomers();
                        this.resetCustomer()
                        waitingDialog.hide();
                    },
                    function (err) {
                        console.log(err);
                });

            }
            
        },

        editCustomer: function(index){

            var data = {
                company: this.customers[index].company,
                client_code: this.customers[index].client_code,
                website: this.customers[index].website,
                user: this.customers[index].user,
                password: this.customers[index].password
            };
            
            this.customer = data;
            this.edit = true;
            this.editID = this.customers[index].id;
        },

        resetCustomer: function(){
            
            var data = {
                company: "",
                client_code: "",
                website: "",
                user: "",
                password: ""
            };

            this.customer = data;

            this.edit = false;
            this.editID = null;
        },

        deleteCustomer: function(index){
           
            var id = this.customers[index].id;
            var apiKey = this.apiKey;
            var self = this;
            
            bootbox.confirm({
                message: "Do you want to delete this customer?",
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

                        self.$http.delete('/api/supervisor/customers/' + id, {headers: {'X-API-KEY': apiKey}})
                            .then(function (res) {
                                self.fetchCustomers();
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

var orders_vm = new Vue({
    el: '#orders-app',

    data: {
        visible: true,
        orders: [],
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

        fetchOrders: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/supervisor/orders', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.orders = res.data;
                }, function(err){
                    console.log(err);
                })
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