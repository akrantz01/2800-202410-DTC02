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

    // Set up progress bars
    const aiDetectionProgress = document.getElementById('ai-detection-progress');
    const aiDetectionText = document.getElementById('ai-detection-text');
    aiDetectionProgress.style.width = `${articleData.aiDetection}%`;
    // aiDetectionProgress.textContent = `${articleData.aiDetection}%`;
    aiDetectionText.textContent = `${articleData.aiDetection}%`;

    const analysisProgress = document.getElementById('analysis-progress');
    const analysisText = document.getElementById('analysis-text');
    analysisProgress.style.width = `${articleData.analysis}%`;
    // analysisProgress.textContent = `${articleData.analysis}%`;
    analysisText.textContent = `${articleData.analysis}% factual`;

    // Set up bias indicator
    const biasLeft = document.getElementById('bias-left');
    const biasNeutral = document.getElementById('bias-neutral');
    const biasRight = document.getElementById('bias-right');
    const biasText = document.getElementById('bias-text');

    biasLeft.classList.remove('bg-blue-500');
    biasNeutral.classList.remove('bg-green-500');
    biasRight.classList.remove('bg-red-500');

    if (articleData.bias === 'left') {
      biasLeft.classList.add('bg-blue-500', 'flex-grow');
      biasNeutral.classList.add('bg-gray-200');
      biasRight.classList.add('bg-gray-200');
      biasText.textContent = 'Bias: Left';
    } else if (articleData.bias === 'right') {
      biasLeft.classList.add('bg-gray-200');
      biasNeutral.classList.add('bg-gray-200');
      biasRight.classList.add('bg-red-500', 'flex-grow');
      biasText.textContent = 'Bias: Right';
    } else {
      biasLeft.classList.add('bg-gray-200');
      biasNeutral.classList.add('bg-green-500', 'flex-grow');
      biasRight.classList.add('bg-gray-200');
      biasText.textContent = 'Bias: Neutral';
    }

    // Add event listeners to the cards to navigate to detailed pages
    document.getElementById('ai-detection-card').addEventListener('click', () => {
      window.location.href = `ai-detect.html?uid=${uid}`;
    });
    document.getElementById('factual-analysis-card').addEventListener('click', () => {
      window.location.href = `analysis.html?uid=${uid}`;
    });
    document.getElementById('bias-detection-card').addEventListener('click', () => {
      window.location.href = `bias.html?uid=${uid}`;
    });
  } catch (error) {
    displayError(error.message);
  }
});
