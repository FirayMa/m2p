
$(document).ready(function() {
    var wrapper = $(".input_fields_wrap"); //Fields wrapper
    var add_button = $("#add_user_button"); //Add button ID


    $(add_button).click(function(e) { //on add input button click
        e.preventDefault();
        var user_id = $("#user_se_id").val(); //
        if (user_id == "-1") {
            $().message("Please select a maintainer first !");
        }
        else {
            var username = $("#user_se_id :selected").text(); // 


            $(wrapper).append("<div><input type='text' readonly='readonly' name='mytext[]'  style='width:160px' value='"
                               + username + "'/><a href='#' class='remove_field'> Remove"
                            + "</a><input type='Hidden' name='myvalue[]' value='"
                            + user_id + "'/></div>"); //add input box;
        }
    });

    $(wrapper).on("click", ".remove_field", function(e) { //user click on remove text
        e.preventDefault();
        $(this).parent('div').remove();
    })

    /***************************************************************************************************************************
    save changes
    ****************************************************************************************************************************/
    $("#id_save").click(function(e) { //on add input button click
        e.preventDefault();
        var product_name = $("#id_product_name").val();
        if ($.trim(product_name) == "") {
            $().message("Please input Product name!");
            return
        }

        var abbreviation = $("#id_abbreviation").val();
        if ($.trim(abbreviation) == "") {
            $().message("Please input abbreviation information !");
            return
        }

        var user_list = $('input[name="myvalue[]"]').map(function() {
            return this.value
        }).get()
        if (user_list.length == 0) {
            $().message("Please add the maintainers !");
            return
        }

        var data_product_Form = new FormData($('#product_form').get(0));
        $('#id_save').prop('disabled', 'disabled');
        $.ajax({
            url: '/base/save_product',
            type: 'POST',
            data: data_product_Form,
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
                    setTimeout(function() { $(location).attr('href', "/base/" + data + "/pruduct_change"); }, delay);
                }
            }
        });

    });
});