

/* Smooth scrolling */
// Select all links with hashes
$('a[href*="#"]')
  // Remove links that don't actually link to anything
  .not('[href="#"]')
  .not('[href="#0"]')
  .click(function(event) {
    // On-page links
    if (
      location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '')
      &&
      location.hostname == this.hostname
    ) {
      // Figure out element to scroll to
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      // Does a scroll target exist?
      if (target.length) {
        // Only prevent default if animation is actually gonna happen
        event.preventDefault();
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000, function() {
          // Callback after animation
          // Must change focus!
          var $target = $(target);
          $target.focus();
          if ($target.is(":focus")) { // Checking if the target was focused
            return false;
          } else {
            $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
            $target.focus(); // Set focus again
          };
        });
      }
    }
  });

/* Delete modal */ 
var deleteButtons = document.getElementsByClassName("delete-button")
var deleteModalForm= document.getElementById("DeleteModal-form")

for (var i = 0; i < deleteButtons.length; i++) {


    deleteButtons[i].onclick = function() {
        deleteModalForm.action = this.dataset.url
    }
}



var topics = document.getElementsByClassName("single-topic");


if(topics[0]) {

    topics[0].classList.add('fade-in');

    var i = 1;
    var animate = setInterval (function() {

        topics[i].classList.add("fade-in");

        i++;

        if (i >= topics.length) {

            clearInterval(animate);

        }



    }, 250);

}

$("body").css("min-height", $(window).height() + 30 * $(".single-topic").length)





var timeout;
var topic_id;
$(".single-topic").on("mousemove", function(e) {
    clearTimeout(timeout);
    
    $(".latest-comment-popup").css("left", e.pageX + "px");
    $(".latest-comment-popup").css("top", e.pageY - 170 + "px");
    $(".latest-comment-popup").removeClass("visible"); 
    
    topic_id = $(this).data("topic_id");

    
    timeout = setTimeout(function(){
       
        
        $.getJSON("/ajax/getLatestComment/" + topic_id, function(data) {
           
             
            $("#latestCommentContent").html(data.content);
            $("#latestCommentUser").html(data.email);
            
        });
        
        
        
        $(".latest-comment-popup").addClass("visible");
        
        
        
    }, 500);
});

$(".single-topic").on("mouseout", function() {
    clearTimeout(timeout);
    $(".latest-comment-popup").removeClass("visible");
})




