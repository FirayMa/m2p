
$(document).ready(function() {
$('#tb_old_problem').DataTable({
    "columnDefs": [
                {
                    "targets": -1,
                    "visible": false
                },
                {
                    "targets": -2,
                    "visible": false
                },
                {
                    "targets": 4,
                    "defaultContent": "test"
                }
            ]
});
});