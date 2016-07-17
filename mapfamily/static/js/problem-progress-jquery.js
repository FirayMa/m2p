
$(document).ready(function() {
    var status = parseInt($('#id_status').val(), 10);
    $('.progress .circle').removeClass().addClass('circle');
    $('.progress .bar').removeClass().addClass('bar');
 
    if (status == 0) {
        var j = status + 2;
    }
    else {
        var j = status + 1;
    }
    var i = 0;
    for (i = 1; i < j; i++) {
        $('.progress .circle:nth-of-type(' + (i + 1) + ')').addClass('active');

        $('.progress .circle:nth-of-type(' + (i) + ')').removeClass('active').addClass('done');

        $('.progress .circle:nth-of-type(' + (i) + ') .label').html('&#10003;');

        $('.progress .bar:nth-of-type(' + (i) + ')').addClass('active');

        $('.progress .bar:nth-of-type(' + (i - 1) + ')').removeClass('active').addClass('done');
    }

});