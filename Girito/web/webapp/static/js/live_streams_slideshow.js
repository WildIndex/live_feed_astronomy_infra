let slideIndex = 0;
    let maxSlides = 5; // Maximum number of visible slides
    showSlides(slideIndex);

    function scrollSlides(n) {
        showSlides(slideIndex += n);
    }

    function showSlides(n) {
        let slides = document.querySelectorAll('.slide');
        if (n >= slides.length - maxSlides + 1) {
            slideIndex = slides.length - maxSlides;
        }
        if (n < 0) {
            slideIndex = 0;
        }
        for (let i = 0; i < slides.length; i++) {
            slides[i].style.display = 'none';
        }
        for (let i = slideIndex; i < slideIndex + maxSlides; i++) {
            if (slides[i]) {
                slides[i].style.display = 'block';
            }
        }
    }