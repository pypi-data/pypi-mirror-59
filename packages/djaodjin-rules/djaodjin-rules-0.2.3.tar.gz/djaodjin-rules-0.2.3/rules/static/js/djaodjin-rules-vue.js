Vue.directive('sortable', {
  inserted: function (el, binding) {
    new Sortable(el, binding.value || {})
  }
})

var DATE_FORMAT = 'MMM DD, YYYY';


var httpRequestMixin = {
    // basically a wrapper around jQuery ajax functions
    methods: {
        _isFunction: function (func){
            // https://stackoverflow.com/a/7356528/1491475
            return func && {}.toString.call(func) === '[object Function]';
        },

        _isObject: function (obj) {
            // https://stackoverflow.com/a/46663081/1491475
            return obj instanceof Object && obj.constructor === Object
        },

        _getAuthToken: function() {
            return null; // XXX NotYetImplemented
        },

        _csrfSafeMethod: function(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        },

        _getCSRFToken: function() {
            var vm = this;
            // Look first for an input node in the HTML page, i.e.
            // <input type="hidden" name="csrfmiddlewaretoken"
            //     value="{{csrf_token}}">
            var crsfNode = vm.$el.querySelector("[name='csrfmiddlewaretoken']");
            if( crsfNode ) {
                return crsfNode.value;
            }
            // Then look for a CSRF token in the meta tags, i.e.
            // <meta name="csrf-token" content="{{csrf_token}}">
            var metas = document.getElementsByTagName('meta');
            for( var i = 0; i < metas.length; i++) {
                if (metas[i].getAttribute("name") == "csrf-token") {
                    return metas[i].getAttribute("content");
                }
            }
            return "";
        },

        /** This method generates a GET HTTP request to `url` with a query
            string built of a `queryParams` dictionnary.

            It supports the following prototypes:

            - reqGet(url, successCallback)
            - reqGet(url, queryParams, successCallback)
            - reqGet(url, queryParams, successCallback, failureCallback)
            - reqGet(url, successCallback, failureCallback)

            `queryParams` when it is specified is a dictionnary
            of (key, value) pairs that is converted to an HTTP
            query string.

            `successCallback` and `failureCallback` must be Javascript
            functions (i.e. instance of type `Function`).
        */
        reqGet: function(url, arg, arg2, arg3){
            var vm = this;
            var queryParams, successCallback;
            var failureCallback = showErrorMessages;
            if(typeof url != 'string') throw 'url should be a string';
            if(vm._isFunction(arg)){
                // We are parsing reqGet(url, successCallback)
                // or reqGet(url, successCallback, errorCallback).
                successCallback = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqGet(url, successCallback, errorCallback)
                    failureCallback = arg2;
                } else if( arg2 !== undefined ) {
                    throw 'arg2 should be a failureCallback function';
                }
            } else if(vm._isObject(arg)){
                // We are parsing
                // reqGet(url, queryParams, successCallback)
                // or reqGet(url, queryParams, successCallback, errorCallback).
                queryParams = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqGet(url, queryParams, successCallback)
                    // or reqGet(url, queryParams, successCallback, errorCallback).
                    successCallback = arg2;
                    if(vm._isFunction(arg3)){
                        // We are parsing reqGet(url, queryParams, successCallback, errorCallback)
                        failureCallback = arg3;
                    } else if( arg3 !== undefined ){
                        throw 'arg3 should be a failureCallback function';
                    }
                } else {
                    throw 'arg2 should be a successCallback function';
                }
            } else {
                throw 'arg should be a queryParams Object or a successCallback function';
            }
            return $.ajax({
                method: 'GET',
                url: url,
                beforeSend: function(xhr, settings) {
                    var authToken = vm._getAuthToken();
                    if( authToken ) {
                        xhr.setRequestHeader("Authorization",
                            "Bearer " + authToken);
                    } else {
                        if( !vm._csrfSafeMethod(settings.type) ) {
                            var csrfToken = vm._getCSRFToken();
                            if( csrfToken ) {
                                xhr.setRequestHeader("X-CSRFToken", csrfToken);
                            }
                        }
                    }
                },
                data: queryParams,
                traditional: true,
                cache: false,       // force requested pages not to be cached
           }).done(successCallback).fail(failureCallback);
        },
        /** This method generates a POST HTTP request to `url` with
            contentType 'application/json'.

            It supports the following prototypes:

            - reqPOST(url, data)
            - reqPOST(url, data, successCallback)
            - reqPOST(url, data, successCallback, failureCallback)
            - reqPOST(url, successCallback)
            - reqPOST(url, successCallback, failureCallback)

            `data` when it is specified is a dictionnary of (key, value) pairs
            that is passed as a JSON encoded body.

            `successCallback` and `failureCallback` must be Javascript
            functions (i.e. instance of type `Function`).
        */
        reqPost: function(url, arg, arg2, arg3){
            var vm = this;
            var data, successCallback;
            var failureCallback = showErrorMessages;
            if(typeof url != 'string') throw 'url should be a string';
            if(vm._isFunction(arg)){
                // We are parsing reqPost(url, successCallback)
                // or reqPost(url, successCallback, errorCallback).
                successCallback = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqPost(url, successCallback, errorCallback)
                    failureCallback = arg2;
                } else if (arg2 !== undefined){
                    throw 'arg2 should be a failureCallback function';
                }
            } else if(vm._isObject(arg)){
                // We are parsing reqPost(url, data)
                // or reqPost(url, data, successCallback)
                // or reqPost(url, data, successCallback, errorCallback).
                data = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqPost(url, data, successCallback)
                    // or reqPost(url, data, successCallback, errorCallback).
                    successCallback = arg2;
                    if(vm._isFunction(arg3)){
                        // We are parsing reqPost(url, data, successCallback, errorCallback)
                        failureCallback = arg3;
                    } else if (arg3 !== undefined){
                        throw 'arg3 should be a failureCallback function';
                    }
                } else if (arg2 !== undefined){
                    throw 'arg2 should be a successCallback function';
                }
            } else if (arg !== undefined){
                throw 'arg should be a data Object or a successCallback function';
            }
            return $.ajax({
                method: 'POST',
                url: url,
                beforeSend: function(xhr, settings) {
                    var authToken = vm._getAuthToken();
                    if( authToken ) {
                        xhr.setRequestHeader("Authorization",
                            "Bearer " + authToken);
                    } else {
                        if( !vm._csrfSafeMethod(settings.type) ) {
                            var csrfToken = vm._getCSRFToken();
                            if( csrfToken ) {
                                xhr.setRequestHeader("X-CSRFToken", csrfToken);
                            }
                        }
                    }
                },
                contentType: 'application/json',
                data: JSON.stringify(data),
            }).done(successCallback).fail(failureCallback);
        },
        /** This method generates a PUT HTTP request to `url` with
            contentType 'application/json'.

            It supports the following prototypes:

            - reqPUT(url, data)
            - reqPUT(url, data, successCallback)
            - reqPUT(url, data, successCallback, failureCallback)
            - reqPUT(url, successCallback)
            - reqPUT(url, successCallback, failureCallback)

            `data` when it is specified is a dictionnary of (key, value) pairs
            that is passed as a JSON encoded body.

            `successCallback` and `failureCallback` must be Javascript
            functions (i.e. instance of type `Function`).
        */
        reqPut: function(url, arg, arg2, arg3){
            var vm = this;
            var data, successCallback;
            var failureCallback = showErrorMessages;
            if(typeof url != 'string') throw 'url should be a string';
            if(vm._isFunction(arg)){
                // We are parsing reqPut(url, successCallback)
                // or reqPut(url, successCallback, errorCallback).
                successCallback = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqPut(url, successCallback, errorCallback)
                    failureCallback = arg2;
                } else if (arg2 !== undefined){
                    throw 'arg2 should be a failureCallback function';
                }
            } else if(vm._isObject(arg)){
                // We are parsing reqPut(url, data)
                // or reqPut(url, data, successCallback)
                // or reqPut(url, data, successCallback, errorCallback).
                data = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqPut(url, data, successCallback)
                    // or reqPut(url, data, successCallback, errorCallback).
                    successCallback = arg2;
                    if(vm._isFunction(arg3)){
                        // We are parsing reqPut(url, data, successCallback, errorCallback)
                        failureCallback = arg3;
                    } else if (arg3 !== undefined){
                        throw 'arg3 should be a failureCallback function';
                    }
                } else if (arg2 !== undefined){
                    throw 'arg2 should be a successCallback function';
                }
            } else if (arg !== undefined){
                throw 'arg should be a data Object or a successCallback function';
            }

            return $.ajax({
                method: 'PUT',
                url: url,
                beforeSend: function(xhr, settings) {
                    var authToken = vm._getAuthToken();
                    if( authToken ) {
                        xhr.setRequestHeader("Authorization",
                            "Bearer " + authToken);
                    } else {
                        if( !vm._csrfSafeMethod(settings.type) ) {
                            var csrfToken = vm._getCSRFToken();
                            if( csrfToken ) {
                                xhr.setRequestHeader("X-CSRFToken", csrfToken);
                            }
                        }
                    }
                },
                contentType: 'application/json',
                data: JSON.stringify(data),
            }).done(successCallback).fail(failureCallback);
        },
        /** This method generates a PATCH HTTP request to `url` with
            contentType 'application/json'.

            It supports the following prototypes:

            - reqPATCH(url, data)
            - reqPATCH(url, data, successCallback)
            - reqPATCH(url, data, successCallback, failureCallback)
            - reqPATCH(url, successCallback)
            - reqPATCH(url, successCallback, failureCallback)

            `data` when it is specified is a dictionnary of (key, value) pairs
            that is passed as a JSON encoded body.

            `successCallback` and `failureCallback` must be Javascript
            functions (i.e. instance of type `Function`).
        */
        reqPatch: function(url, arg, arg2, arg3){
            var vm = this;
            var data, successCallback;
            var failureCallback = showErrorMessages;
            if(typeof url != 'string') throw 'url should be a string';
            if(vm._isFunction(arg)){
                // We are parsing reqPatch(url, successCallback)
                // or reqPatch(url, successCallback, errorCallback).
                successCallback = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqPatch(url, successCallback, errorCallback)
                    failureCallback = arg2;
                } else if (arg2 !== undefined){
                    throw 'arg2 should be a failureCallback function';
                }
            } else if(vm._isObject(arg)){
                // We are parsing reqPatch(url, data)
                // or reqPatch(url, data, successCallback)
                // or reqPatch(url, data, successCallback, errorCallback).
                data = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqPatch(url, data, successCallback)
                    // or reqPatch(url, data, successCallback, errorCallback).
                    successCallback = arg2;
                    if(vm._isFunction(arg3)){
                        // We are parsing reqPatch(url, data, successCallback, errorCallback)
                        failureCallback = arg3;
                    } else if (arg3 !== undefined){
                        throw 'arg3 should be a failureCallback function';
                    }
                } else if (arg2 !== undefined){
                    throw 'arg2 should be a successCallback function';
                }
            } else if (arg !== undefined){
                throw 'arg should be a data Object or a successCallback function';
            }

            return $.ajax({
                method: 'PATCH',
                url: url,
                beforeSend: function(xhr, settings) {
                    var authToken = vm._getAuthToken();
                    if( authToken ) {
                        xhr.setRequestHeader("Authorization",
                            "Bearer " + authToken);
                    } else {
                        if( !vm._csrfSafeMethod(settings.type) ) {
                            var csrfToken = vm._getCSRFToken();
                            if( csrfToken ) {
                                xhr.setRequestHeader("X-CSRFToken", csrfToken);
                            }
                        }
                    }
                },
                contentType: 'application/json',
                data: JSON.stringify(data),
            }).done(successCallback).fail(failureCallback);
        },
        /** This method generates a DELETE HTTP request to `url` with a query
            string built of a `queryParams` dictionnary.

            It supports the following prototypes:

            - reqDELETE(url)
            - reqDELETE(url, successCallback)
            - reqDELETE(url, successCallback, failureCallback)

            `successCallback` and `failureCallback` must be Javascript
            functions (i.e. instance of type `Function`).
        */
        reqDelete: function(url, arg, arg2){
            var vm = this;
            var data, successCallback;
            var failureCallback = showErrorMessages;
            if(typeof url != 'string') throw 'url should be a string';
            if(vm._isFunction(arg)){
                // We are parsing reqDelete(url, successCallback)
                // or reqDelete(url, successCallback, errorCallback).
                successCallback = arg;
                if(vm._isFunction(arg2)){
                    // We are parsing reqDelete(url, successCallback, errorCallback)
                    failureCallback = arg2;
                } else if (arg2 !== undefined){
                    throw 'arg2 should be a failureCallback function';
                }
            } else if (arg !== undefined){
                throw 'arg should be a successCallback function';
            }

            return $.ajax({
                method: 'DELETE',
                url: url,
                beforeSend: function(xhr, settings) {
                    var authToken = vm._getAuthToken();
                    if( authToken ) {
                        xhr.setRequestHeader("Authorization",
                            "Bearer " + authToken);
                    } else {
                        if( !vm._csrfSafeMethod(settings.type) ) {
                            var csrfToken = vm._getCSRFToken();
                            if( csrfToken ) {
                                xhr.setRequestHeader("X-CSRFToken", csrfToken);
                            }
                        }
                    }
                },
            }).done(successCallback).fail(failureCallback);
        },
    }
}


