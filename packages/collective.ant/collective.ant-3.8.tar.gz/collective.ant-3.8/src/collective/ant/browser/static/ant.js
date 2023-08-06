/**
 * Filename: main.js
 * Version: 5.0
 * Date: 2019-03-1
 */

$(function () {
    "use strict";

    // data table
    // ==========
    /**
     * Datagridfield
     * Fill a table cell contents
     */
    // $.fn.dataTable.ext.errMode = 'throw';
    const $batch_list = $('table.datagridwidget-table-view');
    $batch_list.find('>thead>tr>th[class^="header cell-"]')
    //.slice(1,-1)
    // text-widget textline-field
        .on("dblclick", function (/*event*/) {
            // $(this).parent().children().index($(this))
            //var cellIndex = 2 + this.cellIndex;
            //var $cell_cols = $(this).closest("table").find("tbody>tr>td:nth-child(" + cellIndex + ")>input");
            const call_n = $(this).prop('class').match(/cell-\d+/)[0];
            const $cell_cols = $(this).closest("table").find("tbody>tr>td." + call_n + ">input");
            const $first_cell = $cell_cols.first();
            const first_value = $cell_cols.first().val();
            const position = -1;  // disabled! first_value.search(/(\d)+$/);
            let copy_value = true;

            if (position > -1) {
                copy_value = false;
                const prefix = first_value.slice(0, position);
                const suffix = first_value.slice(position);
            }
            $cell_cols.slice(1).each(function (index) {
                if (copy_value) {
                    this.value = first_value;
                } else {
                    this.value = prefix + (suffix - -1 + index);
                }
                // $(this).trigger('change');
            }).add($first_cell).effect("highlight");
        })
        // select-widget choice-field
        .on("dblclick", function (/*event*/) {
            const call_n = $(this).prop('class').match(/cell-\d+/)[0];
            // steps
            const $cell_cols = $(this).closest("table").find("tbody>tr>td." + call_n + " select.choice-field");
            const $first_cell = $cell_cols.first();
            const first_value = $cell_cols.first().val();
            $cell_cols.slice(1).each(function (index) {
                this.value = first_value;
            }).add($first_cell).effect("highlight");
        })
        // radio-widget choice-field
        .on("dblclick", function (/*event*/) {
            const call_n = $(this).prop('class').match(/cell-\d+/)[0];
            // radio button
            const $cell_cols = $(this).closest("table").find("tbody>tr>td." + call_n).has("span.option");
            const $first_cell = $cell_cols.first().find("input[type='radio']:checked");
            if ($first_cell.length === 1) {
                const first_value = $first_cell.first().val();
                $cell_cols.slice(1).each(function (index) {
                    $(this).find("input[type='radio'][value='" + first_value + "']").prop('checked', true);
                }).add($first_cell.closest("td." + call_n)).effect("highlight");
            }
        })
        // checkbox-widget choice-field
        .on("dblclick", function (/*event*/) {
            const call_n = $(this).prop('class').match(/cell-\d+/)[0];
            // radio button
            const $cell_cols = $(this).closest("table").find("tbody>tr>td." + call_n).has("span.option");
            const $first_cell = $cell_cols.first().find("input[type='checkbox']:checked");
            let checked_list = [];
            $first_cell.each(function(index){checked_list.push(this.value)});
            $cell_cols.slice(1).each(function (index) {
                const $checkbox = $cell_cols.find("input[type='checkbox']");
                $checkbox.each(function(index){
                   if ($.inArray(this.value, checked_list) === -1) {
                      $(this).prop('checked', false);
                   }
                   else {
                      $(this).prop('checked', true);
                   }
                });
            }).add($first_cell.closest("td." + call_n)).effect("highlight");
        })
        // datetime-widget datetime-field
        .on("dblclick", function (/*event*/) {
            const self = this;
            const call_n = $(this).prop('class').match(/cell-\d+/)[0];
            const year_month_day = ["year", "month", "day", "hour", "minute"];

            year_month_day.forEach(function (value, index, array) {
                const $cell_cols = $(self).closest("table").find("tbody>tr>td." + call_n + " select." + value);
                const $first_cell = $cell_cols.first();
                const first_value = $cell_cols.first().val();
                $cell_cols.slice(1).each(function (index) {
                    this.value = first_value;
                }).add($first_cell).effect("highlight");
            });

        })
        // ordered-selection-field
        .on("dblclick", function (/*event*/) {
            const call_n = $(this).prop('class').match(/cell-\d+/)[0];
            // multiple select
            const $cell_cols = $(this).closest("table").find("tbody>tr>td." + call_n).has("table.ordered-selection-field");
            const $first_cell = $cell_cols.first().find("select");
            // from widget, to widget
            if ($first_cell.length === 2) {
                const first_html = $first_cell.first().html();
                const last_html = $first_cell.last().html();
                $cell_cols.slice(1).each(function (index) {
                    // dummy values
                    $(this).find("select").first().html(first_html).triggerHandler('change');
                    $(this).find("select").last().html(last_html).triggerHandler('change');
                    // real values
                    $(this).find("select").last().html(last_html).filter(function () {
                        const $container = $("#" + this.id + "DataContainer");
                        const dataname = this.name.slice(0, -3) + ":list";
                        let content = '';
                        $(this).find('option').each(function () {
                            content += '<input name="' + dataname + '" type="hidden" value="' + this.value + '">';
                        });
                        $container.html(content);
                    }).triggerHandler('change');

                }).add($first_cell.closest("td." + call_n))
                    .effect("highlight").effect("highlight");
            }
        });

    // unique checked
    $batch_list.find('span[id]')
        .filter(function(index) {
            return $(this).prop('id').search('-widgets-transition_state')!==-1;
        })
        // .css('background-color', 'red')
        .on( "change", "input[type='checkbox']", function() {
            const checked = this;
            $(this).parentsUntil('tr.datagridwidget-row')
                // .css("background-color", "green")
                .find("input[type='checkbox']")
                .each(function (index) {
                    if (checked !== this) {
                      $(this).prop('checked', false);
                    }
                });
        });
});


