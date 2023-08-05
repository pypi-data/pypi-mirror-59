/**
 * Filename: main.js
 * Version: 5.6
 * Date: 2019-03-01
 */

$(function () {
    "use strict";

    // data table
    // ==========
    /**
     * Data Table Render
     */
        // $.fn.dataTable.ext.errMode = 'throw';
    const $datable_object = $('#report_datatable');

    if ($datable_object.length) {

        const $formSearchableText = $('#form-SearchableText');
        const $formSearchButton = $('#form-SearchButton');
        const $formSearchSelect = $('#form-SearchSelect');
        const $formPortalType = $formSearchSelect.find('select[name="portal_type"]');
        const $formProjectType = $formSearchSelect.find('select[name="project_type"]');
        const $formReportState = $formSearchSelect.find('select[name="report_state"]');
        const $formDownloadCount = $formSearchSelect.find('select[name="download_count"]');
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
            35 /* id=data_table_paginate - */
            /* 25 id=data_table_length - */
            /* 21.row margin & padding */;
        // const root_url = $('link[rel="home"]').prop('href') || window.navigation_root_url || window.portal_url;
        // const root_url_len = root_url.split('/').length;
        // const columns_visible = $("body.userrole-manager, body.userrole-reviewer").length;
        // const screen_width = window.screen.width;
        // let leftColumns = 0;
        // if (screen_width < 768) {
        //         leftColumns = 0;
        // }
        const _authenticator = $form_searchbox.find('input[name="_authenticator"]').val();
        const $datatablepattern = $datable_object.data('datatablepattern');
        const order = $datatablepattern['columnsLength'] + 1;
        const columns_option = $datatablepattern['columns_option'];
        const data_url = $datatablepattern['search_data_url'];
        const fixed_columns = $datatablepattern['fixed_columns'];

        const columns_left = [
            // fieldsets 0 Prefix
            {
                data: "url",
                className: 'select-checkbox',
                render: function (data, type, full, meta) {
                    //return '<input type="checkbox" name="paths:list" value = "' + data + '"/>';
                    // return '<input type="checkbox"/>';
                    return '';
                }
            },
            {
                data: null, defaultContent: '',
                render: function (data, type, full, meta) {
                    const gid = full['DT_RowData']['gid'];
                    let indicator = [];
                    // length=32; Math.floor(32 / 6)=5
                    for (let i = 0; i < 2; i++) {
                        // gid.slice(i * 6, (i + 1) * 6);
                        indicator.push('<div class="gid_box" style="background-color: #'
                            + gid.slice(i * 6, (i + 1) * 6) + '"></div>');
                    }
                    return indicator.join('');
                }
            }
        ];
        const columns_middle = eval(decodeURIComponent(columns_option));
        const columns_right = [];
        const columns_configuration = columns_left.concat(columns_middle, columns_right);
        // Initialisation
        let init_bootstrap = true;
        const $data_table = $datable_object
            .on('preXhr.dt', function (e, settings, data) {
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
                            data.portal_type = state.select.portal_type;
                            data.project_type = state.select.project_type;
                            data.report_state = state.select.report_state;
                            data.download_count = state.select.download_count;
                        }
                    }
                    init_bootstrap = false;
                }
            })
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
            "language": {
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
            },
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
                selector: 'td:first-child',
                info: true
            },
            columnDefs: [
                {
                    orderable: false,
                    searchable: false,
                    targets: '_all'
                }/*,
                {
                    visible: columns_visible,
                    targets: [ 7, 8, 9, 10, 11, 12 ]
                }*/
            ],
            columns: columns_configuration, /*[{},{}]*/
            ajax: {
                url: data_url,
                type: "POST",
                data: function (dict) {
                    dict.portal_type = $formPortalType.val();
                    dict.project_type = $formProjectType.val();
                    dict.report_state = $formReportState.val();
                    dict.download_count = $formDownloadCount.val();

                    dict.date_field = $formDateField.val();
                    dict.date_from = $formDateFrom.val();
                    dict.date_to = $formDateTo.val();

                    dict._authenticator = _authenticator;
                    // console.info(dict)
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
         *    Index column
         *    Be aware that using deferRender.DT will cause some nodes not be immediately available
         *    Init second draw
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
         * Row selection by Group (double click indicator)
         */
        $data_table.on('draw.dt', function () {
            $data_table.rows(function (idx, data, node) {
                $(node).find('td:nth-child(2)').on('dblclick', {gid: data.DT_RowData['gid']}, function (event) {
                    // Repeat dblclick
                    // console.log(node.classList.contains('selected'));
                    $data_table.rows(function (idx, data, node) {
                        return (data.DT_RowData['gid'] === event.data.gid) && true || false;
                    }).select();
                    $data_table.rows(function (idx, data, node) {
                        return (data.DT_RowData['gid'] !== event.data.gid) && true || false;
                    }).deselect();
                });
            });
        });


        // State save event - fired when saving table state information.
        $datable_object.on('stateSaveParams.dt', function (e, settings, data) {
            data.date = {};
            data.date.field = $formDateField.val();
            data.date.start = $formDateFrom.val();
            data.date.end = $formDateTo.val();

            data.select = {};
            data.select.portal_type = $formPortalType.val();
            data.select.project_type = $formProjectType.val();
            data.select.report_state = $formReportState.val();
            data.select.download_count = $formDownloadCount.val();

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
                        $formPortalType.val(state.select.portal_type);
                        $formProjectType.val(state.select.project_type);
                        $formReportState.val(state.select.report_state);
                        $formDownloadCount.val(state.select.download_count);
                    }
                }
            });


        /**
         *    Buttons & Actions Enable | Disable toggle
         */
        function toggle_button() {
            // Action button Enable / Disable
            const $toggle_button = $(
                '#operatorBtnGroup a[data-target="preview"],' +
                '#operatorBtnGroup a[data-target="view"],' +
                '#operatorBtnGroup a[data-target="download-manifest"],' +
                '#operatorBtnGroup a[data-target="download-document"],' +
                '#operatorBtnGroup a[data-target="download-by-project"],' +
                '#operatorBtnGroup a[data-target="download-by-company"],' +
                // '#operatorBtnGroup a[data-target="plugins"],' +
                '#operatorBtnGroup a[data-target="upload-page"],' +
                '#operatorBtnGroup a[data-target="issue"],' +
                '#operatorBtnGroup a[data-target="transition"],' +
                '#operatorBtnGroup a[data-target="delete"], ' +
                '#operatorBtnGroup a[data-target="check"]');
            const selected_count = $data_table.rows({selected: true}).count();
            if (selected_count) {
                //$toggle_button.show();
                $toggle_button.parent().removeClass('disabled');
                //$toggle_button.css('pointer-events', 'auto');
            } else {
                //$toggle_button.hide()
                $toggle_button.parent().addClass('disabled');
                //$toggle_button.css('pointer-events', 'none');
            }
        }

        function toggle_checkall(e, dt, type, indexes) {
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
        }


        $datable_object.on('draw.dt select.dt deselect.dt', function (e, dt, type, indexes) {
            toggle_button();
            toggle_checkall();
        });

        /**
         * Row selection by Buttons
         */
        $selectDropdown.on('click', '*[data-target]', function (event) {
            //event.stopPropagation();
            event.preventDefault();
            //console.log($(this).data('target'), $(event), event.target, event.relatedTarget)
            const target_data = $(this).data('target');

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
            }
        });


        /**
         * Buttons action
         */
        $('#operatorBtnGroup button[data-target],' +
            '#operatorBtnGroup a[data-target]')
            .on('click confirm.toolbar', null, function (event) {
                //event.stopPropagation();
                event.preventDefault();
                //console.log($(this).data('target'), $(event), event.target);
                const target_data = $(this).data('target');
                const target_list = [
                    'preview', 'view',
                    'issue', 'transition',
                    'download-manifest', 'download-document', 'download-by-project', 'download-by-company',
                    'page-upload', 'plugins', 'create', 'delete', 'check',
                    'fetch-1'
                ];
                //const target_list_all = [/*'import',*/, 'export-all'];
                // if ($.inArray(target_data, target_list) === -1) {
                //         return 0;
                // }

                const $selected_row = $data_table.rows({selected: true}).data();
                // const $selected_row = $data_table.rows( { selected: true } ).nodes();
                let uuid_list = [];
                $selected_row.each(function (element, index) {
                    uuid_list.push(element['DT_RowData']['uuid']);
                    // uuid_list.push($(element).data('uuid'));
                });
                const uuid_length = uuid_list.length;

                let view = '.';
                let target = '_self';
                let extraParameters = {};

                switch (target_data) {
                    // Report
                    case 'preview':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'collective-merging-preview';
                        target = '_black';
                        break;
                    case 'view':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'collective-merging-view';
                        target = '_black';
                        break;

                    // Download
                    case 'download-manifest':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'collective-download-manifest';
                        break;
                    case 'download-document':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'collective-packing-download';
                        extraParameters = {
                            'form.widgets.manifest': true
                        };
                        break;
                    case 'download-by-project':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'collective-packing-download';
                        extraParameters = {
                            'form.widgets.manifest': true,
                            'form.widgets.by': 'project_type'
                        };
                        break;
                    case 'download-by-company':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'collective-packing-download';
                        extraParameters = {
                            'form.widgets.manifest': true,
                            'form.widgets.by': 'submission_company'
                        };
                        break;
                    case 'plugins':
                        const name = $(this).attr('href');
                        view = 'collective-plugins-view';
                        extraParameters = {
                            'form.widgets.by': name
                        };
                        break;

                    // Actions
                    case 'upload-page':
                        view = 'collective-upload-page';
                        break;
                    case 'upload-file':
                        view = 'collective-upload-file';
                        break;
                    case 'issue':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'collective-bulk-issue';
                        break;
                    case 'transition':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        view = 'collective-state-transition';
                        break;

                    // More
                    case 'fetch-1':
                        view = '../gene.transfer-fetch-report-job';
                        extraParameters = {
                            'days': 0,
                            'print_type': 'yesOrNoPrint'
                        };
                        break;
                    case 'delete':
                        if (uuid_length === 0) {
                            return 0;
                        }
                        // dismiss default click, waiting dialog confirm.toolbar event.
                        if (event.type === 'click') {
                            const modal = $('#delete_modal_dialog').modal();
                            modal.find('.modal-body strong').text(uuid_length);
                            return 2;
                        }
                        view = 'collective-bulk-delete';
                        break;
                    //Export
                    case 'check':
                        view = 'collective-check-error';
                        break;
                    default:
                        view = '.';
                        break;
                }

                // !!!! ajax_load make form No Style !!!!
                let data = {
                    uuids: uuid_list,
                    bulk_action: target_data,
                    _authenticator: _authenticator/*, ajax_load: false*/
                };
                // $.extend(data, extraParameters);
                // data = {...data, ...extraParameters, ...$data_table.ajax.params()};
                $data_table.ajax.reload(null, false);
                let params = $data_table.ajax.params();
                const col = params['order']['0']['column'];
                params['columns[' + col + '][data]'] = params['columns'][col]['data'];
                params['order[0][column]'] = col;
                params['order[0][dir]'] = params['order']['0']['dir'];
                params['search[value]'] = params['search']['value'];
                Object.assign(data, extraParameters, $data_table.ajax.params());
                submitForm(view, data, target);

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
                $('#operatorBtnGroup').find('a[data-target="' + target + '"]').triggerHandler('confirm.toolbar');
                $delete_dialog.modal('hide');
            });

        /**
         * Export dilution confirm mode dialog
         */
        const $dilution_dialog = $('#dilution_modal_dialog');
        $dilution_dialog.find('.modal-footer button[data-target="export-dilution"]')
            .on('click', function () {
                const target = $(this).data('target');
                $('#operatorBtnGroup').find('a[data-target="' + target + '"]').triggerHandler('confirm.toolbar');
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
        //
        // $("#form-SearchableHelp")
        //         .popover({
        //                 html: true,
        //                 //title: 'Advanced search instructions'.anchor(),
        //                 content: $('#tooltip-SearchableText').html(),
        //                 template: '<div class="popover" role="tooltip" style="max-width: inherit; ">' +
        //                 '<div class="arrow"></div>' +
        //                 '<h3 class="popover-title"></h3>' +
        //                 '<div class="popover-content"></div></div>',
        //                 placement: 'auto rigth'
        //                 //viewport: '#form-SearchableText'
        //         });
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
                } else if (!field_val && ($formDateFrom.val() || $formDateTo.val())) {
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
        /*$datable_object
            .on('draw.dt', function () {
                $('a._ChangeNote').prepOverlay({
                    subtype: 'ajax',
                    cssclass: 'overlay-changenote',
                    width:'30%',
                    filter: 'h2, #content',
                    formselector: 'form[id="ChangeNoteForm"]',
                    noform: function(el) {return $.plonepopups.noformerrorshow(el, 'close');}
                });
            });*/


        /**
         * Content history popup
         */
/*        $datable_object
            .on('draw.dt', function () {
                $('a._ContentHistory').prepOverlay({
                    subtype: 'ajax',
                    cssclass: 'overlay-history',
                    filter: 'h2, #content-history',
                    urlmatch: '@@historyview',
                    urlreplace: '@@contenthistorypopup'
                });
            });*/


        /**
         * Hover over the element show tooltips
         */
        /*
              $datable_object
                  .on('draw.dt', function () {
                      $('span[data-toggle="tooltip"]').tooltip();
                  });
      */


        /**
         * Move paginate Content to top
         */
        $datable_object
            .on('init.dt', function () {
                $('#datatable_info')
                    .append($('#report_datatable_length').css('display', 'inline'))
                    .append($('#report_datatable_info').css('display', 'inline'));
                $('#datatable_paginate').append($('#report_datatable_paginate'));
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

    /*

         const $batch_list = $('table[id^="form-report"]');  // $('table.datagridwidget-table-view');
         $batch_list.find('>tbody>tr>td[class^="cell-"] [name$=".widgets.report_state"]')
            //.slice(1,-1)
            .on("change", function (/!*event*!/) {
                const $this = $(this);
                if(this.value === 'audited' && !$this.attr('checked')){
                    $this.closest('tr')
                      .find('table[id$="-widgets-template_name"]')
                      .css('visibility','visible');
                }
                else {
                   $this.closest('tr')
                      .find('table[id$="-widgets-template_name"]')
                      .css('visibility', 'hidden');
                }
            });

    */

    /**
     * submitForm
     * To keep URLs intact with link buttons, use the 'form action' instead of 'a href=""'.
     * @param action
     * @param params
     */
    function submitForm(action, params, target) {
        $('#_submitForm').remove();
        const form = $('<form enctype="multipart/form-data" style="display: none;"></form>');
        form.prop('id', '_submitForm');
        form.prop('action', action);
        form.prop('method', 'post');
        form.prop('target', '_self');
        if (target) {
            form.prop('target', target);
        }

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

});


$(function () {
    /**
     * Datagridfield
     * Fill a table cell contents
     * Select a template based on the plan
     */
    "use strict";

    const $batch_list = $('#form-state-transition-widgets-batch_list');
    $batch_list.find('>thead>tr>th[class^="header cell-9"]')
    // text-widget textline-field
        .on("dblclick", function (/*event*/) {

            const self = this;

            let request = $.ajax({
                url: "@@collective-plans-regexp",
                method: "GET",
                dataType: "json",
            });

            request.done(function (data, textStatus, jqXHR) {
                // console.log(data);
                // $(self).parent().children().index($(self))
                //const cellIndex = 2 + self.cellIndex;
                //const $cell_cols = $(self).closest("table").find("tbody>tr>td:nth-child(" + cellIndex + ")>input");
                const call_n = $(self).prop('class').match(/cell-\d+/)[0];
                const $cell_cols = $(self).closest("table").find("tbody>tr>td." + call_n + ">span");
                // const $first_cell = $cell_cols.first();
                // const first_value = $cell_cols.first().val();
                $cell_cols.each(function (index) {
                    const plan = this.innerText;
                    for (const prop in data) {
                        if (plan.match(prop)) {
                            // console.log('Found:', data[prop]);
                            const $cell_cols = $(this).parent().siblings('.cell-11').children("table.ordered-selection-field");
                            const $from_widget = $cell_cols.find("select").first();
                            const $from_button = $cell_cols.find('button[name="from2toButton"]').first();
                            const value = data[prop];
                            if ($from_widget.find('option[value="' + value + '"]').length) {
                                $from_widget.val(value);
                                $from_button.triggerHandler('click');
                                // effects
                                $(this).add($cell_cols).parent()
                                    .effect("highlight").effect("highlight");
                            }
                        }
                    }
                });
            });
            request.fail(function (jqXHR, textStatus, errorThrown) {
                console.warn(textStatus);
            });
            request.always(function (jqXHR_data, textStatus, jqXHR_errorThrown) {
                //
            });

        })


});


$(function () {
    "use strict";
    // Handler for .ready() called.
    /**
     * ControlPanel
     * SMS help
     */

    if ($('body.template-collective-controlpanel').length) {
        $('#form-widgets-message')
            .prevAll('label')
            .children('span.formHelp')
            .contents()
            .after(' <a id="message-help-info" href="@@lis-stringinterp-info">Help</a>');

        $('a#message-help-info').prepOverlay({
            subtype: 'ajax',
            cssclass: 'overlay-message-help',
            filter: '#content-core'
        });
    }

});

// upload file page
window.addEventListener('load', event => {
    const section = document.querySelector('#upload_file_part, #upload_page_part');
    if (section) {
        const keyName = 'DataTables_report_datatable_/Plone/report';
        const data = JSON.parse(section.dataset['datatablepattern']);
        if (data['searchable']) {
            const report_datatable = JSON.parse(sessionStorage.getItem(keyName));
            report_datatable['search']['search'] = data['searchable'];
            const keyValue = JSON.stringify(report_datatable);
            sessionStorage.setItem(keyName, keyValue);
        }
    }

});

window.addEventListener('load', event => {
    const upload_form = document.querySelector('#upload_file_part form#upload-file-form');
    if (upload_form) {
        upload_form.addEventListener('submit', event => {
            $('#ProgressModal .progress-bar').addClass('add_slide_progress');
            $('#ProgressModal').modal('show');
        });
    }
});
