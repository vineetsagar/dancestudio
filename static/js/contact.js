$(contact());

function contact(){
	 $("#contactForm").submit(function(e){
		 e.preventDefault();
		 $form = $(this);
		 $.post("/sway/contact/", $(this).serialize(), function(data){
			 if(data['success'] == null){
				 $('#form-feedback').html(data['error']);
			 }else{
				 $('#form-feedback').html(data['success']);
			 }
		 } );
	 });
}