window.addEventListener('load', event => {
    const import_form = document.querySelector('#ant-import-form');
    if (import_form) {
        import_form.addEventListener('submit', event => {
            $('#ProgressModal .progress-bar').addClass('add_slide_progress');
            $('#ProgressModal').modal('show');
        });
    }
});


$(function () {
    "use strict";
    /**
     * search data
     * @type {*|jQuery|HTMLElement}
     */
    const $single = $('#form-single-sample-add');
    if ($single.length) {
        const form_pre = '#form-single-sample-add-widgets-';

        // get sample id for project_type
        $(form_pre + 'project_type')
            .on('change', function (event) {
                // event.stopPropagation();
                event.preventDefault();
                // console.log(this, event);
                //console.info(event.target, event.currentTarget, event.delegateTarget, event.relatedTarget);
                const $sample_id = $(form_pre + 'sample_id');
                const $barcode = $(form_pre + 'barcode');
                // if ($sample_id.val() && $barcode.val()){
                //     return
                // }

                const action = $single.prop('action');
                let content_type = action.match(/^.*\/gene(?<name>\w*)-single-sample-addform$/).groups.name;
                content_type = content_type.replace(content_type[0],content_type[0].toUpperCase());
                // const project_type = this.value.trim();
                const project_type = this.selectedOptions[0].text;
                const portal_url = $('body').attr('data-portal-url');
                let request_url = portal_url + '/lis-next-sn';
                request_url += "?content_type=" + content_type;
                request_url += "&project_type=" + project_type;
                const request = $.ajax({
                    url: request_url,
                    method: "GET",
                    headers: {
                        "Accept": "application/json",
                        // "Content-Type": "application/json",
                        // "Authorization": "Basic YWRtaW46c2VjcmV0",
                    },
                    // contentType: "application/json",
                    // mimeType: "application/json",
                    // dataType: "json",
                    // data: {id : menuId},
                });

                request.done(function (data, textStatus, jqXHR) {
                    if (data.length === 2) {
                        if(data[0]){
                            $sample_id.val(data[0]);
                        }
                        if(data[1]){
                            $barcode.val(data[1]);
                        }
                    }
                });

                request.fail(function (jqXHR, textStatus, errorThrown) {
                    // console.log(jqXHR);
                    // window.alert(textStatus);
                });

            })
            .on('change', function (event) {
                const project_type = this.selectedOptions[0].value;
                const fields = ['detection_plan', 'sex', 'age'];
                fields.forEach(name => {
                    const label = document.querySelector(`label[for="${form_pre.substring(1)}${name}"`);
                    const input = document.querySelector(`${form_pre}${name}`);
                    const span = label.querySelector('span.required');
                    const no_value = document.querySelector('#form-single-sample-add-widgets-detection_plan-novalue');
                    if (project_type === "IM01C") {
                        if (!span) {
                            const sp = document.createElement("span");
                            sp.setAttribute('class', 'required horizontal');
                            label.appendChild(sp);
                        }
                        if (!input.hasAttribute('required')) {
                            input.setAttribute('required', 'true');
                        }
                        no_value.value = '';
                    } else {
                        if (span) {
                            label.removeChild(span);
                        }
                        if (input.hasAttribute('required')) {
                            input.removeAttribute('required');
                        }
                        no_value.value = '--NOVALUE--';
                    }
                });
            });

        // get data
        $(form_pre + "barcode")
            .on('keypress', function (event) {
                if (event.keyCode !== 13) {
                    return;
                }
                // event.stopPropagation();
                event.preventDefault();
                // console.log(this, event);
                //console.info(event.target, event.currentTarget, event.delegateTarget, event.relatedTarget);
                const barcode = this.value.trim();

                const portal_url = $('body').attr('data-portal-url');
                const draft_url = portal_url + '/draft';
                let url = draft_url + "/@search?sort_on=created&sort_order=descending&sort_limit=1";
                url += "&fullobjects=1&portal_type=News%20Item";
                url += "&Subject=NIPT";
                url += "&Title=" + barcode;
                const request = $.ajax({
                    url: url,
                    method: "GET",
                    headers: {
                        "Accept": "application/json",
                        // "Content-Type": "application/json",
                        // "Authorization": "Basic YWRtaW46c2VjcmV0",
                    },
                    // contentType: "application/json",
                    // mimeType: "application/json",
                    // dataType: "json",
                    // data: {id : menuId},
                });

                request.done(function (data, textStatus, jqXHR) {
                    // console.log(jqXHR);
                    if (data["items_total"] === 0) {
                        window.alert("Barcode not found");
                        return
                    }

                    const text = data["items"][0]["text"]["data"];
                    const element_data = JSON.parse(text);
                    element_data.forEach(function (item) {
                        let $item = $(form_pre + item['name']);
                        if ($item.length) {
                            const tagName = $item.prop('tagName');
                            if (["INPUT", "SELECT"].includes(tagName)) {
                                $item[0].value = item['value'];
                            }
                        }

                        $item = $('#formfield-form-single-sample-add-widgets-' + item['name']);
                        if ($item.length) {
                            const tagName = $item.prop('tagName');
                            if (tagName === 'DIV') {
                                set_widget_date(form_pre + item['name'], item['value']);
                                set_widget_date(form_pre + 'received_time', new Date());
                            }
                        }
                    });

                });

                request.fail(function (jqXHR, textStatus, errorThrown) {
                    // console.log(jqXHR);
                    window.alert(textStatus);
                });

            });

        // set receiver
        $single.on('submit', function (event) {
            const receiver_name = "received_operator";
            const $receiver_field = $(form_pre + receiver_name);
            if ($receiver_field) {
                const receiver_new = $receiver_field.val();
                const receiver_old = localStorage.getItem(receiver_name);
                if (receiver_new !== receiver_old) {
                    localStorage.setItem(receiver_name, receiver_new);
                }
            }
        });

        // get receiver
        $(window).on('load', function (event) {
            // portalMessage error
            if($single.prev().length >0){
                return
            }
            $(form_pre + "barcode").focus();

            const receiver_name = "received_operator";
            const $receiver_field = $(form_pre + receiver_name);
            if ($receiver_field) {
                if (localStorage.getItem(receiver_name)) {
                    $receiver_field.val(localStorage.getItem(receiver_name));
                }
            }
        })

    }

    function set_widget_date(selector, value) {
        const date = new Date(value);
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        const hour = date.getHours();
        const minute = date.getMinutes();
        const obj = {'year': year, 'month': month, 'day': day, 'hour': hour, 'minute': minute};
        for (const name in obj) {
            $(selector + '-' + name)
                .val(obj[name]).triggerHandler('change');
        }
    }

});