var itemListMixin = {
    data: function(){
        return this.getInitData();
    },
    mixins: [httpRequestMixin],
    methods: {
        getInitData: function(){
            data = {
                url: '',
                itemsLoaded: false,
                items: {
                    results: [],
                    count: 0
                },
                mergeResults: false,
                params: {
                    // The following dates will be stored as `String` objects
                    // as oppossed to `moment` or `Date` objects because this
                    // is how uiv-date-picker will update them.
                    start_at: null,
                    ends_at: null
                },
                getCb: null,
                getCompleteCb: null,
                getBeforeCb: null,
            }
            if( djaodjinSettings.date_range ) {
                if( djaodjinSettings.date_range.start_at ) {
                    data.params['start_at'] = moment(
                        djaodjinSettings.date_range.start_at).format(DATE_FORMAT);
                }
                if( djaodjinSettings.date_range.ends_at ) {
                    // uiv-date-picker will expect ends_at as a String
                    // but DATE_FORMAT will literally cut the hour part,
                    // regardless of timezone. We don't want an empty list
                    // as a result.
                    // If we use moment `endOfDay` we get 23:59:59 so we
                    // add a full day instead.
                    data.params['ends_at'] = moment(
                        djaodjinSettings.date_range.ends_at).add(1,'days').format(DATE_FORMAT);
                }
            }
            return data;
        },
        get: function(){
            var vm = this;
            if(!vm.url) return
            if(!vm.mergeResults){
                vm.itemsLoaded = false;
            }
            if(vm[vm.getCb]){
                var cb = function(res){
                    vm[vm.getCb](res);

                    if(vm[vm.getCompleteCb]){
                        vm[vm.getCompleteCb]();
                    }
                }
            } else {
                var cb = function(res){
                    if(vm.mergeResults){
                        res.results = vm.items.results.concat(res.results);
                    }
                    vm.items = res;
                    vm.itemsLoaded = true;

                    if(vm[vm.getCompleteCb]){
                        vm[vm.getCompleteCb]();
                    }
                }
            }
            if(vm[vm.getBeforeCb]){
                vm[vm.getBeforeCb]();
            }
            vm.reqGet(vm.url, vm.getParams(), cb);
        },
        getParams: function(excludes){
            var vm = this;
            var params = {};
            for( var key in vm.params ) {
                if( vm.params.hasOwnProperty(key) && vm.params[key] ) {
                    if( excludes && key in excludes ) continue;
                    if( key === 'start_at' || key === 'ends_at' ) {
                        params[key] = moment(vm.params[key], DATE_FORMAT).toISOString();
                    } else {
                        params[key] = vm.params[key];
                    }
                }
            }
            return params;
        },
        getQueryString: function(excludes){
            var vm = this;
            var sep = "";
            var result = "";
            var params = vm.getParams(excludes);
            for( var key in params ) {
                if( params.hasOwnProperty(key) ) {
                    result += sep + key + '=' + params[key].toString();
                    sep = "&";
                }
            }
            if( result ) {
                result = '?' + result;
            }
            return result;
        },
        humanizeTotal: function() {
            var vm = this;
            var filter = Vue.filter('humanizeCell');
            return filter(vm.items.total, vm.items.unit, 0.01);
        },
        humanizeBalance: function() {
            var vm = this;
            var filter = Vue.filter('humanizeCell');
            return filter(vm.items.balance, vm.items.unit, 0.01);
        },
    },
}

