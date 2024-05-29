import { signInWithEmailAndPassword } from 'firebase/auth';

import { displayError, enableSignInWithGoogle, redirectToHome } from './shared.js';
import { auth } from '../firebase.js';
import { currentUser } from '../user.js';

const form = document.querySelector('form');
enableSignInWithGoogle();

const user = await currentUser;
if (user !== null && user.emailVerified) redirectToHome();

// Handle email & password sign in
form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const data = Object.fromEntries(new FormData(form));

  try {
    await signInWithEmailAndPassword(auth, data.email, data.password);
    if (!user.emailVerified) throw new Error('Email has not been verified');
    redirectToHome();
  } catch (error) {
    let message = error.message;
    if (error.code === 'auth/invalid-credential') message = 'Invalid email or password.';

    displayError(message);
  }
});
