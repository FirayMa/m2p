
$(document).ready(function () {

    $("#id_release_date").datepicker();

    $('#id_product').change(function () {
        var product_id;
        product_id = $('#id_product').val();
        if (product_id == '-1') {
            jQuery('#release_se_id').empty();
            $('#release_se_id').prepend("<option value='-1'>--Select a Release--</option>");
        }
        else {

            $.get('/base/get_release_list/', { product_id: product_id }, function (data) {
                try {
                    var release_list = jQuery.parseJSON(data);
                    jQuery('#release_se_id').empty();
                    var i = 0;

                    for (i = 0; i < release_list.release_list.length; i++) {
                        var id = release_list.release_list[i].id;
                        var text = release_list.release_list[i].version_text;
                        $('#release_se_id').prepend("<option value='" + id + "'>" + text + "</option>");
                    }
                    $('#release_se_id').prepend("<option value='-1'>--Select a Release--</option>");
                }
                catch (err) {
                    $().message(data);
                    jQuery('#release_se_id').empty();
                    $("#release_se_id").val('-1');
                }
            });
        }
    });


    var wrapper = $(".input_fields_wrap"); //Fields wrapper
    var add_button = $("#add_os_button"); //Add button ID

   
    $(add_button).click(function (e) { //on add input button click
        e.preventDefault();
        var os_id = $("#os_se_id").val(); //
        if (os_id == "-1") {
            $().message("Please select an OS first !");
        }
        else {
            var os_text = $("#os_se_id :selected").text(); // 
            
            $(wrapper).append("<div><input type='text' readonly='readonly' name='mytext[]'  style='width:160px' value='"
                       + os_text + "'/><a href='#' class='remove_field'> Remove"
                    + "</a><input type='Hidden' name='myvalue[]' value='"
                    + os_id + "'/></div>"); //add input box;
        }
    });

    $(wrapper).on("click", ".remove_field", function (e) { //user click on remove text
        e.preventDefault();
        $(this).parent('div').remove();
        
    })
    /***************************************************************************************************************************
    save changes
    ****************************************************************************************************************************/
    $("#id_save").click(function (e) { //on add input button click
        e.preventDefault();

        var product = $("#id_product").val();
        if (product == "-1")
        {
            $().message("Please select Product !");
            return
        }
        var version = $("#id_release_version").val();
        if ($.trim(version) == "") {
            $().message("Please input version information !");
            return
        }
        var buildno = $("#id_buildno").val();
        if ($.trim(buildno) == "") {
            $().message("Please input build No. information !");
            return
        }

        var os_list = $('input[name="myvalue[]"]').map(function () {
            return this.value
        }).get()
        if (os_list.length == 0) {
            $().message("Please add OS !");
            return
        }

        var data_release_Form = new FormData($('#release_form').get(0));
        $('#id_save').prop('disabled', 'disabled');
        $.ajax({
            url: '/base/save_release',
            type: 'POST',
            data: data_release_Form,
            processData: false,
            contentType: false,
            success: function (data) {
                
                    $().message("successfully !");
                    var delay = 3000; //delay in milliseconds
                    setTimeout(function () { $(location).attr('href', "/base/" + data + "/release_change"); }, delay);
                
            }
        });
      
    });
});