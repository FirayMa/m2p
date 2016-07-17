
$(document).ready(function() {
    $('#data-table-list').dataTable({
    "order": [
                [0, "asc"]
    ],
    "columnDefs": [
                   {
                       "targets": [4],
                       "visible": false,
                       "scrollY": 200,
                       "scrollCollapse": true,
                       "jQueryUI": true
                   }
    ]
    });

    $('#data-table-list tbody').on("click", "tr td", function (e) {
        var table = $('#data-table-list').DataTable();

        var selected = $(this).parent().hasClass("selected");
        $("#data-table-list tr").removeClass("selected");
        if (!selected)
            $(this).parent().addClass("selected");

        var rowindex = table.cell(this).index().row;
        var os_list = table.cells(rowindex, '').render()[4];
        

        var colindex = $(this).index();
        if (colindex == 1) return; //detail
        var msg = os_list ;
        $(".div_msg").html(msg);
        $("#id_div_msg").dialog({
            autoOpen: false,
            width: 200,
            height: 250,
            title: "OS List:",
            position: ({ my: "right top+65", at: "right top", of: $("#data-table-list").parent() })
        });

        $("#id_div_msg").dialog("open");
    });
});