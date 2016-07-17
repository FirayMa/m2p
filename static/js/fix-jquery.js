
$(document).ready(function() {

    $('#id_ajax').click(function() {
        var catid;
        catid = $(this).attr("data-catid");
        $.get('/fix/ajax_test/', { problem_id: catid }, function(data) {
            $('#fix_title_id_temp').html(data);
            $('#id_pr').hide();
        });
    });


    var wrapper = $(".input_fields_wrap"); //Fields wrapper
    var add_button = $(".add_component_button"); //Add button ID

    var x = 0; //initlal text box count
    $(add_button).click(function(e) { //on add input button click
        e.preventDefault();
        var component_id = $("#component_se_id").val(); //
        if (component_id == "component_null") {
            $().message("Please select a component first !");
        }
        else {
            var component_text = $("#component_se_id :selected").text(); // 
            x++;
            $('#id_component_count').val(x);
            $(wrapper).append("<div><input type='text' readonly='readonly' name='mytext[]'  style='width:360px' value='"
                       + component_text + "'/><a href='#' class='remove_field'> Remove"
                    + "</a><input type='Hidden' name='myvalue[]' value='"
                    + component_id + "'/></div>"); //add input box;
        }
    });

    $(wrapper).on("click", ".remove_field", function(e) { //user click on remove text
        e.preventDefault();
        $(this).parent('div').remove();
        x--;
        $('#id_component_count').val(x);
    })


    /***************************************************************************
    submit fix informations section
    *************************************************************************/
    $('#id_submitfix').click(function(e) {
        e.preventDefault();
        var data_fix_Form = new FormData($('#fix_form').get(0));
        var file_binary_id_list = $('input[name="binary_file_ID"]').map(function() {
            return this.value
        }).get()
        var file_O_id_list = $('input[name="source_O_file_ID"]').map(function() {
            return this.value
        }).get()
        var file_M_id_list = $('input[name="source_M_file_ID"]').map(function() {
            return this.value
        }).get()
        var release = $("#release_se_id").val(); //
        var primary_reviewer = $("#id_primary_reviewer").val(); //
        if (typeof release === "undefined") { release = $("#id_release").val() }
        data_fix_Form.append('file_binary_id_list', file_binary_id_list);
        data_fix_Form.append('file_O_id_list', file_O_id_list);
        data_fix_Form.append('file_M_id_list', file_M_id_list);
        data_fix_Form.append('release', release);
        data_fix_Form.append('primary_reviewer', primary_reviewer);
        $('#id_submitfix').prop('disabled', 'disabled');
        $.ajax({
            url: '/fix/save_fix/',
            type: 'POST',
            data: data_fix_Form,
            processData: false,
            contentType: false,
            success: function(data) {
                var str = data.toString();
                if (str.length > 1) {
                    if (str[0] == "y")//the issue No is correct in the Zendesk
                    {
                        $().message(str.substr(1, str.length - 1));
                        $("#binary_file_name_div").empty();
                        $("#file_O_div").empty();
                        $("#file_M_div").empty();
                        var delay = 3000; //delay in milliseconds
                        setTimeout(function() { history.back(); }, delay);
                    }
                    else {
                        $().message(str.substr(1, str.length - 1));
                    }
                }
                else {
                    $().message("Error in server side!");
                }
                $('#id_submitfix').removeAttr('disabled');
            }
        });
    });

    /***************************************************************************
    submit drift fix informations section
    *************************************************************************/
    $('#id_draft').click(function(e) {
        e.preventDefault();
        var data_fix_Form = new FormData($('#fix_form').get(0));
        var file_binary_id_list = $('input[name="binary_file_ID"]').map(function() {
            return this.value
        }).get()
        var file_O_id_list = $('input[name="source_O_file_ID"]').map(function() {
            return this.value
        }).get()
        var file_M_id_list = $('input[name="source_M_file_ID"]').map(function() {
            return this.value
        }).get()
        var release = $("#release_se_id").val(); //

        if (typeof release === "undefined") { release = $("#id_release").val() }
        data_fix_Form.append('file_binary_id_list', file_binary_id_list);
        data_fix_Form.append('file_O_id_list', file_O_id_list);
        data_fix_Form.append('file_M_id_list', file_M_id_list);
        data_fix_Form.append('release', release);
        $('#id_draft').prop('disabled', 'disabled');
        $.ajax({
            url: '/fix/save_draft_fix/',
            type: 'POST',
            data: data_fix_Form,
            processData: false,
            contentType: false,
            success: function(data) {
                if (typeof data["result"] === "undefined") {
                    $().message(data)
                }
                else {
                    $().message(data["result"]);
                    $('#id_fix_id').val(data["id"]);
                    $('#id_draft_fix_id').val(data["id"]);
                    $('#lb_fixNo').text(data["fixNO"]);
                    //$('#release_se_id').prop('disabled', 'disabled');
                }
                $('#id_draft').removeAttr('disabled');
            }
        });
    });

    $('#product_search_id').change(function() {
    var product_id;
        product_id = $('#product_search_id').val();
        if (product_id == '-1') {
            jQuery('#release_search_id').empty();
            $('#release_search_id').prepend("<option value='-1'>--ALL--</option>");
        }
        else {

            $.get('/fix/get_release_list/', { product_id: product_id }, function(data) {
                try {
                    var release_list = jQuery.parseJSON(data);
                    jQuery('#release_search_id').empty();
                    var i = 0;
                    
                    for (i = 0; i < release_list.release_list.length; i++) {
                        var id = release_list.release_list[i].id;
                        var text = release_list.release_list[i].version_text;
                        $('#release_search_id').prepend("<option value='" + id + "'>" + text + "</option>");
                    }
                    $('#release_search_id').prepend("<option value='-1'>--ALL--</option>");
                }
                catch (err) {
                    $().message(data);
                    jQuery('#release_search_id').empty();
                    $("#release_search_id").val('-1');
                }
            });
        }
    });
    //////////////////////////////////////////////////////////////////////////
    //add file js section
    //////////////////////////////////////////////////////////////////////////
    //1
    var file_binary_wrapper = $(".input_binary_files_wrap"); //binary files name wrapper
    $('#id_upload_binary_file').click(function(e) {
        e.preventDefault();
        var file = $('#id_binary_file').get(0).files[0];
        if (file == null)
            $().message("please select file first !");
        else {
            var dataForm = new FormData($('#file_upload_binary_form').get(0));
            var type = '0'
            dataForm.append('filetype', type);
            $.ajax({
                url: '/fix/postForm/',
                type: 'POST',
                enctype: 'multipart/form-data',
                data: dataForm,
                processData: false,
                contentType: false,
                success: function(data, fillename) {
                    var fileid = data; // data is fileid
                    //var file = $('#id_binary_file').get(0).files[0];
                    var filetext = file.name;

                    $(file_binary_wrapper).append("<div><input type='text' name='binary_file_name' value='"
                                               + filetext + "'/><a href='#' class='remove_field'>Remove</a><input type='Hidden' name='binary_file_ID' value='"
                                               + fileid + "'/></div>"); //add input box;
                    $('#id_binary_file').val('');
                }
            });
        }
    });

    $(file_binary_wrapper).on("click", ".remove_field", function(e) { //user click on remove text
        e.preventDefault();
        var values = $(this).next()[0].value;
        var page = $("#page_id").val();
        $(this).parent('div').remove();
        $.post('/fix/deleteFile/', { fileid: values, page: page }, function(data) {
        });
    })
    //2
    var file_O_wrapper = $(".input_source_O_files_wrap"); //files name wrapper
    $('#upload_source_file_O_btn').click(function(e) {
        e.preventDefault();
        var file = $('#id_original_source_file').get(0).files[0];
        if (file == null)
            $().message("please select file first !");
        else {
            var dataForm = new FormData($('#file_upload_source_O_form').get(0));
            var type = '1'
            dataForm.append('filetype', type);
            $.ajax({
                url: '/fix/postForm/',
                type: 'POST',
                enctype: 'multipart/form-data',
                data: dataForm,
                processData: false,
                contentType: false,
                success: function(data, fillename) {
                    var fileid = data; // data is fileid
                    //var file = $('#id_original_source_file').get(0).files[0];
                    var filetext = file.name;

                    $(file_O_wrapper).append("<div><input type='text' name='source_O_file_name' value='"
                                               + filetext + "'/><a href='#' class='remove_field'>Remove</a><input type='Hidden' name='source_O_file_ID' value='"
                                               + fileid + "'/></div>"); //add input box;
                    $('#id_original_source_file').val('');
                }
            });
        }
    });

    $(file_O_wrapper).on("click", ".remove_field", function(e) { //user click on remove text
        e.preventDefault();
        var values = $(this).next()[0].value;
        var page = $("#page_id").val();
        $(this).parent('div').remove();
        $.post('/fix/deleteFile/', { fileid: values, page: page }, function(data) {
        });
    })
    //3
    var file_M_wrapper = $(".input_source_M_files_wrap"); //files name wrapper
    $('#upload_source_file_M_btn').click(function(e) {
        e.preventDefault();
        var file = $('#id_modified_source_file').get(0).files[0];
        if (file == null)
            $().message("please select file first !");
        else {
            var dataForm = new FormData($('#file_upload_source_M_form').get(0));
            var type = '2'
            dataForm.append('filetype', type);
            $.ajax({
                url: '/fix/postForm/',
                type: 'POST',
                enctype: 'multipart/form-data',
                data: dataForm,
                processData: false,
                contentType: false,
                success: function(data, fillename) {
                    var fileid = data; // data is fileid
                    var filetext = file.name;

                    $(file_M_wrapper).append("<div><input type='text' name='source_M_file_name' value='"
                                                   + filetext + "'/><a href='#' class='remove_field'>Remove</a><input type='Hidden' name='source_M_file_ID' value='"
                                                   + fileid + "'/></div>"); //add input box;
                    $('#id_modified_source_file').val('');
                }
            });
        }
    });

    $(file_M_wrapper).on("click", ".remove_field", function(e) { //user click on remove text
        e.preventDefault();
        var values = $(this).next()[0].value;
        var page = $("#page_id").val();
        $(this).parent('div').remove();
        $.post('/fix/deleteFile/', { fileid: values, page: page }, function(data) {
        });
    })
    //4 new binary file
    var new_binary_file_wrapper = $(".input_new_binary_files_wrap"); //files name wrapper
    $('#id_upload_new__binary_file').click(function(e) {
        e.preventDefault();
        var file = $('#id_new_binary_file').get(0).files[0];
        if (file == null)
            $().message("please select file first !");
        else {
            var dataForm = new FormData($('#file_upload_new_binary_form').get(0));
            var type = '3'
            dataForm.append('filetype', type);
            $.ajax({
                url: '/fix/postForm/',
                type: 'POST',
                enctype: 'multipart/form-data',
                data: dataForm,
                processData: false,
                contentType: false,
                success: function(data, fillename) {
                    var fileid = data; // data is fileid
                    var filetext = file.name;

                    new_binary_file_wrapper.append("<div><input type='text' name='new_binary_file_name' value='"
                                                   + filetext + "'/><a href='#' class='remove_field'>Remove</a><input type='Hidden' name='new_binary_file_ID' value='"
                                                   + fileid + "'/></div>"); //add input box;
                    $('#id_new_binary_file').val('');
                }
            });
        }
    });

    $(new_binary_file_wrapper).on("click", ".remove_field", function(e) { //user click on remove text
        e.preventDefault();
        var values = $(this).next()[0].value;
        $(this).parent('div').remove();
        $.post('/fix/deleteFile/', { fileid: values }, function(data) {
        });
    })
    /***************************************************************************
    validate the prerequisite fix Nos
    *************************************************************************/
    $('#btn_validate_fixNo').click(function(e) {
        e.preventDefault();
        var prefixNos = $('#txt_validate_fixNo').val();
        $.post('/fix/validatefixNo/', { prefixNO: prefixNos }, function(data) {
            $().message(data);
        });
    })
    /***************************************************************************
    validate the issue Nos from Zendesk
    *************************************************************************/
    $('#btn_issueNo').click(function(e) {
        e.preventDefault();
        var issueNo = $('#id_txt_issueNo').val();
        $.post('/fix/validateIssueNo/', { issueNo: issueNo }, function(data) {
            var str = data.toString();
            if (str.length > 1) {
                if (str[0] == "y")//the issue No is correct in the Zendesk
                {
                    var index = str.indexOf("^^");
                    $('#id_issue_subject').text(str.substr(1, index - 1));
                    $().message(str.substr(index + 2, str.length - 2 - index));
                }
                else {
                    $().message(str.substr(1, str.length - 1));
                    $('#id_issue_subject').text('');
                }
            }
            else {
                $().message("Error in server side!");
            }
        });
    })

    $('#id_txt_issueNo').change(function(e) {
        e.preventDefault();
        var TicketNo = $('#id_txt_issueNo').val();
        $.post('/fix/validateIssueNo/', { TicketNo: TicketNo }, function(data) {
            var str = data.toString();
            if (str.length > 1) {
                if (str[0] == "y")//the issue No is correct in the Zendesk
                {
                    var index = str.indexOf("^^");
                    var result = str.substr(1, index - 1)
                    $('#id_issue_subject').text(result);
                    $('#id_txt_issue_subject').val(result)
                    $().message(str.substr(index + 2, str.length - 2 - index));
                }
                else {
                    $().message(str.substr(1, str.length - 1));
                    $('#id_issue_subject').text('');
                    $('#id_txt_issueNo').val('')
                    $('#id_txt_issue_subject').val('')
                }
            }
            else {
                $().message("Error in server side!");
            }
        });
    })

 
    /***************************************************************************
    approval section
    *************************************************************************/
    //not approvaled
    $('#id_not_approve').click(function(e) {
        e.preventDefault();
        var fixid = $('#id_fixid').val();
        var opinion = $('#id_txt_opinion').val();
        if (opinion == '') {
            $().message('Opinion cannot be null');
        }
        else {
            $('#id_not_approve').prop('disabled', 'disabled');
            $.post('/fix/NotApproval/', { fixid: fixid, opinion: opinion }, function(data) {
                $().message(data);
                var delay = 3000; //delay in milliseconds
                setTimeout(function() { location.reload(); }, delay);
            });
        }
    })
    //aprroval
    $('#id_approve').click(function(e) {
        e.preventDefault();
        var fixid = $('#id_fixid').val();
        var opinion = $('#id_txt_opinion').val();
        if (opinion == '') {
            $().message('Opinion cannot be null');
        }
        else {
            $('#id_approve').prop('disabled', 'disabled');
            $.post('/fix/YesApproval/', { fixid: fixid, opinion: opinion }, function(data) {
                $().message(data);
                var delay = 3000; //delay in milliseconds
                setTimeout(function() { location.reload(); }, delay);
            });
        }
    })

    /***************************************************************************
    comment section
    *************************************************************************/
    $('#id_submit_comments').click(function(e) {
        e.preventDefault();
        var content = $('#id_txt_comments').val();
        if (content == '')
            $().message('Comments cannot be null')
        else {
            var app_id = $('#fixid').val();
            var isConfirmed = $('#id_checkbox').prop('checked')  // Boolean true
            if (typeof isConfirmed === "undefined") { isConfirmed = false }

            var isSendEmail = $('#id_is_sendemail').prop('checked')  // Boolean true
            if (typeof isSendEmail === "undefined") { isSendEmail = false }
            $('#id_submit_comments').prop('disabled', 'disabled');
            $.post('/fix/savecomment/', { app_id: app_id, content: content, isConfirmed: isConfirmed, isSendEmail: isSendEmail }, function(data) {

                if (isConfirmed) {// reload
                    var delay = 2000; //delay in milliseconds
                    setTimeout(function() { location.reload(); }, delay);
                }
                else {
                    var d = new Date();
                    $(".comment_wrap").append("<tr><td>" + data["username"] + "||" + d.toLocaleString().toLowerCase() + "</td></tr>"); //add input box;
                    $(".comment_wrap").append("<tr><td>" + content + "</td></tr>"); //add input box;
                    $('#id_txt_comments').val('');
                }
                $().message(data["result"]);
                $('#id_submit_comments').removeAttr('disabled');
            });
        }
    })


    /***************************************************************************
    save the new binary files change uploaded by creator
    *************************************************************************/
    $('#id_save_new_binaries').click(function(e) {
        e.preventDefault();
        var fixid = $('#fixid').val();
        var new_binary_file_id_list = $('input[name="new_binary_file_ID"]').map(function() {
            return this.value
        }).get()
        var formdata = new FormData($('#file_upload_new_binary_form').get(0));
        formdata.append('new_binary_file_id_list', new_binary_file_id_list);
        formdata.append('fixid', fixid);
        $('#id_save_new_binaries').prop('disabled', 'disabled');
        $.ajax({
            url: '/fix/saveNewBinaries/',
            type: 'POST',
            data: formdata,
            processData: false,
            contentType: false,
            success: function(data) {
                var str = data.toString();
                if (str.length > 1) {
                    if (str[0] == "y")//the issue No is correct in the Zendesk
                    {
                        $().message(str.substr(1, str.length - 1));
                        var delay = 3000; //delay in milliseconds
                        setTimeout(function() { history.back(); }, delay);
                    }
                    else {
                        $().message(str.substr(1, str.length - 1));
                    }
                }
                else {
                    $().message("Error in server side!");
                }
                $('#id_save_new_binaries').removeAttr('disabled');
            }
        });
    });
});