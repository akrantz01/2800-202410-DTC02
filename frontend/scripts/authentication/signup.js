import {
  GoogleAuthProvider,
  createUserWithEmailAndPassword,
  signInWithPopup,
  updateProfile,
} from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js';
import { doc, setDoc } from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js';

import { displayError, enableSignInWithGoogle, redirectToHome } from './shared.js';
import { auth, firestore } from '../firebase.js';
import { currentUser } from '../user.js';

const form = document.querySelector('form');
enableSignInWithGoogle();

if ((await currentUser) !== null) redirectToHome();

// Handle email & password sign in
form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const data = Object.fromEntries(new FormData(form));
  const dob = new Date(data.dob);
  const age = new Date().getFullYear() - dob.getFullYear();

  if (age < 14) {
    displayError('You must be at least 14 years old to sign up.');
    return;
  }

  try {
    const credential = await createUserWithEmailAndPassword(auth, data.email, data.password);
    await updateProfile(credential.user, { displayName: data.name });
    await setDoc(doc(firestore, 'users', credential.user.uid), {
      name: credential.user.displayName,
      email: credential.user.email,
      dob: data.dob,
    });

    redirectToHome();
  } catch (error) {
    let message = error.message;
    if (error.code === 'auth/email-already-in-use') message = 'Email already in use.';
    else if (error.code === 'auth/weak-password') message = 'Password is too weak.';

    displayError(message);
  }
});

// Handle Google sign in
const googleButton = document.getElementById('signin-google');
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
