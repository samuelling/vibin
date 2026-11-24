/* vibin: copy buttons, done ticks, and the route's "you are here". No libraries. */
(function () {
  'use strict';

  // ---- copy buttons on everything you might paste ----
  function copyText(text, btn) {
    function done() { var was = btn.textContent; btn.textContent = 'Copied'; btn.classList.add('did'); setTimeout(function () { btn.textContent = was; btn.classList.remove('did'); }, 1400); }
    function fallback() {
      var ta = document.createElement('textarea'); ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); done(); } catch (e) { btn.textContent = 'Select and copy'; }
      document.body.removeChild(ta);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, fallback); else fallback();
  }
  function addCopy(host, source) {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'copy'; b.textContent = 'Copy';
    b.addEventListener('click', function () { copyText(source.textContent.trim(), b); });
    host.appendChild(b);
  }
  Array.prototype.forEach.call(document.querySelectorAll('.say pre, .type pre'), function (pre) { addCopy(pre.parentNode, pre); });
  Array.prototype.forEach.call(document.querySelectorAll('.more li'), function (li) {
    var span = document.createElement('span'); while (li.firstChild) span.appendChild(li.firstChild); li.appendChild(span); addCopy(li, span);
  });

  // ---- done ticks, remembered on this device only ----
  var KEY = 'vibin.done', done = {};
  try { done = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { done = {}; }
  function paint() {
    Array.prototype.forEach.call(document.querySelectorAll('.tick'), function (t) {
      var on = !!done[t.dataset.step]; t.setAttribute('aria-pressed', on ? 'true' : 'false'); t.textContent = on ? '☑ Done' : '☐ Done';
      var link = document.querySelector('.toc a[href="#' + t.dataset.step + '"]'); if (link) link.classList.toggle('done', on);
    });
  }
  Array.prototype.forEach.call(document.querySelectorAll('.tick'), function (t) {
    t.addEventListener('click', function () {
      done[t.dataset.step] = !done[t.dataset.step];
      try { localStorage.setItem(KEY, JSON.stringify(done)); } catch (e) { /* private mode: ticks last until you leave */ }
      paint();
    });
  });
  paint();

  // ---- you are here ----
  var links = {}, toc = document.querySelector('.toc ol');
  Array.prototype.forEach.call(document.querySelectorAll('.toc a'), function (a) { links[a.getAttribute('href').slice(1)] = a; });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        Object.keys(links).forEach(function (k) { links[k].classList.remove('here'); });
        var a = links[e.target.id]; if (!a) return;
        a.classList.add('here');
        // on a phone the route is a strip: keep the current step in view
        if (toc && toc.scrollWidth > toc.clientWidth) toc.scrollTo({ left: a.offsetLeft - toc.offsetLeft - 12, behavior: 'smooth' });
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    Array.prototype.forEach.call(document.querySelectorAll('.doc > section'), function (s) { io.observe(s); });
  }
})();
