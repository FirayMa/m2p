$(document).ready(function() { 
   $('.fa-recycle').click(function(event) {
            event.preventDefault(); 
            var current = $(this);
            var path = current.context.parentElement.pathname;
            $.confirm({
                text: "确定删除该帖子?",
                confirmButton: "确定",
                cancelButton: "取消",
                dialogClass: "modal-dialog",
                confirm: function() { 
                $.post(path, function(data) {
                        var status = data['status'];
                        var msg = data['msg']; 
                        if (status == 'OK') {
                            $().message(msg);
                            current.context.parentElement.parentNode.remove();
                        }
                        else { 
                                $().errormessage(msg); 
                        } 
                    });  
                },
                cancel: function() { 
                }
            }); 
    });


   $('.set-fa-diamond').click(function(event) {
            event.preventDefault(); 
            var current = $(this);
            var path = current.context.parentElement.pathname;
            $.confirm({
                text: "设置该帖子为精华帖?",
                confirmButton: "确定",
                cancelButton: "取消",
                dialogClass: "modal-dialog",
                confirm: function() { 
                $.post(path, function(data) {
                        var status = data['status'];
                        var msg = data['msg']; 
                        if (status == 'OK') {
                            $().message(msg);
                            var delay = 3000; //delay in milliseconds
                            setTimeout(function() { location.reload(true); }, delay);
                        }
                        else { 
                                $().errormessage(msg); 
                        } 
                    });  
                },
                cancel: function() { 
                }
            }); 
    });

       $('.cancel-fa-diamond').click(function(event) {
            event.preventDefault(); 
            var current = $(this);
            var path = current.context.parentElement.pathname;
            $.confirm({
                text: "取消帖子为精华帖?",
                confirmButton: "确定",
                cancelButton: "取消",
                dialogClass: "modal-dialog",
                confirm: function() { 
                $.post(path, function(data) {
                        var status = data['status'];
                        var msg = data['msg']; 
                        if (status == 'OK') {
                            $().message(msg);
                            var delay = 3000; //delay in milliseconds
                            setTimeout(function() { location.reload(true); }, delay);
                        }
                        else { 
                                $().errormessage(msg); 
                        } 
                    });  
                },
                cancel: function() { 
                }
            }); 
    });
    
    
     $('.set-to-block-slice').click(function(event) {
            event.preventDefault(); 
            var current = $(this);
            var path = current.context.parentElement.pathname; 
                $.post(path, function(data) {
                        var status = data['status'];
                        var msg = data['msg']; 
                        if (status == 'OK') {
                            $().message(msg);
                            var delay = 3000; //delay in milliseconds
                            setTimeout(function() { location.reload(true); }, delay);
                        }
                        else { 
                                $().errormessage(msg); 
                        } 
                    });  
                
    });
    
       $('.set-to-homepage-slice').click(function(event) {
            event.preventDefault(); 
            var current = $(this);
            var path = current.context.parentElement.pathname; 
                $.post(path, function(data) {
                        var status = data['status'];
                        var msg = data['msg']; 
                        if (status == 'OK') {
                            $().message(msg);
                            var delay = 3000; //delay in milliseconds
                            setTimeout(function() { location.reload(true); }, delay);
                        }
                        else { 
                                $().errormessage(msg); 
                        } 
                    });  
                
    });
});