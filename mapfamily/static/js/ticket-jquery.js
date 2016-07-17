
$(document).ready(function() {

    var wrapper = $(".input_fields_wrap");      //Fields wrapper
    var add_button = $(".add_Ticket_button");   //Add button ID

    $(add_button).click(function(e) { //on add input button click
        var TicketNo = $('#id_ticket_no').val();
        e.preventDefault();
        add_button.prop('disabled', 'disabled');
        $.post('/fix/validateIssueNo/', { TicketNo: TicketNo }, function(data) {
            var str = data.toString();
            if (str.length > 1) {
                if (str[0] == "y")//the issue No is correct in the Zendesk
                {
                    var index = str.indexOf("^^");
                    $(wrapper).append("<div><input style='width:450px'  type='text' readonly='readonly' name='mytext[]' value='"
                       + TicketNo + "#" + str.substr(1, index - 1) + "'/><a href='#' class='remove_field'> Remove</a>"+
                       "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Learn more from Zendesk:"+
                           " <a method='get'  target='_blank' href='https://arcserve.zendesk.com/agent/tickets/"+TicketNo+" '>#"+TicketNo +
                           " </a>"); //add input box;
                    $('#id_ticket_no').val('');
                }
                else {
                    $().message(str);
                }
            }
            else {
                $().message("Error in server side!");
            }
            add_button.removeAttr('disabled');
        });
    });

    $(wrapper).on("click", ".remove_field", function(e) { //user click on remove text
        e.preventDefault();
        $(this).parent('div').remove();
    })

    $('#id_submit_ticketToFix').click(function(e) {
    event.preventDefault();
    $('#id_submit_ticketToFix').prop('disabled', 'disabled');
        var data_Form = new FormData($('#add_ticket_form').get(0));
        $.ajax({
            url: '/fix/AddTicketToFix/',
            type: 'POST',
            data: data_Form,
            processData: false,
            contentType: false,
            success: function(data) {
            $().message(data);
            $('#id_submit_ticketToFix').removeAttr('disabled');
            }
        });
    });

});