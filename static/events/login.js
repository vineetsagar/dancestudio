$(function(){
	 $("#loginForm").submit(function(e){
		 e.preventDefault();
		 $form = $(this);
		 $.post("/sway/loginAuth/", $(this).serialize(), function(data){
			 	if(data['error'] == null){
			 		$('#myModal').modal('hide');
			 		window.location.href=data['success'];
			 	}else{
			 		$('#form-feedback').html(data['error']);	
			 	}
		 } );
	 });
});