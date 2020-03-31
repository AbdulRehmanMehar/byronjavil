// user-app.js

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
        editUsername: null,
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
            this.editUsername = null;
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