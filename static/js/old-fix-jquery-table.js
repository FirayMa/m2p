
$(document).ready(function() {
$('#tb_old_fix').DataTable({
    "columnDefs": [
                {
                    "targets": -1,
                    "visible": false,
                    "scrollY": 200,
                    "scrollCollapse": true,
                    "jQueryUI": true
                },
                {
                    "targets": 4,
                    "defaultContent": "test"
                }
            ]
});

});