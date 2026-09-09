const filters = document.querySelectorAll('.filter');
const shelves = document.querySelectorAll('.shelf');

filters.forEach((button) => {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    filters.forEach((item) => item.classList.toggle('active', item === button));

    shelves.forEach((shelf) => {
      const cards = shelf.querySelectorAll('.book-card');
      let visible = 0;
      cards.forEach((card) => {
        const show = filter === 'all' || card.dataset.series.split(' ').includes(filter);
        card.hidden = !show;
        if (show) visible += 1;
      });
      shelf.hidden = visible === 0;
    });
  });
});
