// research-type-app.js

var research_type_vm = new Vue({
    el: '#research-type-app',

    data: {
        visible: true,
        researchTypes: [],
        researchType: "",
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
            $('#research-type-create').modal('hide');
        },

        createResearchType: function(){

            var form = document.getElementById('research-type-form');

            if (form.checkValidity() === true) {
                this.closeModal();
                this.postForm();
            }
            form.classList.add('was-validated');

        },

        updateResearchType: function(){

            var form = document.getElementById('research-type-form');

            if (form.checkValidity() === true) {
                this.closeModal();
                this.postForm();
            }
            form.classList.add('was-validated');

        },

        fetchResearchTypes: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/admin/research-type', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.researchTypes = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        postForm: function(){
            
            var apiKey = this.apiKey;

            payload = {
                type: this.researchType
            };

            waitingDialog.show('Sending');

            if (this.edit){

                var id = this.editID;
                this.$http.put('/api/admin/research-type/' + id, payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        this.fetchResearchTypes();
                        this.resetResearchType()
                        waitingDialog.hide();
                    },
                    function (err) {
                        console.log(err);
                });
            }
            else {
                this.$http.post('/api/admin/research-type', payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        this.fetchResearchTypes();
                        this.resetResearchType()
                        waitingDialog.hide();
                    },
                    function (err) {
                        console.log(err);
                });

            }
            
        },

        resetForm: function(){
            
            var form = document.getElementById('research-type-form');
            form.classList.remove("was-validated");
        },

        editResearchType: function(index){
            this.researchType = this.researchTypes[index].research_type;
            this.edit = true;
            this.editID = this.researchTypes[index].id;
        },

        resetResearchType: function(){
            this.researchType = "";
            this.edit = false;
            this.editID = null;

            this.resetForm();
        },

        deleteResearchType: function(index){
           
            var id = this.researchTypes[index].id;
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

                        self.$http.delete('/api/admin/research-type/' + id, {headers: {'X-API-KEY': apiKey}})
                            .then(function (res) {
                                self.fetchResearchTypes();
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