$(function () {
    "use strict";
    /**
     * ControlPanel
     * SMS help
     */

    const $sms_widget = $('#form-widgets-sms_message');
    if ($sms_widget.length) {
        $sms_widget
            .prevAll('label')
            .children('span.formHelp')
            .contents()
            .after(' <a id="message-help-info" href="@@gene-stringinterp-info">Help</a>');

        $('a#message-help-info').prepOverlay({
            subtype: 'ajax',
            cssclass: 'overlay-message-help',
            filter: '#content-core'
        });
    }

});


function select_group(dt_object) {
    "use strict";
    /**
     * Row selection by Group (double click indicator)
     */
    dt_object.on('draw.dt', function () {
      dt_object.rows(function (idx, data, node) {
        $(node).find('td:nth-child(2)').on('dblclick', {gid: data.DT_RowData['gid']}, function (event) {
          dt_object.rows(function (idx, data, node) {
            return (data.DT_RowData['gid'] === event.data.gid) && true || false;
          }).select();
          dt_object.rows(function (idx, data, node) {
            return (data.DT_RowData['gid'] !== event.data.gid) && true || false;
          }).deselect();
        });
      });
    });
}


function language_options() {
    return  {
        "sProcessing": "处理中...",
        "sLengthMenu": "每页_MENU_项",
        "sZeroRecords": "没有匹配结果",
        "sInfo": " 第_START_至_END_项，共_TOTAL_项",
        "sInfoEmpty": "第0 至0项，共0项",
        "sInfoFiltered": "(由_MAX_项结果过滤)",
        "sInfoPostFix": "",
        "sSearch": "搜索:",
        "sUrl": "",
        "sEmptyTable": "表中数据为空",
        "sLoadingRecords": "载入中...",
        "sInfoThousands": ",",
        "oPaginate": {
            "sFirst": "首页",
            "sPrevious": "上页",
            "sNext": "下页",
            "sLast": "末页"
        },
        "oAria": {
            "sSortAscending": ": 以升序排列此列",
            "sSortDescending": ": 以降序排列此列"
        },
        select: {
            rows: "选中%d项"
        }
    }
}


