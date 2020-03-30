// supervisor-app.js

var users_vm = new Vue({
    el: '#users-app',

    data: {
        visible: true,
        users: [],
        apiKey: null,

        user: {
            username: "",
            password: "",
            email: "",
            role: "RESEARCH",
        },

        edit: false,
        editID: null,
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
            $('#user-create').modal('hide');
        },

        createUser: function(){

            var form = document.getElementById('user-form');

            if (form.checkValidity() === true) {
                this.closeModal();
                this.postForm();
            }
            form.classList.add('was-validated');

        },

        updateUser: function(){

            var form = document.getElementById('user-form');

            if (form.checkValidity() === true) {
                this.closeModal();
                this.postForm();
            }
            form.classList.add('was-validated');

        },

        fetchUsers: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/supervisor/users', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.users = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        postForm: function(){
            
            var apiKey = this.apiKey;

            payload = this.$get("user");

            waitingDialog.show('Sending');

            if (this.edit){

                var username = this.editUsername;
                this.$http.put('/api/supervisor/users/' + username, payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        this.fetchUsers();
                        this.resetUser()
                        waitingDialog.hide();
                    },
                    function (err) {
                        console.log(err);
                });
            }
            else {
                this.$http.post('/api/supervisor/users', payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        this.fetchUsers();
                        this.resetUser()
                        waitingDialog.hide();
                    },
                    function (err) {
                        console.log(err);
                });

            }
            
        },

        editUser: function(index){

            var data = {
                username: this.users[index].username,
                password: "*******",
                email: this.users[index].email,
                role: this.users[index].role.role,
            };
            
            this.user = data;
            this.edit = true;
            this.editUsername = this.users[index].username;
        },

        resetUser: function(){
            this.user = {
                username: "",
                password: "",
                email: "",
                role: "RESEARCH",
            };
            this.edit = false;
            this.editID = null;
        },

        deleteUser: function(index){
           
            var username = this.users[index].username;
            var apiKey = this.apiKey;
            var self = this;
            
            bootbox.confirm({
                message: "Do you want to delete this user?",
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

                        self.$http.delete('/api/supervisor/users/' + username, {headers: {'X-API-KEY': apiKey}})
                            .then(function (res) {
                                self.fetchUsers();
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

var customers_vm = new Vue({
    el: '#customers-app',

    data: {
        visible: true,
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

        fetchCustomers: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/supervisor/customer', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.customers = res.data;
                }, function(err){
                    console.log(err);
                })
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

        users: [],
        types: [],

        order_type: "",
        user: {},
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