var itemMixin = {
    mixins: [httpRequestMixin],
    data: function() {
        return {
            item: {},
            itemLoaded: false,
        }
    },
    methods: {
        get: function(){
            var vm = this;
            if(!vm.url) return
            if(vm[vm.getCb]){
                var cb = vm[vm.getCb];
            } else {
                var cb = function(res){
                    vm.item = res
                    vm.itemLoaded = true;
                }
            }
            vm.reqGet(vm.url, cb);
        },
    },
}

var paginationMixin = {
    data: function(){
        return {
            params: {
                page: 1,
            },
            itemsPerPage: djaodjinSettings.itemsPerPage,
            getCompleteCb: 'getCompleted',
            getBeforeCb: 'resetPage',
            qsCache: null,
            isInfiniteScroll: false,
        }
    },
    methods: {
        resetPage: function(){
            var vm = this;
            if(!vm.ISState) return;
            if(vm.qsCache && vm.qsCache !== vm.qs){
                vm.params.page = 1;
                vm.ISState.reset();
            }
            vm.qsCache = vm.qs;
        },
        getCompleted: function(){
            var vm = this;
            if(!vm.ISState) return;
            vm.mergeResults = false;
            if(vm.pageCount > 0){
                vm.ISState.loaded();
            }
            if(vm.params.page >= vm.pageCount){
                vm.ISState.complete();
            }
        },
        paginationHandler: function($state){
            var vm = this;
            if(!vm.ISState) return;
            if(!vm.itemsLoaded){
                // this handler is triggered on initial get too
                return;
            }
            // rudimentary way to detect which type of pagination
            // is active. ideally need to monitor resolution changes
            vm.isInfiniteScroll = true;
            var nxt = vm.params.page + 1;
            if(nxt <= vm.pageCount){
                vm.$set(vm.params, 'page', nxt);
                vm.mergeResults = true;
                vm.get();
            }
        },
    },
    computed: {
        totalItems: function(){
            return this.items.count
        },
        pageCount: function(){
            return Math.ceil(this.totalItems / this.itemsPerPage)
        },
        ISState: function(){
            if(!this.$refs.infiniteLoading) return;
            return this.$refs.infiniteLoading.stateChanger;
        },
        qs: function(){
            return this.getQueryString({page: null});
        },
    }
}


