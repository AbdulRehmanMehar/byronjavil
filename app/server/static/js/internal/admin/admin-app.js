// admin-app.js

var vm = new Vue({

    el: '#app',

    data: {
        apiKey: null,
        username: null,
        
        types: [],

        order_type: "",
        company: {},
        order: {},
    },

    ready: function(){
        order_type_vm.setKey(this.apiKey);
        research_type_vm.setKey(this.apiKey);
        users_vm.setKey(this.apiKey);
        client_code_vm.setKey(this.apiKey);
        companies_vm.setKey(this.apiKey);
        
        order_type_vm.fetchOrderTypes();
        research_type_vm.fetchResearchTypes();
        users_vm.fetchUsers();
        client_code_vm.fetchClientCodes();
        companies_vm.fetchCompanies();
        
        this.show('order-type');
    },

    methods: {

        show: function(app){
            this.hide();
            
            if (app == 'order-type'){
                order_type_vm.show();
            }

            if (app == 'research-type'){
                research_type_vm.show();
            }

            if (app == 'users'){
                users_vm.show();
            }

            if (app == 'client-code'){
                client_code_vm.show();
            }

            if (app == 'companies'){
                companies_vm.show();
            }

        },

        hide: function(){
            order_type_vm.hide();
            research_type_vm.hide();
            users_vm.hide();
            client_code_vm.hide();
            companies_vm.hide();
        }

    }
})