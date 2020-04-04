// data-order-app.js

var vm = new Vue({

    el: '#app',

    data: {
        apiKey: null,
        username: null,

        orderId: null,
        order: {},
        comments: [],
        attachments: [],
    },

    ready: function(){

    },

    methods: {

        // Fetch methods
        fetchOrder: function(){
            var apiKey = this.apiKey;
            var id = this.orderId;

            this.$http.get('api/data/orders/' + id, {headers: {'X-API-KEY': apiKey}})
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

        // Post methods
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

        markCompleted: function(){
            
        }
        // Put methods

    }
})