$(document).ready(function(){
    
	//will make pages fade in
    $('body').hide().fadeIn(1000);
	
	$('.firstHeader').hide().fadeIn(1200);
	$('.card').hide().fadeIn(1200);
	
});

//Code to scroll to certain part of page when nav is clicked
$(function() {
  $('a[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
});

//Code for aninmating images so that they flip when hovered over
//highlight nav items in a unique way (maybe create box around or underline)