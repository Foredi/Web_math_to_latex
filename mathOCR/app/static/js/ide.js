$(".sidebar ul li").on("click", function() {
    $(".sidebar ul li.active").removeClass("active");
    $(this).addClass("active");
});

$('.open-btn').on('click', function() {
    $('.sidebar').addClass("active");
});

$('.close-btn').on('click', function() {
    $('.sidebar').removeClass("active");
});

$('.btt').on('click', function() {
    $('.sidebar').toggleClass("collapsed");
    $('.logo').toggleClass("active");
    $('.button-md').toggleClass("active");

});

$('.info').click(function() {
    $('.wrapper').addClass('active-popup');
    $('.upload-image').addClass('hide');
    $('.result-box').addClass('hide');
});
$('.icon-close').click(function() {
    $('.wrapper').removeClass('active-popup');
    $('.upload-image').removeClass('hide');
    $('.result-box').removeClass('hide');
    $('.old-password').removeClass('active');
    $('.new-password').removeClass('active');
    $('button[name="change_password"]').prop('disabled', true);
    $('.edit-password').show();
    $('.password').show();
});
$('.btn-danger').click(function() {
    $('.wrapper').removeClass('active-popup');
    $('.upload-image').removeClass('hide');
    $('.result-box').removeClass('hide');
    $('.old-password').removeClass('active');
    $('.new-password').removeClass('active');
    $('button[name="change_password"]').prop('disabled', true);
    $('.edit-password').show();
    $('.password').show();
});

$('.edit-password').click(function() {
    $('.password').hide();
    $('.old-password').addClass('active');
    $('.new-password').addClass('active');
    $('button[name="change_password"]').prop('disabled', false);
    $(this).hide();
});

$(document).ready(function() {
    let length = $('.latex-text').length;
    let number = length;
    $('.result_' + length).show();
    for (let i = 1; i <= length; i++) {
        if (i != length) {
            $('.result_' + i).hide();
        }
    }
    $('.show-number').text(number + '/' + length);
    $('.btn-arrow-left').click(function() {
        if (number > 1) {
            $('.result_' + number).hide();
            number -= 1;
            $('.result_' + number).show();
        }
        $('.show-number').text(number + '/' + length);
    });
    $('.btn-arrow-right').click(function() {
        if (number < length) {
            $('.result_' + number).hide();
            number += 1;
            $('.result_' + number).show();
        }
        $('.show-number').text(number + '/' + length);
    });
    $('.btn-copy').click(function() {
        let text = $('.result_' + number).text();
        navigator.clipboard.writeText(text);
    });
});

$('.image_{{ image.imageID }}').addClass('active');
  