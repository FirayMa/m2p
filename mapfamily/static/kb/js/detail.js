$(document).ready(function() {
 var text = $('#takepart_in').val();
 var kbid = $('#kbid').val();
 
 var num = /^[1-9]\d*$/;
 $('#id_award').click(function(e){
     e.preventDefault();
     var available_silver = $('#id_v_silver').val();
     $.confirm({ 
                text:'<label>请输入打赏仓库币数量：</label><br/>'+
                '<input type="text" class="silver_text" placeholder="仓库币数量..." value="" id="id_silver"/>'+
                '<label>您当前可用仓库币：'+available_silver+'</label>',
                confirmButton: "打赏",
                cancelButton: "取消",
                dialogClass: "modal-dialog",
                confirm: function() {
                var silver = $('#id_silver').val();
                if (!num.test(silver))
                {
                    $().errormessage('请输入数字...'); 
                    return;
                }
                else{
                    if (parseInt( silver) > parseInt( available_silver))
                    {
                        $().errormessage('您没有足够的仓库币...'); 
                        return;
                    }
                    $.post('/kb/award_kb/', { kbid: kbid, silver:silver }, function(data) {
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
                }   
            },
            cancel: function() {
            
            }
     });
 });
 
 
 
 $('#id_book').click(function(e){
     e.preventDefault();
     var need_moneyr = $('#id_need_money').val();
     var available_silver = $('#id_v_silver').val();
     if(parseInt( available_silver) <parseInt( need_moneyr ))
     {
         $().errormessage('你没有足够的仓库币...');
         return;
     }
     $.confirm({ 
                text:'<label>预约该商品会花掉'+need_moneyr+'仓库币, 确定预约？</label>',
                confirmButton: "预约",
                cancelButton: "取消",
                dialogClass: "modal-dialog",
                confirm: function() {
                $('#id_book').attr('disabled', 'disabled');
                
                $.post('/kb/book_new_product/', { kbid: kbid }, function(data) {
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
                        $('#id_book').removeAttr('disabled');

                    });
                },
                cancel: function() {
                
                }
     });
 });
 
 
 $('#id_recieve').click(function(e){
     e.preventDefault();
     
     $.confirm({ 
                text:'<label>确定领取？</label>',
                confirmButton: "确定",
                cancelButton: "取消",
                dialogClass: "modal-dialog",
                confirm: function() {
                $('#id_recieve').attr('disabled', 'disabled');
                
                $.post('/kb/recieve_gift/', { kbid: kbid }, function(data) {
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
                        $('#id_recieve').removeAttr('disabled');

                    });
                },
                cancel: function() {
                
                }
     });
 });
 
 
 if (text != '报名')
   {
       $('#takepart_in').attr('disabled','disabled');
   }
 $('#takepart_in').click(function(event) {
     event.preventDefault(); 
     $('#id_publish_draft').attr('disabled', 'disabled');
     $.confirm({
            text: "确定参加该活动?",
            confirmButton: "确定",
            cancelButton: "取消",
            dialogClass: "modal-dialog",
            confirm: function() {
            $('#takepart_in').attr('disabled', 'disabled');
            
            $.post('/kb/takepart_in/', { kbid: kbid }, function(data) {
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
 
    $('#id_publish').click(function(event) {
        
        
        $('#id_publish').attr('disabled', 'disabled');
        var formData = new FormData($('#article_form').get(0));
        $.ajax('/kb/savekb/', {
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                if (data['status'] == 'OK') { 
                    var kbid = data['id'];
                    $.confirm({
                        text: "发表成功...",
                        confirmButton: "去看看帖子",
                        cancelButton: "去设置顶图",
                        dialogClass: "modal-dialog",
                        confirm: function() {
                            //去查看帖子详情
                             window.location.href = '/kb/'+kbid+'/kb_detail/'; 
                        },
                        cancel: function() {
                            //去设置顶图
                             window.location.href = '/kb/'+kbid+'/set_kb_top_pic/'; 
                        }
                    });
                }
                else {
                    $('.publish_msg').append('<label class="noteerror" >' + data['msg'] + '</label>'); //
                }
            },
            error: function() {
                console.log('Upload error');
            }
        });
    }); 
var touchStartLocation; 
var touchEndLocation;    
    

$(document).on('touchstart', ".comment_right_div", function(event) {
     touchStartLocation = event.view.scrollY;
});
$(document).on('touchend', ".comment_right_div", function(event) {
     
     touchEndLocation= event.view.scrollY;
     var distance =  (touchEndLocation-touchStartLocation)*(touchEndLocation-touchStartLocation);
     if (distance < 10  )
     {
        event.preventDefault();    
        var comment_text =      $('#id_comment_conent');
        //var comment_content = $.trim(comment_text.val());
        var username = $(this).context.firstElementChild.firstElementChild.outerText;
        $('#id_comment_conent').attr('placeholder', '回复'+username+'：');
        var btn = $('#comment_conent_btn');
        btn.addClass('comment_reply');
        btn.removeClass('comment_ordinary_sent'); 
        $('#current_commentid').val($($(this).context.parentElement).find('.commentid').val()); 
        $('#id_comment_conent').focus(); 
     }
});
    //comment section
    $(document).on('click ', ".comment_right_div", function(event) {
    //$(document).on('click', ".comment_left_div", function(event) {
        event.preventDefault();    
        var comment_text =      $('#id_comment_conent');
        var comment_content = $.trim(comment_text.val());
        var username = $(this).context.firstElementChild.firstElementChild.outerText;
        $('#id_comment_conent').attr('placeholder', '回复'+username+'：');
        var btn = $('#comment_conent_btn');
        btn.addClass('comment_reply');
        btn.removeClass('comment_ordinary_sent'); 
        $('#current_commentid').val($($(this).context.parentElement).find('.commentid').val()); 
        $('#id_comment_conent').focus(); 
    });
 
    //mobile side
    /*
    $(document).on('touchstart', ".comment_right_div", function(event) {
  // $(document).on('touchstart', ".comment_left_div", function(event) {
        event.preventDefault();    
        var comment_text =      $('#id_comment_conent');
        var comment_content = $.trim(comment_text.val());
        var username = $(this).context.firstElementChild.firstElementChild.outerText;
        $('#id_comment_conent').attr('placeholder', '回复'+username+'：');
        var btn = $('#comment_conent_btn');
        btn.addClass('comment_reply');
        btn.removeClass('comment_ordinary_sent'); 
         $('#id_comment_conent').focus();
        $('#current_commentid').val($($(this).context.parentElement).find('.commentid').val()); 
    });
    */
    // 
    $(document).on('click touchstart', ".fa-comment-o", function(event) {
        event.preventDefault();     
        $('#id_comment_conent').removeAttr('placeholder');
        var btn = $('#comment_conent_btn');
        btn.addClass('comment_ordinary_sent');
        btn.removeClass('comment_reply');  
         $('#id_comment_conent').focus();
    }); 
    //comment section
    $(document).on('click touchstart', ".comment_reply", function(event) {
        event.preventDefault();         
        var comment_content = $.trim($('#id_comment_conent').val());
        if (comment_content == '')
        {
            $().errormessage('请输入评论内容...');
            return;
        }
        var is_authenticated = $('#login').val();
        if (is_authenticated == 0) {
            $().errormessage('请先登录...');
            var delay = 3000; //delay in milliseconds
            setTimeout(function() { $(window.location).attr('href', '/login/?next='+window.location.pathname); }, delay);
            return;
        }
        $('#comment_conent_btn').attr('disabled', 'disabled');
         var currentcommentid = $('#current_commentid').val();   
            $.post('/comment/add_replied/', { kbid: kbid, currentcommentid:currentcommentid,  content: comment_content}, function(data) {
                    var status = data['status'];
                    var msg = data['msg']; 
                    if (status == 'OK') {
                        $().message(msg);
                        var delay = 3000; //delay in milliseconds
                        setTimeout(function() { location.reload(true); }, delay);
                    }
                    else { 
                           if (status == 'LOGIN')
                            {
                                $().errormessage('请先登录...');
                                var delay = 3000; //delay in milliseconds
                                setTimeout(function() { $(window.location).attr('href', '/login/?next='+window.location.pathname); }, delay);
                                return;
                            }
                            else
                            {
                                $().errormessage(msg); 
                            }
                    }
                  $('#comment_conent_btn').removeAttr('disabled');
                });
    });
    //comment section
    $(document).on('click touchstart', ".comment_ordinary_sent", function(event) {
        event.preventDefault();         
        var comment_content = $.trim($('#id_comment_conent').val());
        if (comment_content == '')
        {
            $().errormessage('请输入评论内容...');
            return;
        }
        var is_authenticated = $('#login').val();
        if (is_authenticated == 0) {
            $().errormessage('请先登录...');
            var delay = 3000; //delay in milliseconds
            setTimeout(function() { $(window.location).attr('href', '/login/?next='+window.location.pathname); }, delay);
            return;
        }
        $('#comment_conent_btn').attr('disabled', 'disabled');
            
            $.post('/comment/add_fresh/', { kbid: kbid, content: comment_content}, function(data) {
                    var status = data['status'];
                    var msg = data['msg']; 
                    if (status == 'OK') {
                        $().message(msg);
                        var delay = 3000; //delay in milliseconds
                        setTimeout(function() { location.reload(true); }, delay);
                    }
                    else { 
                        if (status == 'LOGIN')
                        {
                            $().errormessage('请先登录...');
                            var delay = 3000; //delay in milliseconds
                            setTimeout(function() { $(window.location).attr('href', '/login/?next='+window.location.pathname); }, delay);
                            return;
                        }
                        else
                        {
                            $().errormessage(msg); 
                        }
                    }
                  $('#comment_conent_btn').removeAttr('disabled');
                });
    });
});