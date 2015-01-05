$(function() {
    $( "#datepicker1" ).datepicker();
  });

  $(function() {
	    $( "#id_start_date" ).datepicker();
	  });
  $(function() {
	    $( "#id_end_date" ).datepicker();
	  });
  $(function() {
	    $( "#id_on" ).datepicker();
	  });

  // initialize input widgets first
  $('.time').timepicker({
      'showDuration': true,
      'timeFormat': 'H:mm'
  });
    
    $("form input[name='repeat']").click(function () { 
    	var x = document.getElementById("id_repeat").checked;
		if(x){
	  		document.getElementById("repeatOptions").style.display = 'block';
	  	}else{
	  		document.getElementById("repeatOptions").style.display = 'none';
	  	}
    });
   
    $("form input[name='all_day']").click(function () {
      	var x = document.getElementById("id_all_day").checked;
      	if(x){
      		document.getElementById("id_start_time").disabled = true;
      		document.getElementById("id_end_time").disabled = true;
      		document.getElementById("id_start_time").value='';
      		document.getElementById("id_end_time").value='';
      	}else{
      		document.getElementById("id_start_time").disabled = false;
      		document.getElementById("id_end_time").disabled = false;
      	}
    });
   
    $('#id_event_type').change(function () {
    	var x = document.getElementById("id_event_type").value;
	    if(x == 3){
	  		document.getElementById("weekly_repeat").style.display = 'block';
	  	}else{
	  		document.getElementById("weekly_repeat").style.display = 'none';
	  	}
    });
   