let init_bootstrap = true;
function restore_state(e, settings, data) {
    // data.sessionId = "$('#sessionId').val()";
    if (init_bootstrap) {
        const api = new $.fn.dataTable.Api(settings);
        const state = api.state.loaded();
        // ... use `state` to restore information
        if (state) {
            const page = parseInt(state.start / state.length);
            api.page(page);
            if (state.date) {
                data.date_field = state.date.field;
                data.date_from = state.date.start;
                data.date_to = state.date.end;
            }
            if (state.select) {
                data.steps = state.select.steps;
                data.review_state = state.select.review_state;
                data.project_type = state.select.project_type;
                data.sample_type = state.select.sample_type;
                data.gid = state.select.gid;
            }
        }
        init_bootstrap = false;
    }
}


/**
 * submitForm
 * To keep URLs intact with link buttons, use the 'form action' instead of 'a href=""'.
 * @param action
 * @param params
 */
function submitForm(action, params) {
    $('#_submitForm').remove();
    const form = $('<form enctype="multipart/form-data" style="display: none;"></form>');
    form.prop('id', '_submitForm');
    form.prop('action', action);
    form.prop('method', 'post');
    form.prop('target', '_self');
    //for (let i = 0; i < params.length; i++) {
    //    const input1 = $('<input type="hidden" name="' + params[i].name + '" />');
    //    input1.prop('value', params[i].val);
    //    form.append(input1);
    //}
    $.each(params, function (key, value) {
        const input1 = $('<input type="hidden" name="' + key + '" />');
        input1.prop('value', value);
        form.append(input1);
    });
    form.appendTo('body');
    form.css('display', 'none');
    form.submit();
}


// Import Excel
// ============
/*    $("#form-ImportHelp")
        .popover({
            html: true,
            //title: 'Advanced search instructions'.anchor(),
            content: $('#popover-ImportHelp').html(),
            template: '<div class="popover" role="tooltip" style="max-width: inherit; ">' +
            '<div class="arrow"></div>' +
            '<h3 class="popover-title"></h3>' +
            '<div class="popover-content"></div></div>',
            placement: 'bottom'
            //viewport: '#form-SearchableText'
        })
        .click(function (event) {
            event.preventDefault();
        });*/


// Datagridfield
// =============
//const $batch_list = $('#form-widgets-batch_list');
///**
// * Datagridfield
// * Change select Missing: value to first option
// */
//    //$('#form-widgets-batch_list select option:selected').text()
//    //$(this).get(0).selectedIndex=1
//$batch_list.find('select option:selected').each(function (/*index, element*/) {
//    // element == this
//    //console.log(index, element);
//    const text = $(this).text();
//    if (text.search("Missing:") == 0) {
//        $(this).parent().get(0).selectedIndex = 0;
//    }
//});
