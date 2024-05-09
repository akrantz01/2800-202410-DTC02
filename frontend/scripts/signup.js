import {
  GoogleAuthProvider,
  createUserWithEmailAndPassword,
  signInWithPopup,
  updateProfile,
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
    const credential = await createUserWithEmailAndPassword(auth, data.email, data.password);
    await updateProfile(credential.user, { displayName: data.name });
    window.location.href = 'home.html';
  } catch (error) {
    let message = error.message;
    if (error.code === 'auth/email-already-in-use') message = 'Email already in use.';
    else if (error.code === 'auth/weak-password') message = 'Password is too weak.';

    displayError(message);
  }
});

// Handle Google sign in
googleSignIn.addEventListener('click', async () => {
  const provider = new GoogleAuthProvider();

  try {
    await signInWithPopup(auth, provider);
    window.location.href = 'home.html';
  } catch (error) {
    if (error.code === 'auth/user-cancelled') return;

    displayError(error.message);
  }
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
