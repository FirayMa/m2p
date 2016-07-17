
$(document).ready(function() {
    $('#tb_old_fix tbody').on("click", "td", function(e) {
        var table = $('#tb_old_fix').DataTable();

        var selected = $(this).parent().hasClass("selected");
        $("#tb_old_fix tr").removeClass("selected");
        if (!selected)
            $(this).parent().addClass("selected");

        var msg;
        var index;
        var title;
        index = $(this).index();
        var rowindex = table.cell(this).index().row;
        if (index == 2 || index == 0) return;
        if (index == 6)// problem column was clicked, show problem detail in dialog
        {
            e.preventDefault();
            var problemNo = $(this).text();
            if (problemNo == 'None') return;
            //var patchid = table.cells(rowindex, '').render()[0];// $(this).parent().find(".td_patchid").text();
            var patchid = $(this).parent().find('.td_name').text()
            patchid = $.trim(patchid)
            $.get('/olddata/get_problem/', { problemNo: problemNo, patchid: patchid }, function(data) {
                try {
                    if (typeof data["msg"] === "undefined") {
                        msg = data;
                        title = "error"
                    }
                    else {
                        msg = data["msg"];
                        title = data["title"];
                    }
                    msg = "<pre>" + msg + "</pre>";
                    $(".div_msg").html(msg);
                    $("#id_div_msg").dialog({
                        autoOpen: false,
                        width: 720,
                        height: 650,
                        //position: ({ my: "right top+35", at: "right top", of: $("#tb_old_fix").parent().parent() }),
                        title: title
                    });

                    $("#id_div_msg").dialog("open");
                }
                catch (err) {
                    $().message(data);
                }
            });
        }
        else//show fix readme.txt
        {

            var msg = table.cells(rowindex, '').render()[8];

            title = $(this).parent().find(".td_title").text();
            msg = "<pre >" + msg + "</pre>";
            $(".div_msg").html(msg);
            $("#id_div_msg").dialog({
                autoOpen: false,
                width: 720,
                height: 650,
                //position: ({ my: "right top+35", at: "right top", of: $("#tb_old_fix").parent().parent() }),
                title: title
            });
        }



        $("#id_div_msg").dialog("open");
    });
});