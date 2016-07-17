
$(document).ready(function() {
$('#release_se_id').change(function() {
    var release_id;
    release_id = $('#release_se_id').val();
    $("#id_div").empty();
    $.get('/base/get_components_list/', { release_id: release_id }, function(data) {
        try {
            var component_list = jQuery.parseJSON(data);
            jQuery('#table_component_list').empty();
            var i = 0;
            for (i = 0; i < component_list.component_list.length; i++) {
                var id = component_list.component_list[i].id;
                var optiontext = component_list.component_list[i].componentName_text;
                var row =$("<tr><td><label >"+optiontext
                + "</label></td><td><a href='/base/" + id + "/change_component/' > Change this component</a></td></tr>");
                $("#table_component_list").append(row);
            }
        }
        catch (err) {
            $().message(data);
            jQuery('#table_component_list').empty();
            $("#release_se_id").val('release_null');
        }
    });
});
});