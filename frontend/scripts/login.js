import {
  GoogleAuthProvider,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  signInWithPopup,
} from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js';

import { auth } from './firebase.js';

const form = document.querySelector('form');
const googleSignIn = document.getElementById('signin-google');
const errorContainer = document.getElementById('error');

// Handle email & password sign in
form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const data = Object.fromEntries(new FormData(form));

  try {
    await signInWithEmailAndPassword(auth, data.email, data.password);
  } catch (error) {
    let message = error.message;
    if (error.code === 'auth/invalid-credential') message = 'Invalid email or password.';

    displayError(message);
  }
});

// Handle Google sign in
googleSignIn.addEventListener('click', async () => {
  const provider = new GoogleAuthProvider();

  try {
    await signInWithPopup(auth, provider);
  } catch (error) {
    if (error.code === 'auth/user-cancelled') return;

    displayError(error.message);
  }
});

onAuthStateChanged(auth, (user) => {
  if (user) window.location.href = 'home.html';
});

/**
 * Display an error message to the user
 *
 * @param {string} message the message to display
 */
function displayError(message) {
  errorContainer.querySelector('span').textContent = message;
  errorContainer.classList.remove('hidden');
}
