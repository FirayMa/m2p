
$(document).ready(function() {
    $('#data-table-list').dataTable({
        "order": [[0, "desc"]],
        "columnDefs": [
                {
                    "scrollY": 200,
                    "scrollCollapse": true,
                    "jQueryUI": true
                },
                {
                    "targets": -1,
                    "defaultContent": "test"
                },
                {
                    "targets": 7,
                    "defaultContent": "test"
                }
            ]
    });
    /***************************************************************************
    Publish Article to Zendesk
    *************************************************************************/
    $('#data-table-list tbody ').on('click', 'tr td.td_publish', function() {
        var problemid = $(this).parent('tr.tr_problem_info').find(".problemid").text();
        $(this).find('#id_publish').prop('disabled', 'disabled');
        $.post('/problem/publishaArticle/', { problemid: problemid }, function(data) {
            $(this).find('#id_publish').removeAttr('disabled');
            $().message(data);
            var delay = 3000; //delay in milliseconds
            setTimeout(function() { location.reload(); }, delay);
        });
    });
});