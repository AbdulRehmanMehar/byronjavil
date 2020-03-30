// order-type-app.js

var order_type_vm = new Vue({
    el: '#order-type-app',

    data: {
        visible: true,
        orderTypes: [],
        orderType: "",
        apiKey: null,

        edit: false,
        editID: null,
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
            $('#order-type-create').modal('hide');
        },

        createOrderType: function(){

            var form = document.getElementById('order-type-form');

            if (form.checkValidity() === true) {
                this.closeModal();
                this.postForm();
            }
            form.classList.add('was-validated');

        },

        updateOrderType: function(){

            var form = document.getElementById('order-type-form');

            if (form.checkValidity() === true) {
                this.closeModal();
                this.postForm();
            }
            form.classList.add('was-validated');

        },

        fetchOrderTypes: function(){
            var apiKey = this.apiKey;

            this.$http.get('api/supervisor/order-type', {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.orderTypes = res.data;
                }, function(err){
                    console.log(err);
                })
        },

        postForm: function(){
            
            var apiKey = this.apiKey;

            payload = {
                type: this.orderType
            };

            waitingDialog.show('Sending');

            if (this.edit){

                var id = this.editID;
                this.$http.put('/api/supervisor/order-type/' + id, payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        this.fetchOrderTypes();
                        this.resetOrderType()
                        waitingDialog.hide();
                    },
                    function (err) {
                        console.log(err);
                });
            }
            else {
                this.$http.post('/api/supervisor/order-type', payload, {headers: {'X-API-KEY': apiKey}})
                    .then(function (res) {
                        this.fetchOrderTypes();
                        this.resetOrderType()
                        waitingDialog.hide();
                    },
                    function (err) {
                        console.log(err);
                });

            }
            
        },

        editOrderType: function(index){
            this.orderType = this.orderTypes[index].order_type;
            this.edit = true;
            this.editID = this.orderTypes[index].id;
        },

        resetOrderType: function(){
            this.orderType = "";
            this.edit = false;
            this.editID = null;
        },

        deleteOrderType: function(index){
           
            var id = this.orderTypes[index].id;
            var apiKey = this.apiKey;
            var self = this;
            
            bootbox.confirm({
                message: "Do you want to delete this item?",
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

                        self.$http.delete('/api/supervisor/order-type/' + id, {headers: {'X-API-KEY': apiKey}})
                            .then(function (res) {
                                self.fetchOrderTypes();
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