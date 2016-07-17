
$(document).ready(function() {
    $('#data-table-list').dataTable({
    "order": [
                [0, "asc"]
    ],
    "columnDefs": [
                   {
                       "targets": [2],
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
        var os_list = table.cells(rowindex, '').render()[2];
        

        var colindex = $(this).index();
        //if (colindex == 1) return; //detail
        var msg = os_list ;
        $(".div_msg").html(msg);
        $("#id_div_msg").dialog({
            autoOpen: false,
            width: 200,
            height: 250,
            title: "Maintainers:",
            position: ({ my: "right top+265", at: "right top", of: $("#data-table-list").parent() })
        });

        $("#id_div_msg").dialog("open");
    });
});