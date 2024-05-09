import { signInWithEmailAndPassword } from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js';

import { displayError, enableSignInWithGoogle, redirectToHome } from './shared.js';
import { auth } from '../firebase.js';
import { currentUser } from '../user.js';

const form = document.querySelector('form');
enableSignInWithGoogle();

if ((await currentUser) !== null) redirectToHome();

// Handle email & password sign in
form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const data = Object.fromEntries(new FormData(form));

  try {
    await signInWithEmailAndPassword(auth, data.email, data.password);
    redirectToHome();
  } catch (error) {
    let message = error.message;
    if (error.code === 'auth/invalid-credential') message = 'Invalid email or password.';

    displayError(message);
  }
});
