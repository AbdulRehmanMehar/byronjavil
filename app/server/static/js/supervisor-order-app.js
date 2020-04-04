// supervisor-order-app.js

var order_vm = new Vue({
    el: '#app',

    data: {

        apiKey: null,
        username: null,
        
        orderId: null,
        order: {},
        comments: [],
        attachments: [],

        comment_text: "",
    },

    ready: function(){
    },

    methods: {

        resetComment: function(){
            this.comment_text = "";
        },

        closeModal: function(){
            $('#user-create').modal('hide');
        },

        fetchOrder: function(){
            var apiKey = this.apiKey;
            var id = this.orderId;

            this.$http.get('api/supervisor/orders/' + id, {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.users = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        fetchComments: function(){
            var apiKey = this.apiKey;
            var id = this.orderId;

            this.$http.get('api/comment/order/' + id, {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.users = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        fetchAttachments: function(){
            var apiKey = this.apiKey;
            var id = this.orderId;

            this.$http.get('api/attachment/order' + id, {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.users = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        postComment: function(){
            var apiKey = this.apiKey;
            var id = this.orderId;

            payload = {text: this.comment_text};

            waitingDialog.show('Sending');

            this.$http.put('/api/comment/order/' + id, payload, {headers: {'X-API-KEY': apiKey}})
                .then(function (res) {
                    this.fetchComments();
                    this.resetComment();
                    waitingDialog.hide();
                },
                function (err) {
                    console.log(err);
            });
            
        },

        postAttachment: function(){
            
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
            
        }
    }
})