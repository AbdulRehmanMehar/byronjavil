// company-app.js

var companies_vm = new Vue({
    el: '#companies-app',

    data: {
        visible: true,
        companies: [],
        apiKey: null,

        company: {
            name: "",
            client_code: "",
            website: "",
            user: "",
            password: ""
        },

        edit: false,
        editID: null,
        view_password: false
        
    },

    ready: function(){
    },

    methods: {

        hide: function(){
            this.visible = false;
        },

        show: function(){
            this.visible = true;
            this.fetchClientCodes();
        },

        setKey: function(key){
            this.apiKey = key;
        },
        
        togglePassword: function(){
            this.view_password = !this.view_password;
        },

        closeModal: function(){
            $('#company-create').modal('hide');
        },

        createCompany: function(){

            var form = document.getElementById('company-form');

            if (form.checkValidity() === true) {
                this.closeModal();
                this.postForm();
            }
            form.classList.add('was-validated');

        },

        updateCompany: function(){

            var form = document.getElementById('company-form');

            if (form.checkValidity() === true) {
                this.closeModal();
                this.postForm();
            }
            form.classList.add('was-validated');

        },

        fetchCompanies: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/admin/companies', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.companies = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        postForm: function(){
            
            var apiKey = this.apiKey;

            payload = this.$get("company");

            waitingDialog.show('Sending');

            if (this.edit){

                var id = this.editID;
                this.$http.put('/api/admin/companies/' + id, payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        this.fetchCompanies();
                        this.resetCompany();
                        waitingDialog.hide();
                    },
                    function (err) {
                        console.log(err);
                });
            }
            else {
                this.$http.post('/api/admin/companies', payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        this.fetchCompanies();
                        this.resetCompany()
                        waitingDialog.hide();
                    },
                    function (err) {
                        console.log(err);
                });

            }
            
        },

        resetForm: function(){
            
            var form = document.getElementById('company-form');
            form.classList.remove("was-validated");
        },

        editCompany: function(index){

            var data = {
                name: this.companies[index].name,
                website: this.companies[index].website,
                user: this.companies[index].user,
                password: this.companies[index].password
            };
            
            this.company = data;
            this.edit = true;
            this.editID = this.companies[index].id;
        },

        resetCompany: function(){
            
            var data = {
                company: "",
                website: "",
                user: "",
                password: ""
            };

            this.company = data;

            this.edit = false;
            this.editID = null;

            this.resetForm();
        },

        deleteCompany: function(index){
           
            var id = this.companies[index].id;
            var apiKey = this.apiKey;
            var self = this;
            
            bootbox.confirm({
                message: "Do you want to delete this company?",
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

                        self.$http.delete('/api/admin/companies/' + id, {headers: {'X-API-KEY': apiKey}})
                            .then(function (res) {
                                self.fetchCompanies();
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