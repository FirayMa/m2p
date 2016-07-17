
$(document).ready(function() {
    function getWidth() {
        if (self.innerWidth) {
            return self.innerWidth;
        }
        
        if (document.documentElement && document.documentElement.clientHeight) {
            return document.documentElement.clientWidth;
        }
        
        if (document.body) {
            return document.body.clientWidth;
        }
    }
    
    function getHeight() {
        if (self.innerHeight) {
            return self.innerHeight;
        }
        
        if (document.documentElement && document.documentElement.clientHeight) {
            return document.documentElement.clientHeight;
        }
        
        if (document.body) {
            return document.body.clientHeight;
        }
    }
    var menuwidth=230;
    var screenwidth = window.innerWidth;
    var left =  (screenwidth - menuwidth)/2-12;
    
    $('.background_div').css("height", getHeight());
    $('.background_div').css("width", getWidth()); 
    $('.background_div').css("background-image", "url(/static/img/IMG_0926.JPG)");
    
});