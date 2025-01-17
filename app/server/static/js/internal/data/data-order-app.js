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
        this.fetchAll();
        this.resetAttachment();
    },

    methods: {

        initMap: function(){
            var uluru = {lat: this.order.latitude, lng: this.order.longitude};
            // The map, centered at Uluru
            var map = new google.maps.Map(
                document.getElementById('map'), {zoom: 10, center: uluru});
            // The marker, positioned at Uluru
            var marker = new google.maps.Marker({position: uluru, map: map});
        },

        viewCompanyDetails: function(){
            var id = this.order.company.id;
            location.href = "/data/companies/" + id;
        },

        fetchAll: function(){
            this.fetchOrder();
            this.fetchAttachments();
            this.fetchComments();  
        },

        downloadAll: function(){
            var id = this.order.id;
            location.href = "/attachment/" + id + "/download-all";
        },

        fetchOrder: function(){
            var apiKey = this.apiKey;
            var id = this.orderId;

            this.$http.get('/api/data/orders/' + id, {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.order = res.data;
                    this.initMap();
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
            var fileInput = $("#input-b5").fileinput("reset");
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

                self.$http.post('/api/data/orders/' + id + "/upload-picture", payload, {headers: {'X-API-KEY': apiKey}})
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

            var apiKey = this.apiKey;
            var id = this.order.id;

            var payload = {};

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
                                waitingDialog.hide();
                                bootbox.alert("Data Marked as Completed!");
                            },
                            function (err) {
                                console.log(err);
                        });
                    }
                }
            });
        },

        markPicture: function(){

            var apiKey = this.apiKey;
            var id = this.order.id;
            
            var payload = {picture: true};

            waitingDialog.show('Sending');

            this.$http.post('/api/data/orders/' + id + "/mark-picture", payload, {headers: {'X-API-KEY': apiKey}})
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

