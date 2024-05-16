import {
  EmailAuthProvider,
  deleteUser,
  reauthenticateWithCredential,
  signOut,
  updateEmail,
  updateProfile,
} from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js';
import {
  deleteDoc,
  doc,
  getDoc,
  updateDoc,
} from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js';

import { displayError, redirectToHome } from './authentication/shared.js';
import { auth, firestore } from './firebase.js';
import { currentUser } from './user.js';

document.addEventListener('DOMContentLoaded', async () => {
  const user = await currentUser;
  if (!user) {
    redirectToHome();
    return;
  }

  try {
    const userDoc = await getDoc(doc(firestore, 'users', user.uid));
    if (!userDoc.exists()) {
      throw new Error('User document does not exist');
    }

    const userData = userDoc.data();
    const profileContainer = document.getElementById('profile-info');
    profileContainer.innerHTML = `
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2">Name:</label>
        <p class="text-lg">${userData.name}</p>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2">Email:</label>
        <p class="text-lg">${userData.email}</p>
      </div>
    `;

    // Check if the user logged in with email and password
    if (user.providerData[0].providerId === 'password') {
      document.getElementById('update-name-form').classList.remove('hidden');
      document.getElementById('update-email-form').classList.remove('hidden');

      document.getElementById('update-name-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const newName = document.getElementById('new-name').value;
        try {
          await updateProfile(user, { displayName: newName });
          await updateDoc(doc(firestore, 'users', user.uid), { name: newName });
          alert('Name updated successfully');
          window.location.reload();
        } catch (error) {
          displayError(error.message);
        }
      });

      document.getElementById('update-email-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const newEmail = document.getElementById('new-email').value;
        const password = prompt('Please enter your password to confirm the change:');
        if (!password) {
          alert('Password is required to change email');
          return;
        }
        try {
          const credential = EmailAuthProvider.credential(user.email, password);
          await reauthenticateWithCredential(user, credential);
          await updateEmail(user, newEmail);
          await updateDoc(doc(firestore, 'users', user.uid), { email: newEmail });
          alert('Email updated successfully');
          window.location.reload();
        } catch (error) {
          displayError(error.message);
        }
      });
    }
  } catch (error) {
    displayError(error.message);
  }

  const logoutButton = document.getElementById('logout-button');
  logoutButton.addEventListener('click', async () => {
    await signOut(auth);
    redirectToHome();
  });

  const deleteAccountButton = document.getElementById('delete-account-button');
  deleteAccountButton.addEventListener('click', async () => {
    try {
      await deleteDoc(doc(firestore, 'users', user.uid));
      await deleteUser(auth.currentUser);
      redirectToHome();
    } catch (error) {
      displayError(error.message);
    }
  });
});
