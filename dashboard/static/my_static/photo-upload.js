
$(function () {
   $(".js-upload-photos").click(function () {
       console.log('clicked!');
       $("#fileupload").click();
   });

   $('#fileupload').fileupload({
       dataType: 'json',
       success: function (data) {
           $('#container_content').html(data.html_data) 
       }
   })
});