Vue.component('rules-table', {
    mixins: [
        itemListMixin,
        paginationMixin,
    ],
    data: function(){
        return {
            url: djaodjinSettings.urls.rules.api_rules,
            itemsLoaded: false,
            items: {
                results: [],
                count: 0
            },
            params: {},
            ruleModalOpen: false,
            newRule: {
                path: '',
                rank: 0,
                is_forward: false,
            },
            edit_description: [],
        }
    },
    methods: {
        moved: function(e){
            var vm = this;
            var oldRank = vm.items.results[e.oldIndex].rank;
            var newRank = vm.items.results[e.newIndex].rank;
            var pos = [{oldpos: oldRank, newpos: newRank}];
            vm.reqPatch(vm.url, {"updates": pos},
            function (resp) {
// XXX The following does not update the rules as would be expected.
//     As a workaround, we call get() here.
//                vm.items = resp;
//                vm.itemsLoaded = true;
                vm.get();
            });
        },
        create: function(){
            var vm = this;
            vm.reqPost(vm.url, vm.newRule,
            function (resp) {
                vm.get();
                vm.newRule = {
                    path: '',
                    rank: 0,
                    is_forward: false,
                }
                vm.ruleModalOpen = false;
            },
            function(resp){
                vm.ruleModalOpen = false;
                showErrorMessages(resp);
            });
        },
        update: function(rule){
            var vm = this;
            vm.reqPut(vm.url + rule.path, rule,
            function (resp) {
                vm.ruleModalOpen = false;
            },
            function(resp){
                vm.ruleModalOpen = false;
                showErrorMessages(resp);
            });
        },
        remove: function(idx){
            var vm = this;
            var rule = vm.items.results[idx]
            vm.reqDelete(vm.url + rule.path,
            function (resp) {
                vm.params.page = 1;
                vm.get();
            });
        },
        editDescription: function(idx){
            var vm = this;
            vm.edit_description = Array.apply(
                null, new Array(vm.items.results.length)).map(function() {
                return false;
            });
            vm.$set(vm.edit_description, idx, true)
            // at this point the input is rendered and visible
            vm.$nextTick(function(){
                vm.$refs.edit_description_input[idx].focus();
            });
        },
        saveDescription: function(coupon, idx, event){
            if (event.which === 13 || event.type === "blur" ){
                this.$set(this.edit_description, idx, false)
                this.update(this.items.results[idx])
            }
        },
    },
    mounted: function(){
        this.get();
    }
});

