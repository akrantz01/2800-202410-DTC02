import { EmailAuthProvider, reauthenticateWithCredential, updatePassword } from 'firebase/auth';

import { displayError } from './shared.js';
import { currentUser } from '../user.js';

document.getElementById('reset-password-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(event.target));

  try {
    const user = await currentUser;
    if (!user) throw new Error('User not logged in');

    const credential = EmailAuthProvider.credential(user.email, data.oldPassword);
    await reauthenticateWithCredential(user, credential);
    await updatePassword(user, data.newPassword);

    alert('Password updated successfully');
  } catch (error) {
    displayError(error.message);
  }
});
