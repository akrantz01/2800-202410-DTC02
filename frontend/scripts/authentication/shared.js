import {
  GoogleAuthProvider,
  signInWithPopup,
} from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js';

import { auth } from '../firebase.js';

const googleButton = document.getElementById('signin-google');
const errorContainer = document.getElementById('error');

/**
 * Enable the sign in with Google button
 */
export function enableSignInWithGoogle() {
  googleButton.addEventListener('click', async () => {
    const provider = new GoogleAuthProvider();
    try {
      const result = await signInWithPopup(auth, provider);
      const user = result.user;

      // Store user info temporarily
      sessionStorage.setItem(
        'googleUser',
        JSON.stringify({
          uid: user.uid,
          displayName: user.displayName,
          email: user.email,
        }),
      );

      // Redirect to the date of birth input page
      window.location.href = 'dob.html';
    } catch (error) {
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
 * Redirect to the home page
 */
export function redirectToIndex() {
  window.location.href = 'index.html';
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
