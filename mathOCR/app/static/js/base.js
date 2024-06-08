$(".navigation ul li").on("click", function() {
    $(".navigation ul li.active").removeClass("active");
    $(this).addClass("active");
});

$(".login-link").on("click", function() {
    $(".login").addClass("active");
    $(".register").removeClass("active");
});

$(".register-link").on("click", function() {
    $(".register").addClass("active");
    $(".login").removeClass("active");
});

$(".btnPopup").on("click", function() {
    $(".wrapper").addClass("active-popup");
    $(".content").addClass("active-popup");
});

$(".icon-close").on("click", function() {
    $(".wrapper").removeClass("active-popup");
    $(".content").removeClass("active-popup");
});

$(document).ready(function(){
    $('.parallax').click(function(event){
        event.preventDefault();
        $(this).addClass('active');
        $('.sec').addClass('active');
        $('html, body').animate({
            scrollTop: $('.sec').offset().top
        }, 'fast');
    });
});

$(window).scroll(function(){
    if($(window).scrollTop() == 0){
        $('.parallax').removeClass('active');
        $('.sec').removeClass('active');
        $('.about').removeClass('active');
        $('.footer').removeClass('active');
        $('.home').addClass('active');
    }
});

$(document).ready(function(){
    $('.about').click(function(event){
        event.preventDefault();
        $(this).addClass('active');
        $('.footer').addClass('active');
        $('html, body').animate({
            scrollTop: $('.footer').offset().top
        }, 'fast');
    });
});
