$(document).ready(function() {
$('#id_submit').click(function(event) {
    event.preventDefault();
    $('#id_submit').prop('disabled', 'disabled');
    var data_Form = new FormData($('#bill_form').get(0));
        $.ajax({
            url: '/bill/save/',
            type: 'POST',
            data: data_Form,
            processData: false,
            contentType: false,
            success: function(data) {
            $().message(data);
            $('#id_submit').removeAttr('disabled');
            }
        });
    });

});