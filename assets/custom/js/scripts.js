var topics = document.getElementsByClassName("single-topic");

topics[0].classList.add('fade-in');

var i = 1;
var animate = setInterval (function() {

    topics[i].classList.add("fade-in");

    i++;

    if (i >= topics.length) {

        clearInterval(animate);

    }



}, 250);

