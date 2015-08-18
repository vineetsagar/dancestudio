$(comments());

function comments(){
	 $("#commentsForm").submit(function(e){
		 e.preventDefault();
            var form = $(e.target);
            $.post( form.attr("action"), form.serialize(), function(res){
                $('#commentsModal').modal('toggle')
            });
	 });
}

 $('body').on('hidden.bs.modal', '.modal', function () {
        $(this).removeData('bs.modal');
      });
