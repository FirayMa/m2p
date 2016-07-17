
$(document).ready(function() {
    /***************************************************************************
    send email
    *************************************************************************/
    $('.action').on('click', 'tr td.td_send_email', function(e) {
        e.preventDefault();
        $('.div_action').isLoading({ text: "Waiting...", position: "overlay" });
        var fixid = $('#fixid').val(); 
         
        $.post('/fix/sendEmail/', { fixid: fixid }, function(data) {
        $(".div_action").isLoading("hide");
            $().message(data);
        });
    });

    /***************************************************************************
    prepare to create KB
    *************************************************************************/
    $('.action').on('click', 'tr td.td_prepare_publish', function(e) {
        e.preventDefault();
        $(".div_action").isLoading({ text: "Waiting...", position: "overlay" });
        var fixid = $('#fixid').val();
        $.post('/fix/prepareToPublishaArticle/', { fixid: fixid }, function(data) {
        $(".div_action").isLoading("hide");
            $().message(data);
            $(this).find('#id_prepare_publish').removeAttr('disabled');
            var delay = 3000; //delay in milliseconds
            setTimeout(function() { location.reload(); }, delay);
        });
    });
 
    /***************************************************************************
    ready to create KB
    *************************************************************************/
    $('.action').on('click', 'tr td.td_ready_publish', function(e) {
        e.preventDefault();
        $('.div_action').isLoading({ text: "Waiting...", position: "overlay" });
        var fixid = $('#fixid').val();
        $.post('/fix/publishaArticle/', { fixid: fixid }, function(data) {
        $(".div_action").isLoading("hide");
            $().message(data);
            var delay = 3000; //delay in milliseconds
            setTimeout(function() { location.reload(); }, delay);
        });
    });
});