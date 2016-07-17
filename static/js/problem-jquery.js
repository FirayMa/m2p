
$(document).ready(function() {
    /***************************************************************************
    submit Problem informations section
    *************************************************************************/
    $('#id_submitproblem').click(function(e) {
        e.preventDefault();
        var data_problem_Form = new FormData($('#problem_form').get(0));
        $('#id_submitproblem').prop('disabled', 'disabled');
        $.ajax({
            url: '/problem/save_problem/',
            type: 'POST',
            data: data_problem_Form,
            processData: false,
            contentType: false,
            success: function(data) {
            $().message(data);
                $('#id_submitproblem').removeAttr('disabled');
                 var delay = 3000; //delay in milliseconds
                 setTimeout(function() { history.back(); }, delay);
            }
        });
    });
    /***************************************************************************
    submit draft Problem informations section
    *************************************************************************/
    $('#id_draft').click(function(e) {
        e.preventDefault();
        var data_problem_Form = new FormData($('#problem_form').get(0));
        $('#id_draft').prop('disabled', 'disabled');
        $.ajax({
           url: '/problem/save_draft_problem/',
            type: 'POST',
            data: data_problem_Form,
            processData: false,
            contentType: false,
            success: function(data) {
                $().message(data["result"]);
                $('#problem_id').val(data["id"]);
                $('#id_draft_probelm_id').val(data["id"]);
                $('#id_draft').removeAttr('disabled');
            }
        });
    });

    /***************************************************************************
    comment section
    *************************************************************************/
    $('#id_submit_comments').click(function(e) {
        e.preventDefault();
        var content = $('#id_txt_comments').val();
        var app_id = $('#id_apps_id').val();
        $('#id_submit_comments').prop('disabled', 'disabled');
        var isSendEmail = $('#id_is_sendemail').prop('checked')  // Boolean true
        if (typeof isSendEmail === "undefined") { isSendEmail = false }
        $.post('/problem/savecommnet/', { app_id: app_id, content: content, isSendEmail: isSendEmail }, function(data) {
        $().message(data["result"]);
        var d = new Date();
             $(".comment_wrap").append("<tr><td>" + data["username"] + "||" + d.toLocaleString().toLowerCase() + "</td></tr>"); //add input box;
             $(".comment_wrap").append("<tr><td>" + content + "</td></tr>"); //add input box;
             $('#id_txt_comments').val('');
             $('#id_submit_comments').removeAttr('disabled');
        });
    })

    /***************************************************************************
    approval section
    *************************************************************************/
    //not approvaled
    $('#id_not_approve').click(function(e) {
        e.preventDefault();
        var problemid   = $('#id_problemid').val();
        var opinion = $('#id_txt_opinion').val();
        $('#id_not_approve').prop('disabled', 'disabled');
        $.post('/problem/NotApproval/', { problemid: problemid, opinion: opinion }, function(data) {
            $().message(data);
            var delay = 3000; //delay in milliseconds
            setTimeout(function() { history.back(); }, delay);
        });
    })
    //aprroval
    $('#id_approve').click(function(e) {
        e.preventDefault();
        var problemid   = $('#id_problemid').val();
        var opinion = $('#id_txt_opinion').val();
        $('#id_approve').prop('disabled', 'disabled');
        $.post('/problem/YesApproval/', { problemid: problemid, opinion: opinion }, function(data) {
            $().message(data);
            var delay = 3000; //delay in milliseconds
            setTimeout(function() { history.back();  }, delay);
        });
    })
});