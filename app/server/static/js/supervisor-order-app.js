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
        this.fetchOrder();
        this.resetAttachment();
        this.fetchAttachments();
        this.fetchComments();
        this.resetAttachment();
    },

    methods: {

        downloadAll: function(){
            var id = this.order.id;
            location.href = "/attachment/" + id + "/download-all";
        },

        fetchAll: function(){
            this.fetchOrder();
            this.fetchAttachments();
            this.fetchComments();
        },

        fetchOrder: function(){
            var apiKey = this.apiKey;
            var id = this.orderId;

            this.$http.get('/api/supervisor/orders/' + id, {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.order = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        fetchComments: function(){
            var apiKey = this.apiKey;
            var id = this.orderId;

            this.$http.get('/api/comment/order/' + id, {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.comments = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        fetchAttachments: function(){
            var apiKey = this.apiKey;
            var id = this.orderId;

            this.$http.get('/api/attachment/order/' + id, {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.attachments = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        resetAttachment: function(){
            var fileInput = $("#input-b8").fileinput("reset");
        },

        postComment: function(){
            var apiKey = this.apiKey;
            var id = this.orderId;

            payload = {text: this.comment_text};

            waitingDialog.show('Sending');

            this.$http.post('/api/comment/order/' + id, payload, {headers: {'X-API-KEY': apiKey}})
                .then(function (res) {
                    this.fetchComments();
                    this.resetComment();
                    waitingDialog.hide();
                },
                function (err) {
                    console.log(err);
            });
            
        },

        resetComment: function(){

            this.comment_text = "";

        },

        postAttachment: function(file){
            
            var apiKey = this.apiKey;
            var id = this.orderId;
            
            var filename = file.name.replace(/^.*[\\\/]/, '').split('.').slice(0, -1).join('.');
            self = this;

            var reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = function () {
                
                var result = reader.result;
                var chunks = result.split(";");
                var filetype = chunks[0].split("/")[1].split(";")[0]
                var base64 = chunks[1].replace("base64,", "");

                var payload = {
                    filename: filename,
                    filetype: filetype,
                    base64: base64
                };

                waitingDialog.show('Sending');

                self.$http.post('/api/attachment/order/' + id, payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        self.fetchAttachments();
                        self.resetAttachment();
                        waitingDialog.hide();
                        bootbox.alert("File uploaded successfully!");
                    },
                    function (err) {
                        console.log(err);
                });

            };
            reader.onerror = function (error) {
                console.log('Error: ', error);
            };
            
        },

        markPicture: function(){

            var apiKey = this.apiKey;
            var id = this.order.id;
            
            var payload = {picture: true};

            waitingDialog.show('Sending');

            this.$http.post('/api/data/supervisor/' + id + "/mark-picture", payload, {headers: {'X-API-KEY': apiKey}})
                .then(function (res) {
                    this.order.picture = res.data;
                    this.fetchAll();
                    waitingDialog.hide();
                    bootbox.alert("Order Picture Marked!");
                },
                function (err) {
                    console.log(err);
            });

        }
    }
})