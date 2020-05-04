// company-app.js

const company_options = {
    // isCaseSensitive: false,
    // findAllMatches: false,
    // includeMatches: false,
    // includeScore: false,
    // useExtendedSearch: false,
    // minMatchCharLength: 1,
    // shouldSort: true,
    // threshold:0.6,
    // location: 0,
    // distance: 100,
    keys: [
        "name",
        "website",
        "user"
    ]
};

var companies_vm = new Vue({
    el: '#companies-app',

    data: {
        visible: true,
        companies: [],
        apiKey: null,
        search: "", 

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

            this.$http.get('/api/admin/companies', {headers: {'X-API-KEY': apiKey}})
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

            this.companies.every(function(item, _index){
                if (item.id == index){
                    index = _index;
                    return false;
                }
                return true;
            });

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
            
            this.companies.every(function(item, _index){
                if (item.id == index){
                    index = _index;
                    return false;
                }
                return true;
            });

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
    },

    filters: {
        fuzzySearch: function(values){
            var pattern = this.search;

            var options = company_options;

            if (pattern == ""){
                return values;
            }

            var fuse = new Fuse(values, options);
            var matches = fuse.search(pattern);
            
            var output =  [];

            matches.forEach(function(value){
                output.push(value.item);
            });

            return output;
        }
    }
})