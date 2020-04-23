// user-app.js

const user_options = {
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
        "username",
        "email",
        "role.role"
    ]
};

var users_vm = new Vue({
    el: '#users-app',

    data: {
        visible: true,
        users: [],
        apiKey: null,
        search: "",

        user: {
            username: "",
            password: "",
            email: "",
            role: "RESEARCH",
        },

        edit: false,
        editUsername: null,

        newPassword: ""
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

        closePasswordModal: function(){
            $('#user-password').modal('hide');
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

        updatePassword: function(){

            var form = document.getElementById('password-form');

            if (form.checkValidity() === true) {
                this.closePasswordModal();
                this.postPassword();
            }

            form.classList.add('was-validated');
        
        },

        fetchUsers: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/admin/users', {headers: {'X-API-KEY': apiKey}})
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
                this.$http.put('/api/admin/users/' + username, payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        this.fetchUsers();
                        this.resetUser();
                        waitingDialog.hide();
                    },
                    function (err) {
                        console.log(err);
                });
            }
            else {
                this.$http.post('/api/admin/users', payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        this.fetchUsers();
                        this.resetUser();
                        waitingDialog.hide();
                    },
                    function (err) {
                        console.log(err);
                });

            }
            
        },

        postPassword: function(){
            
            var apiKey = this.apiKey;

            payload = {};

            payload.username = this.editUsername;
            payload.password = this.newPassword;

            waitingDialog.show('Sending');

            this.$http.post('/api/admin/users/change-password', payload, {headers: {'X-API-KEY': apiKey}})
                .then(function (res) {
                    this.fetchUsers();
                    this.resetUser();
                    waitingDialog.hide();
                },
                function (err) {
                    console.log(err);
            });
            
        },

        resetForm: function(){
            
            var form = document.getElementById('user-form');
            form.classList.remove("was-validated");
        },

        resetPasswordForm: function(){
            
            var form = document.getElementById('password-form');
            form.classList.remove("was-validated");
        },

        editUser: function(index){

            this.users.every(function(item, _index){
                if (item.id == index){
                    index = _index;
                    return false;
                }
                return true;
            });

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
            this.newPassword = "";

            this.resetForm();
            this.resetPasswordForm();
        },

        changePassword: function(index){

            this.users.every(function(item, _index){
                if (item.id == index){
                    index = _index;
                    return false;
                }
                return true;
            });

            this.editUsername = this.users[index].username;
        },

        deleteUser: function(index){

            this.users.every(function(item, _index){
                if (item.id == index){
                    index = _index;
                    return false;
                }
                return true;
            });
           
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
    },

    filters: {
        fuzzySearch: function(values, role){
            var pattern = this.search;

            if (role == 'users'){
                var options = user_options;
            }

            if (pattern == ""){
                return values;
            }
            console.log(values);

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
