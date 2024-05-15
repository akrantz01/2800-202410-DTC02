import { auth } from '../firebase.js';

async function logout() {
  auth
    .signOut()
    .then(async () => {
      // Sign-out successful.
    })
    .catch((error) => {
      // An error happened.
      console.log(error);
    });
}
logout();
