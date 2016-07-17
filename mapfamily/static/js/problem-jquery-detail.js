
$(document).ready(function() {
    /***************************************************************************
    ready to create KB
    *************************************************************************/
$('.action').on('click', 'tr td.td_publish', function(e) {
        e.preventDefault();
        $('.div_action').isLoading({ text: "Waiting...", position: "overlay" });
        var problemid = $('#id_problemid').val();
        $.post('/problem/publishaArticle/', { problemid: problemid }, function(data) {
        $(".div_action").isLoading("hide");
            $().message(data);
            var delay = 3000; //delay in milliseconds
            setTimeout(function() { location.reload(); }, delay);
        });
    });
});