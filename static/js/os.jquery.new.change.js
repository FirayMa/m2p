
$(document).ready(function() {
    /***************************************************************************************************************************
    save changes
    ****************************************************************************************************************************/
    $("#id_save").click(function(e) { //on add input button click
        e.preventDefault();
        var os_name = $("#id_os_name").val();
        if ($.trim(os_name) == "") {
            $().message("Please input OS name!");
            return
        }

        var data_os_Form = new FormData($('#os_form').get(0));
        $('#id_save').prop('disabled', 'disabled');
        $.ajax({
            url: '/base/save_OS',
            type: 'POST',
            data: data_os_Form,
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
                    setTimeout(function() { $(location).attr('href', "/base/" + data + "/OS_change"); }, delay);
                }
            }
        });

    });
});