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

        },

        fetchComments: function(){

        },

        fetchAttachments: function(){

        },

        // Post methods
        pushComment: function(){

        },

        markCompleted: function(){
            
        }
        // Put methods

    }
})