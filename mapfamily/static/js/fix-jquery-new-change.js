
$(document).ready(function() {
$('#release_se_id').change(function() {
    var release_id;
    release_id = $('#release_se_id').val();
    problem_id = $('#id_problem_id').val();
    $("#id_div").empty();
    $.get('/fix/ajax_get_components_list/', { pk_release_id: release_id, problem_id: problem_id }, function(data) {
        try {
            var component_list = jQuery.parseJSON(data);
            jQuery('#component_se_id').empty();
            var i = 0;
            for (i = 0; i < component_list.component_list.length; i++) {
                var id = component_list.component_list[i].id;
                var optiontext = component_list.component_list[i].componentName_text;
                $('#component_se_id').prepend("<option value='" + id + "'>" + optiontext + "</option>");
            }
            $('.chosen-component').trigger('chosen:updated');


        }
        catch (err) {
            $().message(data);
            jQuery('#component_se_id').empty();
            $("#release_se_id").val('release_null');
        }
    });
});
});