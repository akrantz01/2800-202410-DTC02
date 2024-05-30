import { currentUser } from './user.js';

const form = document.getElementById('form');
const error = document.getElementById('error');

const submit = document.getElementById('submit');
const submitText = document.getElementById('submit-text');
const submitSpinner = document.getElementById('submit-spinner');

const user = await currentUser;
if (user === null || !user.emailVerified) window.location.href = 'login.html';

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const data = Object.fromEntries(new FormData(form));
  for (const key in data) if (data[key].trim().length === 0) delete data[key];

  try {
    spinner(true);

    const result = await send(data);
    window.location.href = `summary.html?uid=${result.id}`;
  } catch (e) {
    let errorMessage;
    // try converting to JSON first
    try {
      const errorArray = JSON.parse(e.message);
      errorMessage = errorArray
        .map((errorMsg) => `${capitalize(errorMsg.loc.toString())}: ${errorMsg.msg}`)
        .join('<br/>');
      // handle the error if it's not in JSON
    } catch (jsonError) {
      errorMessage = e.message;
    }

    // Display the error message
    error.querySelector('span').innerHTML = errorMessage;
    error.classList.remove('hidden');
    console.error(e);
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

const capitalize = (string) => {
  return string.charAt(0).toUpperCase() + string.slice(1);
};
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
