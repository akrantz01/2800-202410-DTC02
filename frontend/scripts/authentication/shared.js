import { GoogleAuthProvider, signInWithPopup } from 'firebase/auth';

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
      const { user } = await signInWithPopup(auth, provider);

      const createdAt = getUserCreationTime(user.metadata);
      if (createdAt > Date.now() - 10000) {
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
      } else redirectToHome();
    } catch (error) {
      displayError(error.message);
    }
  });
}

/**
 * Get the timestamp of when the user was created
 *
 * @param {import('firebase/auth').UserMetadata} metadata the user metadata
 * @returns {number} a unix timestamp with milliseconds
 */
function getUserCreationTime(metadata) {
  if ('createdAt' in metadata) return parseInt(metadata.createdAt, 10);
  else return new Date(metadata.creationTime).getTime();
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
