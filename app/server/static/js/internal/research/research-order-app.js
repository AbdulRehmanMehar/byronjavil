// research-order-app.js

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
        this.fetchAll();
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

            this.$http.get('/api/research/orders/' + id, {headers: {'X-API-KEY': apiKey}})
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

        postListAttachment: function(files){
            var file = files.pop();

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
                        
                        waitingDialog.hide();
                        bootbox.alert("File "+ filename + " uploaded successfully!");
                        
                        window.setTimeout(function(){
                            bootbox.hideAll();
                        }, 750);
                        
                        if (files.length > 0){
                            self.postListAttachment(files);
                        } else {
                            self.fetchAttachments();
                            self.resetAttachment();
                            bootbox.alert("All Files were uploaded successfully!");
                        }
                            
                    },
                    function (err) {
                        console.log(err);
                });

            };
            reader.onerror = function (error) {
                console.log('Error: ', error);
            };
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

        deleteAttachment: function(index){

            var apiKey = this.apiKey;
            var attachment_id = this.attachments[index].uuid;
            
            waitingDialog.show('Sending');

            this.$http.delete('/api/attachment/delete/' + attachment_id, {headers: {'X-API-KEY': apiKey}})
                .then(function (res) {
                    this.fetchAttachments();
                    this.resetAttachment();
                    waitingDialog.hide();
                    bootbox.alert("File deleted successfully!");
                },
                function (err) {
                    waitingDialog.hide();
                    bootbox.alert("Unauthorized to delete this file!");
                    console.log(err);
            });

        },

        markCompleted: function(){

            var apiKey = this.apiKey;
            var id = this.order.id;

            var payload = {};
            
            var self = this;
            bootbox.confirm({
                message: "Do you want to mark this research as completed?",
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

                        self.$http.post('/api/research/orders/' + id + "/mark-completed", payload, {headers: {'X-API-KEY': apiKey}})
                            .then(function (res) {
                                self.fetchAll();
                                self.resetAttachment();
                                waitingDialog.hide();
                                bootbox.alert("Research Marked as Completed!");
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