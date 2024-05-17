import { doc, getDoc } from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js';

import { firestore } from './firebase.js';

// Function to get URL parameters
function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

document.addEventListener('DOMContentLoaded', async () => {
  const uid = getQueryParam('uid');
  const errorContainer = document.getElementById('error-message');

  function displayError(message) {
    errorContainer.querySelector('span').textContent = message;
    errorContainer.classList.remove('hidden');
  }

  if (!uid) {
    displayError('Article UID not provided.');
    return;
  }

  try {
    const articleDoc = await getDoc(doc(firestore, 'articles', uid));
    if (!articleDoc.exists()) {
      throw new Error('Article document does not exist');
    }

    const articleData = articleDoc.data();
    const articleInfoContainer = document.getElementById('article-info');
    articleInfoContainer.innerHTML = `
      <h2 class="text-2xl font-bold">${articleData.title}</h2>
      <p class="text-gray-700">${articleData.publisher}</p>
      <a href="${articleData.originalUrl}" target="_blank" class="text-blue-500 hover:underline">Original article</a>
      <p class="mt-4">${articleData.summary}</p>
    `;

    // Set up links with the UID query parameter
    document.getElementById('ai-detect-link').href = `ai-detect.html?uid=${uid}`;
    document.getElementById('analysis-link').href = `analysis.html?uid=${uid}`;
    document.getElementById('bias-link').href = `bias.html?uid=${uid}`;
  } catch (error) {
    displayError(error.message);
  }
});
