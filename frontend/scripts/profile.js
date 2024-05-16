import { deleteUser, signOut } from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js';
import {
  deleteDoc,
  doc,
  getDoc,
} from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js';

import { displayError, redirectToHome } from './authentication/shared.js';
import { auth, firestore } from './firebase.js';
import { currentUser } from './user.js';

document.addEventListener('DOMContentLoaded', async () => {
  const user = await currentUser;
  if (!user) {
    console.log('No user is currently signed in.');
    redirectToHome();
    return;
  }

  try {
    console.log('Fetching user document for UID:', user.uid);
    const userDoc = await getDoc(doc(firestore, 'users', user.uid));
    if (!userDoc.exists()) {
      throw new Error('User document does not exist');
    }

    const userData = userDoc.data();
    console.log('User data retrieved:', userData);
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
  } catch (error) {
    console.error('Error fetching user document:', error);
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
      console.error('Error deleting user account:', error);
      displayError(error.message);
    }
  });
});
