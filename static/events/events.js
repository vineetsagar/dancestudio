
	function showRepeatOptions(){
		var x = document.getElementById("repeat_checkbox").checked;
		if(x){
	  		document.getElementById("repeatOptions").style.display = 'block';
	  	}else{
	  		document.getElementById("repeatOptions").style.display = 'none';
	  	}
	}
	
	
	function hideTime(){
  	var x = document.getElementById("all_day").checked;
  	if(x){
  		document.getElementById("start_time").disabled = true;
  		document.getElementById("end_time").disabled = true;
  		document.getElementById("start_time").value='';
  		document.getElementById("end_time").value='';
  	}else{
  		document.getElementById("start_time").disabled = false;
  		document.getElementById("end_time").disabled = false;
  	}
	}
	
	function selectRepeats() {
	  	var x = document.getElementById("selectpicker").value;
	    if(x =='Weekly')  {   
	    $("label#repeat_every_label").replaceWith('weeks');
	    var weekly="<tr class='form-group' ><th>Repeat on:</th><td  id='toreplace'><div id='weekly'  style='display:block'><span >&nbsp;<input id=':2l.dow1' name='MO' type='checkbox' aria-label='Repeat on Monday' title='Monday'><label for=':2l.dow1' title='Monday'>&nbsp;M</label></span><span >&nbsp;<input id=':2l.dow2' name='TU' type='checkbox' checked='' aria-label='Repeat on Tuesday' title='Tuesday'><label for=':2l.dow2' title=''Tuesday'>&nbsp;T</label></span><span >&nbsp;<input id=':2l.dow3' name='WE' type='checkbox' aria-label='Repeat on Wednesday' title='Wednesday'><label for=':2l.dow3' title='Wednesday'>&nbsp;W</label></span><span >&nbsp;<input id=':2l.dow4' name='TH' type='checkbox' aria-label='Repeat on Thursday' title='Thursday'><label for=':2l.dow4' title='Thursday'>&nbsp;T</label></span><span >&nbsp;<input id=':2l.dow5' name='FR' type='checkbox' aria-label='Repeat on Friday' title='Friday'><label for=':2l.dow5' title='Friday'>&nbsp;F</label></span><span>&nbsp;<input id=':2l.dow6' name='SA' type='checkbox' aria-label='Repeat on Saturday' title='Saturday'><label for=':2l.dow6' title='Saturday'>&nbsp;S</label></span><span >&nbsp;<input id=':2l.dow0' name='SU' type='checkbox' aria-label='Repeat on Sunday' title='Sunday'><label for=':2l.dow0' title='Sunday'>&nbsp;S</label></span></div></td></tr>"
	    $("td#toreplace").parent().replaceWith(weekly);
	    }else if(x =='Monthly')  {
	    	$("label#repeat_every_label").replaceWith('months');
	    	var monthly = "<tr ><th>Repeat on:</th><td  id='toreplace'><input id=':3o.domrepeat' name='repeatby' type='radio' checked='' aria-label='Repeat by day of the month' title='Repeat by day of the month'>&nbsp;<label for=':3o.domrepeat' title='Repeat by day of the month'>&nbsp;day of the month</label></span><span >&nbsp;&nbsp;<input id=':3o.dowrepeat' name='repeatby' type='radio' aria-label='Repeat by day of the week' title='Repeat by day of the week'><label for=':3o.dowrepeat' title='Repeat by day of the week'>&nbsp;&nbsp;day of the week</label></span></td></tr>"
			$("td#toreplace").parent().replaceWith(monthly);
	    }
	    else{
	    	$("label#repeat_every_label").replaceWith('days');
	    	var newStr = "<tr  style='display:none'><th>Repeat on:</th><td  id='toreplace'></td></tr>"
	 		   $("td#toreplace").parent().replaceWith(newStr);
	    }
	}
    
  $(function() {
    $( "#datepicker1" ).datepicker();
  });

  // initialize input widgets first
   
$('#startDateTime .time').timepicker({
        'showDuration': true,
        'timeFormat': 'H:mm'
    });

    $('#startDateTime .date').datepicker({
        'format': 'm/d/yyyy',
        'autoclose': true
    });
