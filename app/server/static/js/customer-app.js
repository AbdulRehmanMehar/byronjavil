// customer-app.js

var customers_vm = new Vue({
    el: '#customers-app',

    data: {
        visible: true,
        customers: [],
        apiKey: null,

        customer: {
            company: "",
            client_code: "",
            website: "",
            user: "",
            password: ""
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

            this.$http.get('api/admin/customers', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.customers = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        postForm: function(){
            
            var apiKey = this.apiKey;

            payload = this.$get("customer");

            waitingDialog.show('Sending');

            if (this.edit){

                var id = this.editID;
                this.$http.put('/api/admin/customers/' + id, payload, {headers: {'X-API-KEY': apiKey}})
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
                this.$http.post('/api/admin/customers', payload, {headers: {'X-API-KEY': apiKey}})
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

        resetForm: function(){
            
            var form = document.getElementById('customer-form');
            form.classList.remove("was-validated");
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

            this.resetForm();
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