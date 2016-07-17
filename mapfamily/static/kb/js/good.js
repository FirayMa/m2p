$(document).ready(function() {
    
    $(document).on('touchstart', ".fa-thumbs-up", function() {
    event.preventDefault();  
    var current = $(this);
 
    var kbid = $('#kbid').val();
    var count =current.context.outerText;
    //get ingeter from string
    count = count.match(/\d/g).join("");
    count = parseInt(count);
   
    //var current = $(this);
    $.post('/kb/good_add/', { kbid: kbid }, function(data) {
        var status = data['status']; 
             if (status == 'OK')
            { 
                current.addClass('fa-thumbs-up');
                current.removeClass('fa-thumbs-o-up');
                current.text(data['good_count'].toString());
            }
            else
            {
                 var msg = data['msg'];
                $().errormessage(msg); 
            }
       
            
        });
    });
    
    
    $(document).on('click', ".fa-thumbs-up", function() {
    event.preventDefault();
    
    var current = $(this); 
    
    var kbid = $('#kbid').val();
    var count = current.context.outerText;
    //get ingeter from string
    count = count.match(/\d/g).join("");
    count = parseInt(count);
 
    //var current = $(this);
    $.post('/kb/good_add/', { kbid: kbid }, function(data) {
        var status = data['status'];
        var msg = data['msg'];
        
        if (status == '1')
        {
             $().errormessage(msg); 
            var delay = 3000; //delay in milliseconds
            setTimeout(function() { $(window.location).attr('href', '/login/?next='+window.location.pathname); }, delay);
        }
        else{
             if (status == '0')
            {
                
                current.addClass('fa-thumbs-up');
                current.removeClass('fa-thumbs-o-up');
                current.text(love + (count+1).toString());
            }
            else
            {
                $().errormessage(msg); 
            }
        }
            
        });
    }); 
});