// company-detail-app.js

var company_vm = new Vue({
    el: '#company-detail-app',

    data: {
        apiKey: null,
        companyId: null,

        company: {
        },

        view_password: false
        
    },

    ready: function(){
        this.fetchCompany();
    },

    methods: {

        setKey: function(key){
            this.apiKey = key;
        },
        
        togglePassword: function(){
            this.view_password = !this.view_password;
        },

        fetchCompany: function(){
            var apiKey = this.apiKey;
            var companyId = this.companyId;

            this.$http.get('/api/company/companies/' + companyId, {headers: {'X-API-KEY': apiKey}})
                .then(function (res){
                    this.company = res.data;
                }, function(err){
                    console.log(err);
                })
        },
    }
})