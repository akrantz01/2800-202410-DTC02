import { sendPasswordResetEmail } from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js';

import { redirectToHome } from './shared.js';
import { auth } from '../firebase.js';
import { currentUser } from '../user.js';

const form = document.getElementById('form');
const status = document.getElementById('status');

if ((await currentUser) !== null) redirectToHome();

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const data = Object.fromEntries(new FormData(form));

  await sendPasswordResetEmail(auth, data.email);

  form.classList.add('hidden');
  status.classList.remove('hidden');
});
