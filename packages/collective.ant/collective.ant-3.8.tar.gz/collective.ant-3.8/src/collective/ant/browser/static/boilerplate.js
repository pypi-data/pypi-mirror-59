/**
 * Filename: genebpo.js
 * Version: 5.0
 * Date: 2019-03-01
 */

$(function () {
    "use strict";

    // data table
    // ==========
    /**
     * Datagridfield
     */
    // $.fn.dataTable.ext.errMode = 'throw';
    const $datable_object = $('div.project-genebpo #ant_datatable');

    if ($datable_object.length) {

        const $formSearchableText = $('#form-SearchableText');
        const $formSearchButton = $('#form-SearchButton');
        const $formSearchSelect = $('#form-SearchSelect');
        const $formSteps = $formSearchSelect.find('select[name="steps"]');
        const $formReviewState = $formSearchSelect.find('select[name="review_state"]');
        const $formProjectType = $formSearchSelect.find('select[name="project_type"]');
        const $formSampleType = $formSearchSelect.find('select[name="sample_type"]');
        const $formGroup = $formSearchSelect.find('select[name="gid"]');
        const $formDateField = $('#form-date-field');
        const $formDateFrom = $('#form-date-from');
        const $formDateTo = $('#form-date-to');
        const $selectDropdown = $('#selectDropdown');
        const $form_searchbox = $('#form-searchbox');
        const table_height = $(window).innerHeight() -
            $datable_object.find('thead').height() -
            $datable_object.find('tfoot').height() -
            $form_searchbox.closest('div.row').height() -
            $selectDropdown.closest('div.row').height() -
            100 /* id=data_table_paginate - */
            /* 25 id=data_table_length - */
            /* 21.row margin & padding */;
        const root_url = $('link[rel="home"]').prop('href') || window.navigation_root_url || window.portal_url;
        const _authenticator = $form_searchbox.find('input[name="_authenticator"]').val();
        // const columns_visible = $("body.userrole-manager, body.userrole-reviewer").length;
        const screen_width = window.screen.width;
        // let leftColumns = 9;
        // if ( screen_width < 768 ) {
        //     leftColumns = 0;
        // }

        const $datatablepattern = $datable_object.data('datatablepattern');
        const order = $datatablepattern['columnsLength'] + 4;
        const columns_option = $datatablepattern['columns_option'];
        const view_name = $datatablepattern['view_name'];
        const data_url = $datatablepattern['search_data_url'];
        const fixed_columns = $datatablepattern['fixed_columns'];

        const columns_left = [
            // fieldsets 0 Prefix
            {
                data: "url",
                className: 'select-checkbox',
                render: function (data, type, full, meta) {
                    if (data) {
                        return '*';
                    }
                    //return '<input type="checkbox" name="paths:list" value = "' + data + '"/>';
                    return '';
                }
            },
            {
                data: 'gid', defaultContent: '',
                render: function (data, type, full, meta) {
                    const gid = full['DT_RowData']['gid'];
                    const indicator = [];
                    // length=32; Math.floor(32 / 6)=5
                    for (let i = 0; i < 2; i++) {
                        gid.slice(i * 6, (i + 1) * 6);
                        indicator.push('<div class="gid_box" style="background-color: #'
                            + gid.slice(i * 6, (i + 1) * 6) + '"></div>');
                    }
                    return indicator.join('');
                }
            },
            {data: "steps", orderable: true, searchable: true},
            {
                data: "review_state", orderable: true, searchable: true,
                "createdCell": function (td, cellData, rowData, row, col) {
                    if (cellData !== 1) {
                        $(td).css('color', 'red');
                    }
                }
            }];
            const columns_middle = eval(decodeURIComponent(columns_option));
            const columns_right = [
            // fieldsets 0 Suffix
            {data: "created", orderable: true, searchable: true},
            {data: "modified", orderable: true, searchable: true},
            // actions
            {
                // action fieldsets
                data: null, defaultContent: '',
                "render": function (data, type, full, meta) {
                    const uuid = full['DT_RowData']['uuid'];
                    const steps = full['DT_RowData']['steps'];
                    const sample_id = data['sample_id'];
                    const action = [];
                    // if (full['DT_RowData']['review_state'] === 'success') {
                    //     action.push('<a class="_DigitalSignature" href="' +
                    //         data['url'] + '/@@generate-report">报告</a>');
                    // }
                    // if (full['DT_RowData']['review_state'] === 'success') {
                    //     action.push('<a class="_DigitalSignature" href="' +
                    //         data['url'] + '/@@generate-signature">签名</a>');
                    // }
                    // if ($('body').hasClass('template-genebpo-sample-view') &&
                    //     ($('body').hasClass('userrole-manager') ||
                    //         $('body').hasClass('userrole-sample'))) {
                    //     if (steps === 'sample') {
                    //         action.push('<a class="_ResultAction" href="" ' +
                    //             'data-uuid="' + uuid + '" ' +
                    //             'data-sample_id="' + sample_id + '" ' +
                    //             'title="上传照片">' + '上传' + '</a>');
                    //     }
                    //     // todo: fix me.
                    //     if ("data['photo'][0]") {
                    //         action.push('<a class="_Result" href="./genebpo-sample-photo-download?uuid=' +
                    //             uuid + '" title="下载照片" target="_blank">下载</a>');
                    //     }
                    // }
                    if (data['can_changenote']) {
                        action.push('<a class="_ChangeNote" href="' +
                            data['url'] + '/@@lis-changenote">' + '备注' + '</a>');
                    }
                    if (data['can_versions']) {
                        action.push('<a class="_ContentHistory" href="' +
                            data['url'] + '/@@historyview">' + '历史' + '</a>');
                    }
                    return action.join(' ');
                }
            }];
        const columns_configuration = columns_left.concat(columns_middle, columns_right);

        // Initialisation
        let init_bootstrap = true;
        const $data_table = $datable_object
            .on('preXhr.dt', restore_state)
            .DataTable({
                scrollY: table_height,
                scrollX: true,
                scrollCollapse: true,
                autoWidth: true,
                searching: true,
                ordering: true,
                order: [order, "desc"],
                info: true,
                // oLanguage: {"sUrl": "@@collective.js.datatables.translation"},
                // deferRender: [ 20, 1000 ],
                language: language_options(),
                paging: true,
                lengthMenu: [10, 20, 50, 100, 200],
                pageLength: 20,
                processing: true,
                serverSide: true,
                stateSave: true,
                stateDuration: -1,
                // rowId: 'DT_RowId',
                fixedColumns: {
                    leftColumns: fixed_columns,
                    rightColumns: 0
                },
                select: {
                    style: 'os',
                    selector: 'td:first-child'
                },
                columnDefs: [
                    {
                        orderable: false,
                        searchable: false,
                        targets: '_all'
                    }/*,
                    {
                        visible: columns_visible,
                        targets: [ 8 ]
                    }*/
                ],
                columns: columns_configuration, /*[{},{}]*/
                ajax: {
                    url: data_url,
                    type: "POST",
                    data: function (dict) {
                        dict.steps = $formSteps.val();
                        dict.review_state = $formReviewState.val();
                        dict.project_type = $formProjectType.val();
                        dict.sample_type = $formSampleType.val();
                        dict.gid = $formGroup.val();

                        dict.date_field = $formDateField.val();
                        dict.date_from = $formDateFrom.val();
                        dict.date_to = $formDateTo.val();
                        dict.view_name = view_name;
                        dict._authenticator = _authenticator;
                        //console.info(dict)
                        //dict.myKey = "myValue";
                        // etc
                    }
                },
                initComplete: function (settings, json) {
                },
                rowCallback: function (row, data, index) {
                },
                drawCallback: function (settings) {
                    // Row grouping
                    const api = this.api();
                    const rows = api.rows({page: 'current'}).nodes();
                    let last = null;

                    // second draw
                    /*if ($(rows).eq( 0 ).prev().length) {
                        return false;
                    }
                    api.column(1, {page:'current'} ).data().each( function ( row, i ) {
                        const group = row['DT_RowData']['gid'];
                        const row_td = new Array(64).join("<td></td>");
                        if ( last !== group ) {

                            $(rows).eq( i ).before(
                                // '<tr class="group"><td colspan="63">'+ ++i +'</td></tr>'
                                '<tr class="group">' + row_td + '</tr>'
                            );
                            last = group;
                        }
                    });*/

                    // window scroll Top to #form-searchbox
                    /*window.setTimeout(function () {
                        // Delay n millisecond waiting for draw finish.
                        $(window).scrollTop($form_searchbox.offset()['top'] - 2)
                    }, 50)*/
                }
                /*stateSaveCallback: function(settings,data) {
                    localStorage.setItem( 'DataTables_' + settings.sInstance, JSON.stringify(data) )
                  },
                stateLoadCallback: function(settings) {
                    return JSON.parse( localStorage.getItem( 'DataTables_' + settings.sInstance ) )
                  },*/

            });
            // End init


        /**
         *  Index column
         *  Be aware that using deferRender.DT will cause some nodes not be immediately available
         *  Init second draw
         */
        $data_table.on(/*'order.dt search.dt'*/ 'draw.dt', function () {
            const info = $data_table.page.info();
            $data_table.column(1, {search: 'applied', order: 'applied'}).nodes().each(function (cell, i) {
                //cell.innerHTML = info.start + i + 1;
                const line_number = info.start + i + 1;
                const cell_content = cell.innerHTML;
                // Trigger two times
                if (!cell_content.endsWith(line_number)) {
                    cell.innerHTML = cell_content + (info.start + i + 1);
                }
            });
        });


        /**
         * Set the visibility of the selected columns.
         * Hide multiple columns using redrawCalculations to improve performance:
         */
        // const columns_visible = $("body.userrole-manager, body.userrole-reviewer").length;
        // $data_table.columns( [ 3 ] ).visible( false, false );
        // $data_table.columns.adjust().draw( false ); // adjust column sizing and redraw


        /**
         * Fixed Columns
         * Responsive tables
         * Scroll horizontally on small devices (under 768px).
         */
        /*$(window).on( 'resize load',function( event ){
            // table-responsive
            const screen_width = window.screen.width;
            const leftColumns = 11;

            if ( screen_width < 768 ) {
                leftColumns = 0;
            }
            const fc_object = new $.fn.dataTable.FixedColumns( $data_table, {
                leftColumns: leftColumns,
                rightColumns: 1
            });
        });*/


        /**
         * ColReorder
         * click and drag any table header cell
         */
        // new $.fn.dataTable.ColReorder($data_table, {realtime: true});


        // Select by the grouping
        // $datable_object.find('tbody').on( 'click', 'tr.group', function () {
        //     console.log('click group title');
        // } );


        // State save event - fired when saving table state information.
        $datable_object.on('stateSaveParams.dt', function (e, settings, data) {
            data.date = {};
            data.date.field = $formDateField.val();
            data.date.start = $formDateFrom.val();
            data.date.end = $formDateTo.val();

            data.select = {};
            data.select.steps = $formSteps.val();
            data.select.review_state = $formReviewState.val();
            data.select.project_type = $formProjectType.val();
            data.select.sample_type = $formSampleType.val();
            data.select.gid = $formGroup.val();

            // data.search_field = {};
            // data.search_date = {};
        });

        // Page change event - fired when the table's paging is updated.
        $datable_object.on('page.dt', function (e, settings) {
            const api = new $.fn.dataTable.Api(settings);
            api.state.save();
        });

        // Get the table state that was loaded during initialisation.
        $datable_object
            .on('init.dt', function (e, settings) {
                const api = new $.fn.dataTable.Api(settings);
                const state = api.state.loaded();
                // ... use `state` to restore information
                if (state) {
                    $formSearchableText.val(state.search.search);
                    const page = parseInt(state.start / state.length);
                    $data_table.page(page);
                    if (state.date) {
                        $formDateField.val(state.date.field);
                        $formDateFrom.val(state.date.start);
                        $formDateTo.val(state.date.end);
                    }
                    if (state.select) {
                        $formSteps.val(state.select.steps);
                        $formReviewState.val(state.select.review_state);
                        $formProjectType.val(state.select.project_type);
                        $formSampleType.val(state.select.sample_type);
                        $formGroup.val(state.select.gid);
                    }
                }
            });


        select_group($data_table);


        /**
         *  Buttons & Actions Enable | Disable toggle
         */
        $data_table.on('select.dt deselect.dt', function (e, dt, type, indexes) {
            const current_len = $data_table.page.info().end - $data_table.page.info().start;
            const selected_count = $data_table.rows({selected: true}).count();
            const $indicator = $selectDropdown.find(' span[data-target="indicator"]');

            if (current_len === selected_count && current_len > 0) {
                $indicator.prop('class', 'glyphicon glyphicon-check');
            } else if (current_len > selected_count && selected_count === 0) {
                $indicator.prop('class', 'glyphicon glyphicon-unchecked');
            } else if (current_len > selected_count) {
                $indicator.prop('class', 'glyphicon glyphicon-modal-window');
            }

            // Action button Enable / Disable
            const $toggle_button = $(
                '#dataBtnGroup a[data-target="sample-edit"],' +
                '#dataBtnGroup a[data-target="separation-edit"],' +
                '#dataBtnGroup a[data-target="extraction-edit"],' +
                '#dataBtnGroup a[data-target="qc-edit"],' +
                '#dataBtnGroup a[data-target="qc-edit"],' +
                '#dataBtnGroup a[data-target="detection-add"],' +
                '#dataBtnGroup a[data-target="result-add"],' +
                '#dataBtnGroup a[data-target="result-edit"],' +
                '#manageBtnGroup a[data-target="change-steps"], ' +
                '#manageBtnGroup a[data-target="state-transition"], ' +
                '#manageBtnGroup a[data-target="failed-redo"], ' +
                '#manageBtnGroup a[data-target="report"], ' +
                '#manageBtnGroup a[data-target="delete"], ' +
                '#moreBtnGroup a[data-target="export-item"], ' +
                '#moreBtnGroup a[data-target="export-dilution"]'
            );
            if (selected_count) {
                //$toggle_button.show();
                $toggle_button.parent().removeClass('disabled');
                //$toggle_button.css('pointer-events', 'auto');
            } else {
                //$toggle_button.hide()
                $toggle_button.parent().addClass('disabled');
                //$toggle_button.css('pointer-events', 'none');
            }
        });


        /**
         * Row selection by Buttons
         */
        $selectDropdown.on('click', '*[data-target]', function (event) {
            //event.stopPropagation();
            event.preventDefault();
            //console.log($(this).data('target'), $(event), event.target, event.relatedTarget)
            const target_data = $(this).data('target');
            const target_list = [
                'sample', 'result',
                'private', 'pending', 'success', 'failed', 'abort'];

            if (target_data === 'indicator') {
                const css_class = $(this).prop('class');

                if (css_class === 'glyphicon glyphicon-unchecked') {
                    $data_table.rows().select();
                } else if (css_class === 'glyphicon glyphicon-check' ||
                    css_class === 'glyphicon glyphicon-modal-window') {
                    $data_table.rows().deselect();
                }
            } else if (target_data === 'all') {
                $data_table.rows().select();
            } else if (target_data === 'none') {
                $data_table.rows().deselect();
            } else if ($.inArray(target_data, target_list) > -1) {
                $data_table.rows().deselect();
                $data_table.rows('.' + target_data).select();
            }
        });


        /**
         * Row selection by Group (double click indicator)
         * todo:
         */
        $datable_object.on('draw.dt', function () {
            $datable_object.find('>tbody>tr>td>div.gid_box')
                .on('dblclick', null, function (event) {
                    // !!! Columns has cloned, so change evnent coming from
                    // Fixed Columns Or Data Datable !!!
                    // event.stopPropagation();

                    //const gid = $(this).closest('tr').data('gid');
                    //console.info( $(this).closest('tr').data('steps') );
                    // Select Row
                    /*if ($(this).prop("checked")) {
                     $(this).closest('tr').find('>td>input[type="checkbox"]:first-of-type');
                     }*/

                });
        });


        /**
         * Buttons action
         */
        $('#dataBtnGroup a[data-target],' +
            '#manageBtnGroup a[data-target],' +
            '#moreBtnGroup a[data-target]')
            .on('click confirm.toolbar', null, function (event) {
                //event.stopPropagation();
                event.preventDefault();
                //console.log($(this).data('target'), $(event), event.target);
                const target_data = $(this).data('target');
                const target_list = [
                    'sample-view', 'sample-import', 'sample-single-add', 'sample-add', 'sample-edit',
                    'extraction-view', 'extraction-import', 'extraction-add', 'extraction-edit',
                    'result-view', 'result-import', 'result-add', 'result-edit',
                    'pcr-view', 'pcr-import', 'pcr-add', 'pcr-edit',
                    'qc-view', 'qc-import', 'qc-add', 'qc-edit',
                    'detection-view', 'detection-import', 'detection-add', 'detection-edit',
                    'change-steps', 'state-transition', 'failed-redo', /*'report',*/
                    'delete', 'export-item', 'export-dilution', 'backup', 'recovery'
                ];
                //const target_list_all = [/*'import',*/, 'export-all'];
                if ($.inArray(target_data, target_list) === -1) {
                    return 0;
                }

                const $selected_row = $data_table.rows({selected: true}).data();
                // const $selected_row = $data_table.rows( { selected: true } ).nodes();
                const uuid_list = [];
                $selected_row.each(function (element, index) {
                    uuid_list.push(element['DT_RowData']['uuid']);
                    // uuid_list.push($(element).data('uuid'));
                });
                const uuid_length = uuid_list.length;

                let view = '.';
                const extraParameters = {};

                switch (target_data) {
                    // sample
                    case 'sample-view':
                        view = 'genebpo-sample-view';
                        break;
                    case 'sample-import':
                        view = 'genebpo-sample-import';
                        break;
                    case 'sample-single-add':
                        view = 'genebpo-single-sample-addform';
                        break;
                    case 'sample-add':
                        view = 'genebpo-sample-addform';
                        break;
                    case 'sample-edit':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'genebpo-sample-editform';
                        break;

                    // extraction
                    case 'extraction-view':
                        view = 'genebpo-extraction-view';
                        break;
                    case 'extraction-import':
                        view = 'genebpo-extraction-import';
                        break;
                    case 'extraction-add':
                        view = 'genebpo-extraction-addform';
                        break;
                    case 'extraction-edit':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'genebpo-extraction-editform';
                        break;

                    // pcr
                    case 'pcr-view':
                        view = 'genebpo-pcr-view';
                        break;
                    case 'pcr-import':
                        view = 'genebpo-pcr-import';
                        break;
                    case 'pcr-add':
                        view = 'genebpo-pcr-addform';
                        break;
                    case 'pcr-edit':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'genebpo-pcr-editform';
                        break;

                    // qc
                    case 'qc-view':
                        view = 'genebpo-qc-view';
                        break;
                    case 'qc-import':
                        view = 'genebpo-qc-import';
                        break;
                    case 'qc-add':
                        view = 'genebpo-qc-addform';
                        break;
                    case 'qc-edit':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'genebpo-qc-editform';
                        break;

                    // detection
                    case 'detection-view':
                        view = 'genebpo-detection-view';
                        break;
                    case 'detection-import':
                        view = 'genebpo-detection-import';
                        break;
                    case 'detection-add':
                        view = 'genebpo-detection-addform';
                        break;
                    case 'detection-edit':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'genebpo-detection-editform';
                        break;

                    // result
                    case 'result-view':
                        view = 'genebpo-result-view';
                        break;
                    case 'result-import':
                        view = 'genebpo-result-import';
                        break;
                    case 'result-add':
                        view = 'genebpo-result-addform';
                        break;
                    case 'result-edit':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'genebpo-result-editform';
                        break;

                    // Change Steps
                    case 'change-steps':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'genebpo-change-steps-form';
                        break;
                    case 'state-transition':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'genebpo-state-transition-form';
                        break;
                    // Mark failed redo
                    case 'failed-redo':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'genebpo-failed-redo-form';
                        break;
                    // More
                    case 'delete':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        // dismiss default click, waiting dialog confirm click.toolbar event.
                        if (event.type === 'click') {
                            const modal = $('#delete_modal_dialog').modal();
                            modal.find('.modal-body strong').text(uuid_length);
                            return 2;
                        }
                        view = '.';
                        break;
                    //Export
                    case 'export-item':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'genebpo-export-items';
                        break;
                    case 'export-dilution':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        // const $btn_confirm = $('#dilution_modal_dialog')
                        //   .find('.modal-footer button[data-target="export-dilution"]');
                        // dismiss default click, waiting dialog confirm click.toolbar event.
                        if (event.type === 'click') {
                            // $btn_confirm.addClass('disabled').prop('disabled', true);

                            const bar_list = [];
                            $selected_row.each(function (element, index) {
                                bar_list.push(element['qc_barcode']);
                                // bar_list.push($(element).data('qc_barcode'));
                            });

                            const key_list = [];
                            const value_list = [];
                            const dict_list = [];

                            for (let i = 0,  j = 1; i < bar_list.length; i++, j++) {
                                const value = bar_list[i];
                                // if (bar_list.indexOf(value, j) > -1 && key_list.indexOf(value) === -1)
                                // {
                                //     key_list.push(value);
                                // }
                                if (bar_list.indexOf(value, j) > -1) {
                                    const name_index = key_list.indexOf(value);
                                    if (name_index === -1) {
                                        key_list.push(value);
                                        value_list[value_list.length] = 2;
                                    } else {
                                        value_list[name_index] += 1;
                                    }
                                }
                            }

                            for (let i = 0; i < key_list.length; i++) {
                                dict_list.push("'" + key_list[i] + "'" + ':' + value_list[i]);
                            }
                            const modal = $('#dilution_modal_dialog').modal();
                            modal.find('.modal-body strong._total').text(uuid_length);
                            modal.find('.modal-body strong._same').text(key_list.length);
                            modal.find('.modal-body span._bar').text(dict_list.join(', '));
                            // modal.find('.modal-body span._bar').text(key_list.sort().toString());
                            // $btn_confirm.removeClass('disabled').prop('disabled', false);

                            return 'Request confirmation';
                        }
                        view = 'genebpo-export-dilution';
                        break;
                    case 'backup':
                        view = 'genebpo-backup-view';
                        break;
                    case 'recovery':
                        view = 'genebpo-recovery-view';
                        break;
                    default:
                        view = '.';
                        break;
                }

                // !!!! ajax_load make form No Style !!!!
                const data = {
                    uuids: uuid_list,
                    bulk_action: target_data,
                    _authenticator: _authenticator /*, ajax_load: false*/
                };
                $.extend(data, extraParameters);
                submitForm(view, data);

                /*$.post(".", data, dataType = "html")
                 .done(function (data) {
                 console.log(data);
                 });*/
                //const href = window.location.pathname + '/' + view +'?' + $.param(data);
                //window.location.href = href;
            });


        /**
         * Delete confirm mode dialog
         */
        const $delete_dialog = $('#delete_modal_dialog');
        $delete_dialog.find('.modal-footer button[data-target="delete"]')
            .on('click', function () {
                const target = $(this).data('target');
                $('#manageBtnGroup').find('a[data-target="' + target + '"]').triggerHandler('confirm.toolbar');
                $delete_dialog.modal('hide');
            });


        /**
         * Upload result mode dialog
         */
            // $("form#data").submit(function(){
            //
            //     const formData = new FormData(this);
            //     console.log(formData);
            //     debugger;
            //     $.ajax({
            //         url: window.location.pathname,
            //         type: 'POST',
            //         data: formData,
            //         async: false,
            //         success: function (data) {
            //             alert(data)
            //         },
            //         cache: false,
            //         contentType: false,
            //         processData: false
            //     });
            //
            //     return false;
            // });
        const $upload_dialog = $('#upload_modal_dialog');
        if ($upload_dialog.length) {
            const $button_start = $upload_dialog.find('.modal-footer button._start');
            const $button_cancel = $upload_dialog.find('.modal-footer button._cancel');
            const $button_reload = $upload_dialog.find('.modal-footer button._reload');
            const $success_msg = $upload_dialog.find('.modal-body div.alert-success');
            const $failed_msg = $upload_dialog.find('.modal-body div.alert-danger');

            $button_start
                .on('click', function () {
                    const view = './genebpo-sample-photo-upload';
                    const formData = new FormData($upload_dialog.find('form'));
                    const uuid = $upload_dialog.find('input[name="form.widgets.uuid"]').val();
                    const sample_id = $upload_dialog.find('input[name="form.widgets.sample_id"]').val();
                    const force = $upload_dialog.find('input[name="form.widgets.force"]').prop('checked');
                    let fileObj = $upload_dialog.find('input[name="form.widgets.result"]')[0].files;
                    if (fileObj.length === 0) {
                        return;
                    }
                    fileObj = fileObj[0];
                    formData.append('form.widgets.result', fileObj);
                    formData.append('form.widgets.sample_id', sample_id);
                    formData.append('form.widgets.uuid', uuid);
                    formData.append('form.widgets.force', force);
                    formData.append('_authenticator', _authenticator);

                    // const xhr = new XMLHttpRequest();
                    // xhr.open('post', view, true);
                    // xhr.onload = function (data) {
                    //     console.log(data);
                    //     console.log("上传完成!");
                    // };
                    // xhr.upload.addEventListener('progress', progressFunction, false);
                    // xhr.send(formData);
                    //
                    // function progressFunction(evt) {
                    //     const progressBar = document.getElementById("progressBarResult");
                    //     // const percentageDiv = document.getElementById("percentage");
                    //     if (evt.lengthComputable) {
                    //       progressBar.max = evt.total;
                    //       progressBar.value = evt.loaded;
                    //       // percentageDiv.innerHTML = Math.round(evt.loaded / evt.total * 100) + "%";
                    //     }
                    // }

                    // const param = {
                    //     // uuids: uuid_list.join(),
                    //     _authenticator: _authenticator
                    //     /*bulk_action: target_data,*/ /*for delete*/
                    //     /*, ajax_load: false*/
                    // };
                    // const jqxhr = $.post(view, formData, function( data ) {
                    //     // console.info(data);
                    // });
                    const jqxhr = $.ajax({
                        type: "POST",
                        url: view,
                        data: formData,
                        processData: false,
                        contentType: false
                        // success: success,
                        // dataType: dataType
                    });
                    jqxhr.done(function (data, textStatus, jqXHR) {
                        data = JSON.parse(data);
                        if (data) {
                            const _back_success = data['_back_success'];
                            const _back_message = data['_back_message'];
                            if (_back_success) {
                                $success_msg.text(_back_message);
                                $button_reload.show();
                            } else {
                                $failed_msg.text(_back_message);
                            }
                        }
                    });
                    jqxhr.fail(function (data, textStatus, errorThrown) {
                        $upload_dialog.find('.modal-body div.alert-danger').text(errorThrown);
                    });
                    jqxhr.always(function (data, textStatus, jqXHR) {
                        // $upload_dialog.find('.modal-body div._result_info').show();
                    });

                    // $upload_dialog.modal('hide');
                    $success_msg.text('');
                    $failed_msg.text('');
                });
            $upload_dialog.find('.modal-footer button._reload')
                .on("click", function () {
                    location.reload();
                });
            $upload_dialog.find('.modal-footer button._failed')
                .on("click", function () {
                    $formSearchableText.val(window.sessionStorage.getItem('fetch.failed.sample'));
                    const event = jQuery.Event("keypress", {keyCode: 13});
                    $formSearchableText.triggerHandler(event);
                });

            $upload_dialog
                .on('shown.bs.modal', function (e) {
                    $success_msg.text('');
                    $failed_msg.text('');
                    $button_reload.hide();
                })
                .on('hidden.bs.modal', function (e) {
                    $success_msg.text('');
                    $failed_msg.text('');
                    $button_reload.hide();
                });
        }


        /**
         * Export dilution confirm mode dialog
         */
        const $dilution_dialog = $('#dilution_modal_dialog');
        $dilution_dialog.find('.modal-footer button[data-target="export-dilution"]')
            .on('click', function () {
                const target = $(this).data('target');
                $('#moreBtnGroup').find('a[data-target="' + target + '"]').triggerHandler('confirm.toolbar');
                $dilution_dialog.modal('hide');
            });


        /**
         * SearchableText
         */

        $formSearchableText
            .on('keypress', function (event) {
                if (event.keyCode === 13) {
                    $data_table.search(this.value).draw();
                }
            });

        $("#form-SearchableHelp")
            .popover({
                html: true,
                //title: 'Advanced search instructions'.anchor(),
                content: $('#tooltip-SearchableText').html(),
                template: '<div class="popover" role="tooltip" style="max-width: inherit; ">' +
                    '<div class="arrow"></div>' +
                    '<h3 class="popover-title"></h3>' +
                    '<div class="popover-content"></div></div>',
                placement: 'auto rigth'
                //viewport: '#form-SearchableText'
            });
        /*.on('shown.bs.popover', function () {
         $('#' + this.getAttribute('aria-describedby'))
         .insertAfter($(this)
         .parent().parent());
         });*/

        $("#form-SearchableClear, #form-date-from-clear, #form-date-to-clear")
            .on('click', function (event) {
                const target = $(this).data('for');
                const $target_input = $('#' + target);
                if ($target_input.val() === '') {
                    return
                }
                $target_input.val('');

                const clear_id = $(this).prop('id');

                if ((clear_id === 'form-date-from-clear' ||
                    clear_id === 'form-date-to-clear') && !$formDateField.val()) {
                    return
                }
                // Create a new jQuery.Event object with specified event properties.
                const key_event = jQuery.Event("keypress", {keyCode: 13});
                // trigger an artificial keydown event with keyCode 13
                $formSearchableText.triggerHandler(key_event);
            });

        $formSearchButton
            .on('click', function (event) {
                //event.stopPropagation();
                // event.preventDefault();
                // console.log(this, event);
                //console.info(event.target, event.currentTarget, event.delegateTarget, event.relatedTarget);
                const key_event = jQuery.Event('keypress', {keyCode: 13});
                $formSearchableText.triggerHandler(key_event);
            });

        $formSearchSelect.find('select')
            .on('change', function (event) {
                //event.stopPropagation();
                // event.preventDefault();
                // console.log(this, event);
                //console.info(event.target, event.currentTarget, event.delegateTarget, event.relatedTarget);
                const key_event = jQuery.Event('keypress', {keyCode: 13});
                $formSearchableText.triggerHandler(key_event);
            });

        $formDateField
            .on('change', function (event) {
                //event.stopPropagation();
                event.preventDefault();
                //console.log(this, event);
                //console.info(event.target, event.currentTarget, event.delegateTarget, event.relatedTarget);
                const field_val = $(this).val();

                if (field_val && !($formDateFrom.val() || $formDateTo.val())) {
                    return
                }
                else if (!field_val && ($formDateFrom.val() || $formDateTo.val())) {
                    $formDateFrom.val('');
                    $formDateTo.val('');
                }

                const key_event = jQuery.Event('keypress', {keyCode: 13});
                $formSearchableText.triggerHandler(key_event);
            });

        $formDateFrom.datepicker({
            dateFormat: "yy-mm-dd",
            defaultDate: "-1m",
            changeMonth: true,
            numberOfMonths: 2,
            showAnim: "slideDown",
            onSelect: function (selectedDate) {
                if ($formDateField.val()) {
                    const key_event = jQuery.Event('keypress', {keyCode: 13});
                    $formSearchableText.triggerHandler(key_event);
                }
            },
            onClose: function (selectedDate) {
                $formDateTo.datepicker("option", "minDate", selectedDate);
            }
        });

        $formDateTo.datepicker({
            dateFormat: "yy-mm-dd",
            defaultDate: "-1m",
            changeMonth: true,
            numberOfMonths: 2,
            showAnim: "slideDown",
            onSelect: function (selectedDate) {
                if ($formDateField.val()) {
                    const key_event = jQuery.Event('keypress', {keyCode: 13});
                    $formSearchableText.triggerHandler(key_event);
                }
            },
            gotoCurrent: true,
            onClose: function (selectedDate) {
                $formDateFrom.datepicker("option", "maxDate", selectedDate);
            }
        });


        /**
         * Change Note form
         */
        // $datable_object
        //     .on('draw.dt', function () {
        //         $('a._ChangeNote').prepOverlay({
        //             subtype: 'ajax',
        //             cssclass: 'overlay-changenote',
        //             width:'30%',
        //             filter: 'h2, #content',
        //             formselector: 'form[id="ChangeNoteForm"]',
        //             noform: function(el) {return $.plonepopups.noformerrorshow(el, 'close');}
        //         });
        //     });
        //
        //
        // /**
        //  * Content history popup
        //  */
        // $datable_object
        //     .on('draw.dt', function () {
        //         $('a._ContentHistory').prepOverlay({
        //             subtype: 'ajax',
        //             cssclass: 'overlay-history',
        //             filter: 'h2, #content-history',
        //             urlmatch: '@@historyview',
        //             urlreplace: '@@contenthistorypopup'
        //         });
        //     });

        /**
         * Move paginate Content to top
         */
        $datable_object
            .on('init.dt', function () {
                $('#datatable_info')
                    .append($('#ant_datatable_length').css('display', 'inline'))
                    .append($('#ant_datatable_info').css('display', 'inline'));
                $('#datatable_paginate').append($('#ant_datatable_paginate'));
            });


        /**
         * Content result popup
         */
        $datable_object
            .on('click', 'a._ResultAction', function (event) {
                event.preventDefault();
                const modal = $('#upload_modal_dialog').modal();
                modal.find('#result_sample_id').text($(this).data()['sample_id']);
                modal.find('input[name="form.widgets.sample_id"]').val($(this).data()['sample_id']);
                modal.find('input[name="form.widgets.uuid"]').val($(this).data()['uuid']);
                // $('a._ResultAction').modal();
            });


        /**
         * Processing Indicator - fired when DataTables is processing data.
         */
        (function ($) {
            $datable_object
                .on('processing.dt', function (e, settings, processing) {
                    //  $('#processingIndicator').css( 'display', processing ? 'block' : 'none' );
                    if(processing){
                        $('#ProgressModal .progress-bar').addClass('add_slide_progress');
                        $('#ProgressModal').modal('show');
                    }
                    else{
                        $('#ProgressModal .progress-bar').removeClass('add_slide_progress');
                        $('#ProgressModal').modal('hide');
                    }
                });

        })(jQuery); // End Processing Indicator

    } // End Data Table

});
