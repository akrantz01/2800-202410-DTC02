import { currentUser } from './user.js';

const form = document.getElementById('form');
const error = document.getElementById('error');

const submit = document.getElementById('submit');
const submitText = document.getElementById('submit-text');
const submitSpinner = document.getElementById('submit-spinner');

const user = await currentUser;
if (user === null) window.location.href = 'login.html';

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const data = Object.fromEntries(new FormData(form));
  for (const key in data) if (data[key].trim().length === 0) delete data[key];

  try {
    spinner(true);

    const result = await send(data);
    window.location.href = `summary.html?uid=${result.id}`;
  } catch (e) {
    console.error(e);

    error.querySelector('span').textContent = e.message;
    error.classList.remove('hidden');
  } finally {
    spinner(false);
  }
});

/**
 * Send data to the backend for analysis
 *
 * @param {object} data the data to send to the backend
 * @returns {object} the response from the backend
 */
async function send(data) {
  const response = await fetch(import.meta.env.VITE_BACKEND_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${await user.getIdToken()}`,
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message);
  }

  return await response.json();
}

/**
 * Toggle the visibility of the loading spinner
 *
 * @param {boolean} enabled whether to show the spinner
 */
function spinner(enabled) {
  submitText.style.display = enabled ? 'none' : 'block';
  submitSpinner.style.display = enabled ? 'flex' : 'none';
  submit.disabled = enabled;
}
