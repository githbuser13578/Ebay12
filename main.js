// main.js
document.getElementById('searchForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const query = document.getElementById('queryInput').value;
  const res = await fetch(`/fetch_listings?query=${encodeURIComponent(query)}`);
  const data = await res.json();

  const container = document.getElementById('results');
  container.innerHTML = ''; // Clear previous results

  if (data.error) {
    container.innerHTML = `<p>${data.error}</p>`;
  } else {
    data.items.forEach(item => {
      const resultItem = document.createElement('div');
      resultItem.classList.add('result-item');
      resultItem.innerHTML = `
        <img src="${item.imageUrl}" alt="${item.title}">
        <h3>${item.title}</h3>
        <p>Price: $${item.price}</p>
      `;
      container.appendChild(resultItem);
    });
  }
});
