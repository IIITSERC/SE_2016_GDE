(function () {
    Ember.TEMPLATES['defaultItemContainer'] = Ember.Handlebars.compile("{{text}}");
    Ember.TEMPLATES['components/gamily-list'] = Ember.Handlebars.compile('' +
        '<ul class="list-group">' +
            '{{#each data in dataList}}' +
            '<li class="list-group-item">Hello, {{data}}!</li>' +
            '{{/each}}' +
        '</ul>' +
    '');

    var GamilyListComponent = Ember.Component.extend({
        ajaxURL: '_some_default_path_if_gets_overwrite_',
        ajaxResponse: 'will_come_from_API',
        requestSent: false,
        requestFinished: false,
        getData: "{}",
        dataList: [],
        variable: "",
        selectContentInRequest: function () {
            response = this.get('ajaxResponse');
            path = this.get('variable');
            console.log(response);
            if(path != "") {
                path_ = path.split(".");
                for(var i=0; i<path_.length; ++i){
                    response = response[path_[i]];
                }
            }
            console.log(response);
            this.set('dataList',response);
        }.observes('ajaxResponse'),
        fetchData: function() {
            var parent = this;
            var success = function(data) {
                parent.set('ajaxResponse', data);
            };
            this.cAjax({
                type: 'GET',
                url: this.get('ajaxURL'),
                data: JSON.parse(this.get('getData')),
                success: success
            });
        }.observes('ajaxURL').on('init'),
        cAjax : function (obj) {
            return $.ajax({
                dataType: obj['dataType'] ? obj['dataType'] : "JSON",
                url: obj['url'],
                type: obj['type'] ? obj['type'] : "GET",
                data: obj['data'],
                retryCount: obj['retryCount'] ? obj['retryCount'] : 0,
                retryLimit: 10,
                success: function (data) {
                    if (typeof obj['success'] == 'function') {
                        obj['success'](data);
                    }
                },
                error: function (data) {
                    if (data.status > 498 && this.retryCount < this.retryLimit) {
                        obj['retryCount'] = obj['retryCount'] ? obj['retryCount'] + 1 : 1;
                        setTimeout(function () {
                            cAjax(obj);
                        }, 2000);
                    } else {
                        if (typeof obj['error'] == 'function') {
                            obj['error'](data);
                        }
                    }
                }

            });
        }
    });

    Ember.Application.initializer({
        name:"gamily-list",
        initialize:function (container, application) {
            container.register('component:gamily-list', GamilyListComponent);
        }
    });
})();