// XXX Connects to bootstrap.js should be somewhere else.
$('#new-rule').on('shown.bs.modal', function(){
    var self = $(this);
    self.find('[name="new_rule_path"]').focus();
});


Vue.component('rule-list', {
    mixins: [
        itemMixin,
    ],
    data: function() {
        return {
            sessionKey: gettext('Generating...'),
            testUsername: '',
            forward_session: '',
            forward_session_header: '',
            forward_url: '',
        }
    },
    methods: {
        generateKey: function(){
            var vm = this;
            vm.reqPut(djaodjinSettings.urls.rules.api_generate_key,
            function (resp) {
                vm.sessionKey = resp.enc_key;
            },
            function(resp) {
                vm.sessionKey = gettext("ERROR");
                showErrorMessages(resp);
            });
        },
        getSessionData: function(){
            var vm = this;
            vm.reqGet(djaodjinSettings.urls.rules.api_session_data + "/" + vm.testUsername,
            function(resp) {
                vm.forward_session = resp.forward_session;
                vm.forward_session_header = resp.forward_session_header;
                vm.forward_url = resp.forward_url;
            });
        },
        update: function(submitEntryPoint) {
            var vm = this;
            var data = {
                authentication: vm.$refs.authentication.value,
                welcome_email: vm.$refs.welcomeEmail.checked,
                session_backend: vm.$refs.sessionBackend.value,
            }
            if( submitEntryPoint ) {
                data['entry_point'] = vm.$refs.entryPoint.value;
            }
            vm.reqPut(djaodjinSettings.urls.rules.api_detail, data,
            function (resp) {
                showMessages([gettext("Update successful.")], "success");
            });
        },
    },
});


