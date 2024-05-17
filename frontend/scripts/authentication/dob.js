import { deleteUser } from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js';
import { doc, setDoc } from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js';

import { displayError, redirectToHome } from './shared.js';
import { auth, firestore } from '../firebase.js';

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('dob-form');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const data = new FormData(form);
    const dob = new Date(data.get('dob'));
    const age = new Date().getFullYear() - dob.getFullYear();

    if (age < 14) {
      displayError('You must be at least 14 years old to sign up.');
      // const user = JSON.parse(sessionStorage.getItem('googleUser'));
      const userAuth = auth.currentUser;
      if (userAuth) {
        await deleteUser(userAuth);
      }
      return;
    }

    try {
      const user = JSON.parse(sessionStorage.getItem('googleUser'));

      await setDoc(doc(firestore, 'users', user.uid), {
        name: user.displayName,
        email: user.email,
        dob: data.get('dob'),
      });

      sessionStorage.removeItem('googleUser');
      redirectToHome();
    } catch (error) {
      displayError(error.message);
    }
  });
});
