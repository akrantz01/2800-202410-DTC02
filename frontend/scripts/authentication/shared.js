import {
  GoogleAuthProvider,
  signInWithPopup,
} from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js';

import { auth } from '../firebase.js';

const googleSignIn = document.getElementById('signin-google');
const errorContainer = document.getElementById('error');

/**
 * Enable the sign in with Google button
 */
export function enableSignInWithGoogle() {
  googleSignIn.addEventListener('click', async () => {
    const provider = new GoogleAuthProvider();

    try {
      await signInWithPopup(auth, provider);
      redirectToHome();
    } catch (error) {
      if (error.code === 'auth/user-cancelled') return;

      displayError(error.message);
    }
  });
}

/**
 * Redirect to the home page
 */
export function redirectToHome() {
  window.location.href = 'home.html';
}

/**
 * Display an error message to the user
 *
 * @param {string} message the message to display
 */
export function displayError(message) {
  if (errorContainer) {
    errorContainer.querySelector('span').textContent = message;
    errorContainer.classList.remove('hidden');
  } else {
    console.error('Error container element not found');
  }
}
