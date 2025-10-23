const servicosCarousel = document.getElementById('servicos-carousel');
document.getElementById('servicos-left').onclick = () => servicosCarousel.scrollBy({ left: -340, behavior: 'smooth' });
document.getElementById('servicos-right').onclick = () => servicosCarousel.scrollBy({ left: 340, behavior: 'smooth' });
