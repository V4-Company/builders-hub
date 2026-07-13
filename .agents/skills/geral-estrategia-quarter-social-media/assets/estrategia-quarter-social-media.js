(function () {
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide:not(.slide-investimento)'));
  var investimentoSlide = document.querySelector('.slide-investimento');
  var toggleBtn = document.querySelector('.investimento-toggle');
  var counterEl = document.querySelector('.deck-counter');
  var dotsEl = document.querySelector('.dots');
  var current = 0;
  var investimentoAtivo = false;

  function getActiveSlides() {
    return investimentoAtivo && investimentoSlide ? slides.concat([investimentoSlide]) : slides;
  }

  function renderDots() {
    if (!dotsEl) return;
    var active = getActiveSlides();
    dotsEl.innerHTML = '';
    active.forEach(function (_, i) {
      var dot = document.createElement('button');
      dot.className = 'dot' + (i === current ? ' active' : '');
      dot.setAttribute('aria-label', 'Ir para slide ' + (i + 1));
      dot.addEventListener('click', function () { goTo(i); });
      dotsEl.appendChild(dot);
    });
  }

  function goTo(index) {
    var active = getActiveSlides();
    if (index < 0 || index >= active.length) return;
    active.forEach(function (s) { s.classList.remove('active'); });
    current = index;
    active[current].classList.add('active');
    if (counterEl) {
      counterEl.textContent = String(current + 1).padStart(2, '0') + ' / ' + String(active.length).padStart(2, '0');
    }
    renderDots();
  }

  function next() { goTo(current + 1); }
  function prev() { goTo(current - 1); }

  var nextBtn = document.querySelector('.nav-next');
  var prevBtn = document.querySelector('.nav-prev');
  if (nextBtn) nextBtn.addEventListener('click', next);
  if (prevBtn) prevBtn.addEventListener('click', prev);

  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === ' ') next();
    if (e.key === 'ArrowLeft') prev();
    if (e.key === 'Home') goTo(0);
    if (e.key === 'End') goTo(getActiveSlides().length - 1);
  });

  if (toggleBtn && investimentoSlide) {
    toggleBtn.addEventListener('click', function () {
      investimentoAtivo = !investimentoAtivo;
      toggleBtn.textContent = investimentoAtivo ? '− Ocultar investimento' : '+ Mostrar investimento';
      investimentoSlide.classList.toggle('slide-disabled', !investimentoAtivo);
      var active = getActiveSlides();
      goTo(Math.min(current, active.length - 1));
    });
  }

  goTo(0);
})();
