import {
  EmailAuthProvider,
  GoogleAuthProvider,
  deleteUser,
  reauthenticateWithCredential,
  reauthenticateWithPopup,
  sendPasswordResetEmail,
  signOut,
  updateEmail,
  updateProfile,
} from 'firebase/auth';
import { deleteDoc, doc, getDoc, updateDoc } from 'firebase/firestore';

import { redirectToHome, redirectToIndex } from './authentication/shared.js';
import { auth, firestore } from './firebase.js';
import { currentUser } from './user.js';

document.addEventListener('DOMContentLoaded', async () => {
  const user = await currentUser;
  if (!user) {
    redirectToHome();
    return;
  }

  const errorContainer = document.getElementById('error-message');
  const messageContainer = document.getElementById('message');

  const modal = document.getElementById('confirm');
  const cancel = document.getElementById('cancel');

  const deleteAccountButton = document.getElementById('delete-account-button');

  // disable the modal if clicking outside
  window.onclick = function (event) {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  };

  deleteAccountButton.addEventListener('click', () => {
    modal.style.display = 'block';
  });

  cancel.addEventListener('click', () => {
    modal.style.display = 'none';
  });
  function displayMessage(message, isError = false) {
    if (isError) {
      errorContainer.querySelector('span').textContent = message;
      errorContainer.classList.remove('hidden');
    } else {
      messageContainer.querySelector('span').textContent = message;
      messageContainer.classList.remove('hidden');
    }
  }

  try {
    const userDoc = await getDoc(doc(firestore, 'users', user.uid));
    if (!userDoc.exists()) {
      throw new Error('User document does not exist');
    }

    const userData = userDoc.data();
    const dob = new Date(userData.dob);
    const today = new Date();

    const normalizedDob = new Date(dob.getFullYear(), dob.getMonth(), dob.getDate() + 1);
    const normalizedToday = new Date(today.getFullYear(), today.getMonth(), today.getDate());

    const isBirthday =
      normalizedToday.getMonth() === normalizedDob.getMonth() &&
      normalizedToday.getDate() === normalizedDob.getDate();

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
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2">Date of Birth:</label>
        <p class="text-lg">${userData.dob}${isBirthday ? '<p>Happy Birthday! 🎉 </p>' : ''}</p>
      </div>
    `;

    // Check if the user logged in with email and password
    if (user.providerData[0].providerId === 'password') {
      document.getElementById('change-name-button').classList.remove('hidden');
      document.getElementById('change-email-button').classList.remove('hidden');
      document.getElementById('reset-password-button').classList.remove('hidden');

      document.getElementById('change-name-button').addEventListener('click', () => {
        document.getElementById('update-name-form').classList.toggle('hidden');
      });

      document.getElementById('update-name-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const newName = document.getElementById('new-name').value;
        try {
          await updateProfile(user, { displayName: newName });
          await updateDoc(doc(firestore, 'users', user.uid), { name: newName });
          displayMessage('Name updated successfully');
          window.location.reload();
        } catch (error) {
          displayMessage(error.message, true);
        }
      });

      document.getElementById('change-email-button').addEventListener('click', () => {
        document.getElementById('update-email-form').classList.toggle('hidden');
      });

      document.getElementById('update-email-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const newEmail = document.getElementById('new-email').value;
        const password = document.getElementById('password').value;
        try {
          const credential = EmailAuthProvider.credential(user.email, password);
          await reauthenticateWithCredential(user, credential);
          await updateEmail(user, newEmail);
          await updateDoc(doc(firestore, 'users', user.uid), { email: newEmail });
          displayMessage('Email updated successfully. Please verify your new email.');
          window.location.reload();
        } catch (error) {
          displayMessage(error.message, true);
        }
      });

      document.getElementById('reset-password-button').addEventListener('click', async () => {
        try {
          await sendPasswordResetEmail(auth, user.email);
          displayMessage('Password reset email sent. Check your inbox.');
        } catch (error) {
          displayMessage(error.message, true);
        }
      });
    }
  } catch (error) {
    displayMessage(error.message, true);
  }

  const logoutButton = document.getElementById('logout-button');
  logoutButton.addEventListener('click', async () => {
    await signOut(auth);
    redirectToIndex();
  });
  const confirmDelete = document.getElementById('delete');
  confirmDelete.addEventListener('click', async () => {
    try {
      if (user.providerData[0].providerId === 'google.com') {
        const provider = new GoogleAuthProvider();
        await reauthenticateWithPopup(user, provider);
      }
      await deleteDoc(doc(firestore, 'users', user.uid));
      await deleteUser(auth.currentUser);
      redirectToIndex();
    } catch (error) {
      displayMessage(error.message, true);
    }
  });
});
