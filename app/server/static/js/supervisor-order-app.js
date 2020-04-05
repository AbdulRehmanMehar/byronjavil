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

        postAttachment: function(file){
            
            var apiKey = this.apiKey;
            var id = this.orderId;

            var reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = function () {
                console.log(reader.result);
            };
            reader.onerror = function (error) {
                console.log('Error: ', error);
            };

            console.log(file);

            payload = file;

            waitingDialog.show('Sending');

            this.$http.put('/api/attachment/order/' + id, payload, {headers: {'X-API-KEY': apiKey}})
                .then(function (res) {
                    this.fetchAttachments();
                    this.resetAttachment();
                    waitingDialog.hide();
                },
                function (err) {
                    console.log(err);
            });
            
        }
    }
})