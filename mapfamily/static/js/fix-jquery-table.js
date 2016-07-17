
$(document).ready(function() {
    $('#data-table-list').dataTable({
    "order": [
                [0, "desc"]
        ],
    "columnDefs": [
                        {
                            "targets": [0],
                            "visible": false,
                            "scrollY": 200,
                            "scrollCollapse": true,
                            "jQueryUI": true
                        },
                        {
                            "targets": -1,
                            "defaultContent": "test"
                        }
       ]

    });

    var table = $('#data-table-list').DataTable();
    /***************************************************************************
    send email
    *************************************************************************/
    $('#data-table-list tbody ').on('click', 'tr td.td_send_email', function() {
        $(this).find('#id_send_emai').prop('disabled', 'disabled');
        var rowindex = table.cell(this).index().row;
        var fixid = table.cells(rowindex, '').render()[0];
        $.post('/fix/sendEmail/', { fixid: fixid }, function(data) {
            $(this).find('#id_send_emai').removeAttr('disabled');
            $().message(data);
        });
    });
    /*
    tr = $('#data-table-list').find('tr');
    td_sendEmail = tr.find("td.td_send_email");
    td_sendEmail.bind('click', function(event) {
    td_sendEmail.find($(':button[id="id_send_emai"]')).prop('disabled', 'disabled');
    var rowindex = table.cell(this).index().row;
    var fixid = table.cells(rowindex, '').render()[0];
    $.post('/fix/sendEmail/', { fixid: fixid }, function(data) {
        td_sendEmail.find($(':button[id="id_send_emai"]')).removeAttr('disabled');
        $().message(data);
    });
    });*/
    /***************************************************************************
    prepare to create KB
    *************************************************************************/
    $('#data-table-list tbody ').on('click', 'tr td.td_prepare_publish', function() {
        var rowindex = table.cell(this).index().row;
        var fixid = table.cells(rowindex, '').render()[0];
        $('#id_publish_fixid').val(fixid)
        $(this).find('#id_prepare_publish').prop('disabled', 'disabled');
        $.post('/fix/prepareToPublishaArticle/', { fixid: fixid }, function(data) {
            $().message(data);
            $(this).find('#id_prepare_publish').removeAttr('disabled');
            var delay = 3000; //delay in milliseconds
            setTimeout(function() { location.reload(); }, delay);
        });
    });
    /*
    td_prepare_publish = tr.find("td.td_prepare_publish");
    td_prepare_publish.bind('click', function(event) {
        event.preventDefault();
        var rowindex = table.cell(this).index().row;
        var fixid = table.cells(rowindex, '').render()[0];
        $('#id_publish_fixid').val(fixid)
        td_prepare_publish.find($(':button[id="id_prepare_publish"]')).prop('disabled', 'disabled');
        $.post('/fix/prepareToPublishaArticle/', { fixid: fixid }, function(data) {
            $().message(data);
            td_prepare_publish.find($(':button[id="id_prepare_publish"]')).removeAttr('disabled');
            var delay = 3000; //delay in milliseconds
            setTimeout(function() { location.reload(); }, delay);
        });
    });
    console.dir(td_prepare_publish.data('events'));
    console.dir(td_prepare_publish);*/
    /***************************************************************************
    ready to create KB
    *************************************************************************/
    $('#data-table-list tbody ').on('click', 'tr td.td_ready_publish', function() {
        var rowindex = table.cell(this).index().row;
        var fixid = table.cells(rowindex, '').render()[0];
        $('#id_publish_fixid').val(fixid)
        $(this).find('#id_ready_publish').prop('disabled', 'disabled');
        $.post('/fix/publishaArticle/', { fixid: fixid }, function(data) {
            $().message(data);
            $(this).find('#id_ready_publish').removeAttr('disabled');
            var delay = 3000; //delay in milliseconds
            setTimeout(function() { location.reload(); }, delay);
        });
    });
    /*
    td_ready_publish = tr.find("td.td_ready_publish");
    td_ready_publish.bind('click', function(event) {
        var rowindex = table.cell(this).index().row;
        var fixid = table.cells(rowindex, '').render()[0];
        $('#id_publish_fixid').val(fixid)
        td_ready_publish.find($(':button[id="id_ready_publish"]')).prop('disabled', 'disabled');
        $.post('/fix/publishaArticle/', { fixid: fixid }, function(data) {
            td_ready_publish.find($(':button[id="id_ready_publish"]')).removeAttr('disabled');
            $().message(data);
            var delay = 3000; //delay in milliseconds
            setTimeout(function() { location.reload(); }, delay);
        });
    });
    */
});