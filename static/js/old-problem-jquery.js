
$(document).ready(function() {

    $('#tb_old_problem tbody').on("click", "tr td", function (e) {
        var table = $('#tb_old_problem').DataTable();

        var selected = $(this).parent().hasClass("selected");
        $("#tb_old_problem tr").removeClass("selected");
        if (!selected)
            $(this).parent().addClass("selected");
        
        var rowindex = table.cell(this).index().row;
        var definition = table.cells(rowindex, '').render()[11];
        var keywords = table.cells(rowindex, '').render()[12];
        var title = $(this).parent().find(".td_title").html();

        var colindex = $(this).index();
        if (colindex == 2) return; //Fix detail
        var msg = "<p><strong><em>Keywords:</em></strong><br /> <pre>" + keywords
        + "</pre></p><p><strong><em>Definition:</em></strong> <br /> <pre>" + definition + "</pre></p>";
        $(".div_msg").html(msg);
        $("#id_div_msg").dialog({
            autoOpen: false,
            width: 750,
            height: 350,
            title: title
        });

        $("#id_div_msg").dialog("open");
    });
});