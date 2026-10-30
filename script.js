// Mobile menu
const menuBtn = document.querySelector('.menu-btn');
const nav = document.getElementById('nav');
const setMenu = open => {
  nav.classList.toggle('open', open);
  menuBtn.setAttribute('aria-expanded', open);
};
menuBtn.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
nav.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });

// Gallery filters
const shots = [...document.querySelectorAll('.shot')];
const filterBtns = [...document.querySelectorAll('.filters button')];
const applyFilter = group => {
  shots.forEach(s => { s.hidden = group !== 'all' && !s.dataset.group.split(' ').includes(group); });
  filterBtns.forEach(b => b.setAttribute('aria-pressed', b.dataset.filter === group));
};
filterBtns.forEach(b => b.addEventListener('click', () => applyFilter(b.dataset.filter)));
document.querySelectorAll('.tile').forEach(t => t.addEventListener('click', () => applyFilter(t.dataset.filter)));

// Lightbox, stepping only through photos the current filter shows
const box = document.querySelector('.box');
const boxImg = box.querySelector('img');
const boxCap = box.querySelector('figcaption span');
const boxLink = box.querySelector('figcaption a');
let current = null;
const visible = () => shots.filter(s => !s.hidden).map(s => s.querySelector('button'));
const show = btn => {
  current = btn;
  boxImg.src = btn.dataset.full;
  boxImg.alt = btn.querySelector('img').alt;
  boxCap.textContent = btn.dataset.caption;
  boxLink.href = btn.dataset.post;
};
const step = dir => {
  const list = visible();
  show(list[(list.indexOf(current) + dir + list.length) % list.length]);
};
document.querySelector('.grid').addEventListener('click', e => {
  const btn = e.target.closest('button');
  if (btn) { show(btn); box.showModal(); }
});
box.querySelector('.box-close').addEventListener('click', () => box.close());
box.querySelector('.prev').addEventListener('click', () => step(-1));
box.querySelector('.next').addEventListener('click', () => step(1));
box.addEventListener('click', e => { if (e.target === box) box.close(); });
box.addEventListener('keydown', e => {
  if (e.key === 'ArrowLeft') step(-1);
  if (e.key === 'ArrowRight') step(1);
});
box.addEventListener('close', () => current && current.focus());

// Clips play only while on screen, and never for reduced-motion visitors
const clips = document.querySelectorAll('.clip-row video');
if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
  clips.forEach(v => { v.controls = true; });
} else {
  const io = new IntersectionObserver(entries => {
    entries.forEach(({ target, isIntersecting }) => {
      if (isIntersecting) target.play().catch(() => { target.controls = true; });
      else target.pause();
    });
  }, { threshold: .4 });
  clips.forEach(v => io.observe(v));
}
