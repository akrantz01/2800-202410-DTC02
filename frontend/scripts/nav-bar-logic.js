import { auth } from './firebase.js';

async function loadSkeleton() {
  const headerRequest = new XMLHttpRequest();
  const footerRequest = new XMLHttpRequest();

  await headerRequest.open('get', '/templates/header-template.html', true);
  headerRequest.onreadystatechange = () => {
    if (headerRequest.readyState === 4 && headerRequest.status === 200) {
      document.getElementById('header-placeholder').innerHTML = headerRequest.responseText;
    }
  };
  headerRequest.send();

  auth.onAuthStateChanged(async function (user) {
    if (user) {
      await footerRequest.open('get', '/templates/footer-logged-in-template.html', true);
    } else {
      // No user is signed in.
      await footerRequest.open('get', '/templates/footer-logged-out-template.html', true);
    }
    footerRequest.onreadystatechange = () => {
      if (footerRequest.readyState === 4 && footerRequest.status === 200) {
        document.getElementById('footer-placeholder').innerHTML = footerRequest.responseText.slice(
          6,
          -9,
        );
      }
    };
    footerRequest.send();
  });
}
loadSkeleton(); // invoke the function
