import { currentUser } from './user.js';

const BACKEND_URL = 'http://localhost:5000';

const form = document.getElementById('form');

const user = await currentUser;
if (user === null) window.location.href = 'login.html';

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const data = Object.fromEntries(new FormData(form));
  for (const key in data) if (data[key].trim().length === 0) delete data[key];

  // TODO: show loading spinner

  const response = await fetch(BACKEND_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${await user.getIdToken()}`,
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    // TODO: handle errors properly
    const message = await response.text();
    console.error(message);
    return;
  }

  const result = await response.json();
  window.location.href = `summary.html?uid=${result.id}`;
});
