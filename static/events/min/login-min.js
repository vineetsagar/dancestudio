$(function(){$("#loginForm").submit(function(o){o.preventDefault(),$form=$(this),$.post("/sway/loginAuth/",$(this).serialize(),function(o){null==o.error?($("#myModal").modal("hide"),window.location.href=o.success):$("#form-feedback").html(o.error)})})});