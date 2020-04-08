// client-code-app.js

var client_code_vm = new Vue({
    el: '#client-code-app',

    data: {
        visible: true,
        clientCodes: [],
        clientCode: "",
        apiKey: null,

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
            $('#client-code-create').modal('hide');
        },

        createClientCode: function(){

            var form = document.getElementById('client-code-form');

            if (form.checkValidity() === true) {
                this.closeModal();
                this.postForm();
            }
            form.classList.add('was-validated');

        },

        updateClientCode: function(){

            var form = document.getElementById('client-code-form');

            if (form.checkValidity() === true) {
                this.closeModal();
                this.postForm();
            }
            form.classList.add('was-validated');

        },

        fetchClientCodes: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/admin/client-code', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.clientCodes = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        postForm: function(){
            
            var apiKey = this.apiKey;

            payload = {
                code: this.clientCode
            };

            waitingDialog.show('Sending');

            if (this.edit){

                var id = this.editID;
                this.$http.put('/api/admin/client-code/' + id, payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        this.fetchClientCodes();
                        this.resetClientCode()
                        waitingDialog.hide();
                    },
                    function (err) {
                        console.log(err);
                });
            }
            else {
                this.$http.post('/api/admin/client-code', payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        this.fetchClientCodes();
                        this.resetClientCode()
                        waitingDialog.hide();
                    },
                    function (err) {
                        console.log(err);
                });

            }
            
        },

        resetForm: function(){
            
            var form = document.getElementById('client-code-form');
            form.classList.remove("was-validated");
        },

        editClientCode: function(index){
            this.clientCode = this.clientCodes[index].code;
            this.edit = true;
            this.editID = this.clientCodes[index].id;
        },

        resetClientCode: function(){
            this.clientCode = "";
            this.edit = false;
            this.editID = null;

            this.resetForm();
        },

        deleteClientCode: function(index){
           
            var id = this.clientCodes[index].id;
            var apiKey = this.apiKey;
            var self = this;
            
            bootbox.confirm({
                message: "Do you want to delete this item?",
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

                        self.$http.delete('/api/admin/client-code/' + id, {headers: {'X-API-KEY': apiKey}})
                            .then(function (res) {
                                self.fetchClientCodes();
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