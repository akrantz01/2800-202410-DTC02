import { doc, onSnapshot } from 'firebase/firestore';

import { firestore } from './firebase.js';

const errorContainer = document.getElementById('error-message');

const title = document.getElementById('title');
const articleInfo = document.getElementById('article-info');
const shareLink = document.getElementById('share-link');
const author = document.getElementById('author-name');
const publisher = document.getElementById('publisher-name');
const url = document.getElementById('url');
const summary = document.getElementById('summary');

const params = new URLSearchParams(window.location.search);
const uid = params.get('uid');
if (!uid) window.location.href = 'home.html';

const ref = doc(firestore, 'articles', uid);
onSnapshot(ref, async (doc) => {
  try {
    if (!doc.exists()) throw new Error('Article document does not exist');

    const articleData = doc.data();

    if (articleData.status.extract === 'complete') {
      title.textContent = articleData.title;

      articleInfo.classList.remove('hidden');
      shareLink.classList.remove('hidden');
      createShareLink(shareLink);
      author.textContent = articleData.author;
      author.addEventListener('click', () => {
        window.location.href = `author?name=${articleData.author}`;
      });
      publisher.textContent = articleData.publisher;
      publisher.addEventListener('click', () => {
        window.location.href = `publisher?name=${articleData.publisher}`;
      });
      url.href = articleData.url;
      summary.textContent = articleData.summary;
    }

    if (articleData.status.ai === 'complete') {
      const aiDetectionProgress = document.getElementById('ai-detection-progress');
      const aiDetectionText = document.getElementById('ai-detection-text');
      aiDetectionProgress.style.width = `${articleData.aiDetection}%`;
      aiDetectionText.textContent = `${articleData.aiDetection}%`;

      linkCardToPage('ai-detection-card', 'ai-detect.html');
      hideSpinner('ai-detection-card');
    }

    if (articleData.status.accuracy === 'complete') {
      const analysisProgress = document.getElementById('analysis-progress');
      const analysisText = document.getElementById('analysis-text');
      analysisProgress.style.width = `${articleData.analysis}%`;
      // analysisProgress.textContent = `${articleData.analysis}%`;
      analysisText.textContent = `${articleData.analysis}% factual`;

      linkCardToPage('factual-analysis-card', 'analysis.html');
      hideSpinner('factual-analysis-card');
    }

    if (articleData.status.bias === 'complete') {
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

      linkCardToPage('bias-detection-card', 'bias.html');
      hideSpinner('bias-detection-card');
    }

    if (articleData.status.tone === 'complete') {
      const toneDetectionProgress = document.getElementById('tone-detection-progress');
      const toneDetectionText = document.getElementById('tone-detection-text');
      toneDetectionProgress.style.width = `${articleData.toneDetection}%`;
      toneDetectionText.textContent = `${articleData.toneDetection}%`;

      linkCardToPage('tone-detection-card', 'tone.html');
      hideSpinner('tone-detection-card');
    }
  } catch (error) {
    displayError(error.message);
  }
});

/**
 * Link a card to a page.
 *
 * @param {string} cardId the id of the card to add the event listener to
 * @param {string} page the page to navigate to when the card is clicked
 */
function linkCardToPage(cardId, page) {
  document.getElementById(cardId).addEventListener('click', () => {
    window.location.href = `${page}?uid=${uid}`;
  });
}

function hideSpinner(cardId) {
  const card = document.getElementById(cardId);
  card.querySelector('.spinner').style.display = 'none';
  card.querySelectorAll('.result').forEach((result) => {
    result.classList.remove('hidden');
  });
}

/**
 * Display an error message on the page.
 *
 * @param {string} message the error message to display
 */
function displayError(message) {
  errorContainer.querySelector('span').textContent = message;
  errorContainer.classList.remove('hidden');
}

/**
 * Copy the link to the page to the clipboard
 *
 */
function createShareLink(element) {
  element.addEventListener('click', () => {
    const currentURL = window.location;
    navigator.clipboard.writeText(currentURL);
    alert('URL has been copied to the clipboard!');
  });
}
