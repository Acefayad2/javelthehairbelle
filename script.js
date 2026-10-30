const form = document.querySelector('.book-form');

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
box.querySelector('.book-this').addEventListener('click', () => {
  const style = current.dataset.style;
  current = null;
  box.close();
  const radio = [...form.elements.style].find(r => r.value === style);
  radio.checked = true;
  radio.dispatchEvent(new Event('change', { bubbles: true }));
  document.getElementById('book').scrollIntoView();
  form.elements.name.focus({ preventScroll: true });
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

// Booking form: stays on the page with JS, falls back to thanks.html without it
const statusLine = form.querySelector('.form-status');
const done = document.querySelector('.book-done');
const dateInput = form.elements['preferred-date'];
const now = new Date();
dateInput.min = new Date(now - now.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
form.noValidate = true;

const fieldValid = field => [...field.querySelectorAll('[required]')].every(c => c.checkValidity());
const markField = (field, ok) => {
  field.classList.toggle('bad', !ok);
  field.querySelector('.err').textContent = ok ? '' : field.dataset.error;
  field.querySelectorAll('input').forEach(c => c.setAttribute('aria-invalid', !ok));
};
const clearIfFixed = e => {
  const field = e.target.closest('.field.bad');
  if (field && fieldValid(field)) markField(field, true);
};
form.addEventListener('input', clearIfFixed);
form.addEventListener('change', clearIfFixed);

form.addEventListener('submit', async e => {
  e.preventDefault();
  const fields = [...form.querySelectorAll('.field[data-error]')];
  fields.forEach(f => markField(f, fieldValid(f)));
  const firstBad = fields.find(f => !fieldValid(f));
  if (firstBad) {
    firstBad.querySelector('input').focus();
    return;
  }
  const btn = form.querySelector('[type=submit]');
  const data = new FormData(form);
  btn.disabled = true;
  btn.textContent = 'Sending...';
  statusLine.textContent = '';
  try {
    const res = await fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(data).toString(),
    });
    if (!res.ok) throw new Error(res.status);
    const date = new Date(`${data.get('preferred-date')}T12:00`).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });
    done.querySelector('h3').textContent = `Thanks, ${data.get('name').trim().split(/\s+/)[0]}. Your request is in.`;
    done.querySelector('.done-summary').textContent = `${data.get('style')}, ${date}`;
    done.querySelector('.done-contact').textContent = data.get('contact');
    form.hidden = true;
    done.hidden = false;
    done.focus();
  } catch {
    statusLine.textContent = "That didn't go through. Please try again, or DM @javelthehairbelle on Instagram.";
  } finally {
    btn.disabled = false;
    btn.textContent = 'Send request';
  }
});
done.querySelector('button').addEventListener('click', () => {
  form.reset();
  done.hidden = true;
  form.hidden = false;
  form.elements.name.focus();
});

// The sticky button steps aside once the booking section is on screen
const sticky = document.querySelector('.sticky-book');
new IntersectionObserver(([e]) => sticky.classList.toggle('away', e.isIntersecting))
  .observe(document.getElementById('book'));
