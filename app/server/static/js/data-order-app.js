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

        comment_text: "",
    },

    ready: function(){
        this.fetchOrder();
        this.fetchAttachments();
        this.fetchComments();
    },

    methods: {

        fetchOrder: function(){
            var apiKey = this.apiKey;
            var id = this.orderId;

            this.$http.get('/api/data/orders/' + id, {headers: {'X-API-KEY': apiKey}})
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

        resetComment: function(){

            this.comment_text = "";

        },

        postPicture: function(file){
            
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

                self.$http.post('/api/data/order/' + id + "/upload-picture", payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        self.fetchAttachments();
                        self.resetAttachment();
                        waitingDialog.hide();
                        bootbox.alert("Picture uploaded successfully!");
                    },
                    function (err) {
                        console.log(err);
                });

            };
            reader.onerror = function (error) {
                console.log('Error: ', error);
            };
        },

        markCompleted: function(){
            var self = this;
            bootbox.confirm({
                message: "Do you want to mark this data entry as completed?",
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
                    if (result){

                        waitingDialog.show('Sending');

                        self.$http.post('/api/data/orders/' + id + "/mark-completed", payload, {headers: {'X-API-KEY': apiKey}})
                            .then(function (res) {
                                self.fetchAll();
                                self.resetAttachment();
                                waitingDialog.hide();
                                bootbox.alert("Data Marked as Completed!");
                            },
                            function (err) {
                                console.log(err);
                        });
                    }
                }
            });
        }

    }
})