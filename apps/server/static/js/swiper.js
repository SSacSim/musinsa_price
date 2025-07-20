// static/js/swiper-init.js
const swiper = new Swiper('.swiper', {
    loop: true,
    autoplay: {
        delay: 3000,
    },
    slidesPerView: 5,
    spaceBetween: 0,    // 간격 줄임
    centeredSlides: true,  // 중앙 정렬
});