Vue.component('user-engagement', {
    mixins: [
        itemListMixin,
    ],
    data: function() {
        return {
            url: djaodjinSettings.urls.rules.api_user_engagement,
        }
    },
    computed: {
        tags: function(){
            var tags = [];
            this.items.results.forEach(function(e){
                tags = tags.concat(e.engagements).filter(function(value, index, self){
                    return self.indexOf(value) === index;
                });
            });
            return tags;
        }
    },
    mounted: function(){
        this.get();
    },
});


Vue.component('user-aggregate-engagement', {
    mixins: [
        itemMixin
    ],
    data: function(){
        return {
            url: djaodjinSettings.urls.rules.api_engagement,
            getCb: 'getAndChart',
        }
    },
    methods: {
        getAndChart: function(res){
            var vm = this;
            vm.itemLoaded = true;
            vm.$set(vm.item, 'activeUsers', res.active_users);
            vm.$set(vm.item, 'engagements', res.engagements);
            var el = vm.$refs.engagementChart;

            // nvd3 is available on djaoapp
            if(vm.item.engagements.length === 0 || !el || !nv) return;

            nv.addGraph(function() {
                var data = [{
                    "key": "Engagements",
                    "values": vm.item.engagements.map(function(e){
                      return {
                        "label": e.slug,
                        "value" : e.count
                      }
                    })
                }];
                var chart = nv.models.multiBarHorizontalChart()
                    .x(function(d) { return d.label })
                    .y(function(d) { return d.value })
                    .barColor(nv.utils.defaultColor())
                    .showValues(true)
                    .showLegend(false)
                    .showControls(false)
                    .showXAxis(false)
                    .showYAxis(false)
                    .groupSpacing(0.02)
                    .margin({top: 0, right: 0, bottom: 0, left: 0});

                d3.select(el)
                    .datum(data)
                    .call(chart);

                // centering logic
                var height = parseInt(d3.select(".positive rect").attr('height'));
                var y = (height / 2) + 3; // 3 is a magic number
                // add labels inside bars
                d3.selectAll(".positive").append("text")
                    .style('fill', 'white')
                    .text(function(d){ return d.label })
                    .attr('x', '10')
                    .attr('y', y)

                chart.tooltip.enabled(false);

                nv.utils.windowResize(chart.update);

                return chart;
            });
        },
    },
    mounted: function(){
        this.get();
    }
});

