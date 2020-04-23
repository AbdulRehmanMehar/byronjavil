// supervisor-app.js

var orders_vm = new Vue({
    el: '#orders-app',

    data: {
        visible: true,
        orders: [],
        apiKey: null,

        order: {
            address: "",
            research_id: "",
            data_id: "",
            company_id: "",
            client_code: "",
            type: "",
            assigned_date: "",
            due_date: ""
        },

        research_users: [],
        data_users: [],
        companies: [],
        order_types: [],
        client_codes: [],
        states: [],

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

        setUsers: function(users){
            var research = [];
            var data = [];

            for (var i=0; i<users.length; i++){
                var user = users[i];

                if (user.role.role == "RESEARCH"){
                    research.push(user);
                }

                if (user.role.role == "DATA"){
                    data.push(user);
                }
            }

            this.$set("research_users", research);
            this.$set("data_users", data);
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

        fetchAll: function(){
            this.fetchOrders();
            this.fetchUsers();
            this.fetchCompanies();
            this.fetchClientCodes();
            this.fetchOrderTypes();
            this.fetchStates();
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

        fetchUsers: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/supervisor/users', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    var users = res.data;
                    this.setUsers(users);
                }, function(err){
                    console.log(err);
                })
        },

        fetchCompanies: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/supervisor/companies', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.companies = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        fetchOrderTypes: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/supervisor/order-type', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.order_types = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        fetchClientCodes: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/supervisor/client-code', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.client_codes = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        fetchStates: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/supervisor/states', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.states = res.data;
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
                address: this.orders[index].address,
                research_id: this.orders[index].research_user.id,
                data_id: this.orders[index].data_user.id,
                company: this.orders[index].company.name,
                company_id: this.orders[index].company.id,
                client_code: this.orders[index].client_code.code,
                type: this.orders[index].kind.order_type,
                state: this.orders[index].state.state,
                assigned_date: this.orders[index].assigned_date,
                due_date: this.orders[index].due_date
            };
            
            this.order = data;
            this.edit = true;
            this.editID = this.orders[index].id;
        },

        viewOrder: function(id){
            location.href = "/supervisor/orders/" + id;
        },

        resetOrder: function(){
            
            var data = {
                address: "",
                username: "",
                research_id: "",
                data_id: "",
                company: "",
                company_id: "",
                client_code: "",
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
        company: {},
        order: {},
    },

    ready: function(){
        orders_vm.setKey(this.apiKey);

        orders_vm.fetchAll();
        
        this.show('orders');
    },

    methods: {

        show: function(app){
            this.hide();

            if (app == 'orders'){
                orders_vm.fetchAll();
                orders_vm.show();
            }

        },

        hide: function(){
            orders_vm.hide();
            attachments_vm.hide();
        }

    }
})