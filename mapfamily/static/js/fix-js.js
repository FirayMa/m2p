
function getRadioValue(name) {
    var radioes = document.getElementsByName(name);
    for (var i = 0; i < radioes.length; i++) {
        if (radioes[i].checked) {
            var title = document.getElementById("fix_title_id_temp");
            title.value = radioes[i].value;
            break;
        }
    }
    return false;
}

function getSelectValue(name) {
    var selects = document.getElementsByName(name);
    for (var i = 0; i < selects.length; i++) {
        if (selects[i].selected) {
            var title = document.getElementById("fix_title_id_temp");
            title.value = selects[i].value;
            break;
        }
    }
    return false;
}


function getselectValue(name) {
    var select = document.getElementById(name);
    var index = select.selectedIndex; // 
    var text = select.options[index].text; //		
    var value = select.options[index].value; //

    var title = document.getElementById("fix_title_id_temp");
    title.value = text + value;
}
