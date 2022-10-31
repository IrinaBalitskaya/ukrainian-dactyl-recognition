$(function(){
    window.setInterval(function(){
        updateTranslation()
    }, 1000)

   function updateTranslation(){
     $.ajax({
        url: "/translation",
        type: "GET",
        dataType: "json",
        success: function(data){
            $(translation_textarea).replaceWith(data)
        }
     });
   }
});

$(document).on('click','#button_clear',function(){
     $.ajax({
        url: "/clear_textarea",
        type: "DELETE"
     });
});

$(document).on('click','#button_erase',function(){
     $.ajax({
        url: "/erase_letter",
        type: "DELETE"
     });
});

$(document).on('click','#button_start',function(){
     $.ajax({
        url: "/start_pause_webcam",
        type: "PUT",
        contentType: "application/json",
        dataType: 'json',
        data: JSON.stringify({
            btn_text: $(this).text()
        }),
        success: function(response){
            $("#button_start").text(response.btn_text)
        }
     });
});