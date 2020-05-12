// manager-order-app.js

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
            location.href = "/manager/companies/" + id;
        },

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

            this.$http.get('/api/manager/orders/' + id, {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.order = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        resetComment: function(){

            this.comment_text = "";

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

        submitOrder: function(){

            var apiKey = this.apiKey;
            var id = this.order.id;
            
            var payload = {picture: true};

            waitingDialog.show('Sending');

            this.$http.post('/api/manager/orders/' + id + "/submit", payload, {headers: {'X-API-KEY': apiKey}})
                .then(function (res) {
                    this.order.picture = res.data;
                    this.fetchAll();
                    waitingDialog.hide();
                    bootbox.alert("Order Submitted!");
                },
                function (err) {
                    console.log(err);
            });

        }
    }
})