"use strict";

$(document).ready(function () {
  $(".page__main__slider").owlCarousel({
    items: 1,
    singleItem: true,
    loop: true,
    // responsiveClass: true,
    // nav: true,
    // navText: ["<div class='owl__nav owl__nav__left'><i class='gg-chevron-left'></i></div>","<div class='owl__nav owl__nav__right'><i class='gg-chevron-right'></i></div>" ],
    dots: true,
    // rewind: true,
    lazyLoad: true,
    autoplay: true,
    autoHeight: true,
    autoplayTimeout: 5000 // autoplayHoverPause: true,

  }); // $('.page__main__slider').slick({
  //     //slide: 'div',
  //     slidesToScroll: 1,
  //     slidesToShow: 1,
  //     mobileFirst: true,
  //     //dots: true,
  //     infinite: true,
  //     cssEase: 'ease',
  //     swipe: true,
  //     arrows: true,
  //     autoplay: true,
  //     autoplayspeed: 1000,
  //     lazyLoad: 'ondemand',
  //     prevArrow: $('#prev_main'),
  //     nextArrow: $('#next_main'),
  // });
});
$(document).ready(function () {
  $(".products__slider__main").owlCarousel({
    loop: true,
    responsiveClass: true,
    nav: true,
    navText: ["<div class='owl__nav owl__nav__left'><i class='gg-chevron-left'></i></div>", "<div class='owl__nav owl__nav__right'><i class='gg-chevron-right'></i></div>"],
    dots: false,
    rewind: true,
    lazyLoad: true,
    autoplay: true,
    autoplayTimeout: 3000,
    autoplayHoverPause: true,
    // animateOut: true,
    // animateIn: true,
    responsive: {
      0: {
        items: 1
      },
      600: {
        items: 2
      },
      850: {
        items: 3
      },
      1150: {
        items: 4
      }
    }
  }); // $('.products__slider__main').slick({
  //     //slide: 'div',
  //     slidesToScroll: 4,
  //     slidesToShow: 4,
  //     // mobileFirst: true,
  //     //dots: true,
  //     infinite: true,
  //     cssEase: 'ease',
  //     swipe: true,
  //     arrows: true,
  //     autoplay: true,
  //     autoplayspeed: 1000,
  //     lazyLoad: 'ondemand',
  //     prevArrow: $('#prev_pr1'),
  //     nextArrow: $('#next_pr1'),
  //     responsive: [
  //         {
  //           breakpoint: 1024,
  //           settings: {
  //             slidesToShow: 3,
  //             slidesToScroll: 3,
  //             infinite: true,
  //             dots: true
  //           }
  //         },
  //         {
  //           breakpoint: 600,
  //           settings: {
  //             slidesToShow: 2,
  //             slidesToScroll: 2
  //           }
  //         },
  //         {
  //           breakpoint: 480,
  //           settings: {
  //             slidesToShow: 1,
  //             slidesToScroll: 1
  //           }
  //         }
  //         // You can unslick at a given breakpoint now by adding:
  //         // settings: "unslick"
  //         // instead of a settings object
  //       ]
  // });
});

function showModal(item) {
  $(item).addClass("show");
  $(".pform__wrap__wrapper").addClass("show");
}

function closeModal() {
  $(".pform__wrap").removeClass("show");
  $(".pform__wrap__wrapper").removeClass("show");
}

$(".pform__wrap__close").click(function () {
  closeModal();
});
$(".pform__wrap__wrapper").click(function () {
  closeModal();
});

function setDeliveryActive(current) {
  $("#cart_input_own").removeClass("show");
  $("#cart_input_cura").removeClass("show");
  $(".delivery__method").removeClass("active");
  $(current).addClass("active");
  var curr_content = $(current).attr('data-toogle');
  $(curr_content).addClass("show");
}

function setPaymentActive(current) {
  $(".payment__method").removeClass("active");
  $(current).addClass("active");
}