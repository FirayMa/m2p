
$(document).ready(function() {
    /***************************************************************************************************************************
    save changes
    ****************************************************************************************************************************/
    $("#id_save").click(function(e) { //on add input button click
        e.preventDefault();
        var language_name = $("#id_language_name").val();
        if ($.trim(language_name) == "") {
            $().message("Please input language name!");
            return
        }

        var data_language_Form = new FormData($('#language_form').get(0));
        $('#id_save').prop('disabled', 'disabled');
        $.ajax({
            url: '/base/save_language',
            type: 'POST',
            data: data_language_Form,
            processData: false,
            contentType: false,
            success: function(data) {
                var str = data.toString();
                if (str[0] == "n")//
                {
                    $().message(str.substr(1, str.length - 1));
                    $('#id_save').removeAttr('disabled');
                } else {
                    $().message("successfully !");
                    var delay = 3000; //delay in milliseconds
                    setTimeout(function() { $(location).attr('href', "/base/" + data + "/language_change"); }, delay);
                }
            }
        });

    });
});