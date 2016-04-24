(function () {
    Ember.TEMPLATES['defaultItemContainer'] = Ember.Handlebars.compile("{{text}}");
    Ember.TEMPLATES['components/gamily-matrix'] = Ember.Handlebars.compile('' +
        '{{table-component columnsBinding="columns" contentBinding="content" hasFooter=false isSortable=true}}' +
        '');

    var GamilyMatrixComponent = Ember.Component.extend({
        ajaxURL: '_some_default_path_if_gets_overwrite_',
        ajaxResponse: 'will_come_from_API',
        requestSent: false,
        requestFinished: false,
        getData: "{}",
        numColumns: 2,
        variable: "",
        imgPath: "http://127.0.0.1:5000/badges/static/",
        selectContentInRequest: function (response) {
            path = this.get('variable');
            if(path != "") {
                path_ = path.split(".");
                for(var i=0; i<path_.length; ++i){
                    response = response[path_[i]];
                }
            }
            return response;
        },
        columns: function() {
            if(this.get('requestSent') == false) {
                this.toggleProperty('requestSent');
                this.fetchData();
            }
            if(this.get('requestFinished') == false) {
                return [];
            }
            columnsData = this.get('columns_data');
            if(columnsData === undefined) {
                return [];
            }
            return columnsData
        }.property('columns_data'),
        content: function() {
            contentData = this.get('content_data');
            if(contentData === undefined) {
                return [];
            }
            return contentData;
        }.property('content_data'),
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
        }.observes('ajaxURL'),
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
        },
        processData: function() {
            response = this.get('ajaxResponse');
            leaderBoardData = this.selectContentInRequest(response);
            this.createColumns(leaderBoardData[0]);
            this.createContent(leaderBoardData);
            this.toggleProperty('requestFinished');
        }.observes('ajaxResponse'),
        createColumns: function(dataSingleRow) {
            var output = [];
            var parent = this;
            var numColumns = this.get('numColumns');
            for(var i=0; i<numColumns; i++) {
                var col = Ember.Table.ColumnDefinition.create({
                    textAlign: 'text-align-center',
                    headerCellName: '',
                    myNumber: i,
                    getCellContent: function(row) {
                        var rowContent = row.get('content');
                        var myCell = rowContent[this.get('myNumber')];
                        if('image_name' in myCell) {
                            if (myCell['k']=='1')
                            return {
                                'imgLink': parent.get('imgPath') + myCell['image_name'],
                                'style': 'width:24px;height:24px;',
                                'exist': true
                            }
                            else
                                return {
                                'imgLink': parent.get('imgPath') + myCell['image_name'],
                                'style': 'width:24px;height:24px;background:black',
                                'exist': true
                            }
                        }
                        else {
                            return {
                                'exist': false
                            }
                        }
                    },
                    tableCellViewClass: Ember.Table.TableCell.extend({
                        template: Em.Handlebars.compile('' +
                        '{{#if "view.cellContent.exist"}}' +
                        '   <img  {{bind-attr src="view.cellContent.imgLink"}} {{bind-attr style=view.cellContent.style}}">' +
                        '{{/if}}' +
                        '')
                    })
                });
                output.push(col);
            }
            this.set('columns_data', output);
        },
        createContent: function(data) {
            var matrix_form = [];
            var current_cell = [];
            var numColumns = this.get('numColumns');
            console.log(data);
            var left_elements = data.length;
            while(left_elements) {
                var current_row = [];
                for (var i = 0; i < numColumns; i++) {
                    if (left_elements) {
                        current_cell = data[left_elements - 1];
                        left_elements -= 1;
                    }
                    else {
                        current_cell = {}
                    }
                    current_row.push(current_cell);
                }
                matrix_form.push(current_row);
            }
            console.log(matrix_form);
            this.set('content_data', matrix_form);
        },
        capitalize: function(string){
            return string.replace( /(^|\s)([a-z])/g , function(m,p1,p2){ return p1+p2.toUpperCase(); } );
        }
    });

    Ember.Application.initializer({
        name:"gamily-matrix",
        initialize:function (container, application) {
            container.register('component:gamily-matrix', GamilyMatrixComponent);
        }
    });
})();