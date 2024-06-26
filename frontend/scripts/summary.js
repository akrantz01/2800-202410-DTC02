import ApexCharts from 'apexcharts';
import { doc, onSnapshot } from 'firebase/firestore';

import { assignArticle, updateAuthorBias, updatePublisherBias } from './assign-article.js';
import { getChartOptions } from './bias.js';
import { firestore } from './firebase.js';
import { addHistory } from './history.js';
import { createApexChart } from './tone.js';
const errorContainer = document.getElementById('error-message');

const title = document.getElementById('title');
const shareLink = document.getElementById('share-link');
const author = document.getElementById('author-name');
const publisher = document.getElementById('publisher-name');
const url = document.getElementById('url');
const summary = document.getElementById('summary');

let biasLoaded = false;
let toneLoaded = false;

const params = new URLSearchParams(window.location.search);
const uid = params.get('uid');
if (!uid) window.location.href = 'home.html';

const ref = doc(firestore, 'articles', uid);
onSnapshot(ref, async (doc) => {
  try {
    if (!doc.exists()) throw new Error('Article document does not exist');

    const articleData = doc.data();

    if (title.textContent === 'Processing...') {
      title.textContent = articleData.title;
      shareLink.classList.remove('hidden');
      createShareLink(shareLink);
      author.textContent = articleData.author;
      document.getElementById('author-card').addEventListener('click', () => {
        window.location.href = `author?name=${articleData.author}`;
      });
      publisher.textContent = articleData.publisher;
      document.getElementById('publisher-card').addEventListener('click', () => {
        window.location.href = `publisher?name=${articleData.publisher}`;
      });
      await addHistory(doc.id);
      await assignArticle(doc.id);
      if (articleData.url) url.href = articleData.url;
      else url.classList.add('hidden');
    }

    if (articleData.status.summary === 'complete') {
      summary.textContent = articleData.summary;
      summary.classList.remove('hidden');
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

    if (articleData.status.bias === 'complete' && !biasLoaded) {
      biasLoaded = true;

      // Set up bias indicator
      populateBias(articleData.bias);

      await addHistory(doc.id);
      await assignArticle(doc.id);
      await updateAuthorBias(articleData.author);
      await updatePublisherBias(articleData.publisher);

      linkCardToPage('bias-detection-card', 'bias');
      hideSpinner('bias-detection-card');
    }

    if (articleData.status.tone === 'complete' && !toneLoaded) {
      toneLoaded = true;

      linkCardToPage('tone-detection-card', 'tone.html');
      hideSpinner('tone-detection-card');
      const toneResults = document.getElementById('tone-results');
      toneResults.classList.remove('hidden');
      populateTone(articleData.tone);
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

function populateTone(tone) {
  const radar = document.getElementById('radar-chart');
  if (radar && tone) {
    const radarChart = createApexChart(
      tone.document.emotion,
      tone.entities['averaged emotions'],
      tone.keywords['averaged emotions'],
      radar,
    );
    if (radarChart) {
      radarChart.render();
    }
  }
}

/**
 * Populate the bias card with bias summary results.
 *
 * @param {Object} bias Bias from analyzed article
 */
function populateBias(bias) {
  const pieChart = document.getElementById('pie-chart');
  const biasGaugeText = document.getElementById('overall-bias-gauge');
  const overallGauge = document.querySelector('.overall-gauge');
  const opinionBiasText = document.getElementById('opinion-bias-gauge');
  const opinionGauge = document.querySelector('.opinion-gauge');
  const genderGaugeText = document.getElementById('gender-bias-gauge');
  const genderGauge = document.querySelector('.gender-gauge');
  const languageGaugeText = document.getElementById('language-bias-gauge');
  const languageGauge = document.querySelector('.language-gauge');
  const languageDirection = document.querySelector('.language-direction-gauge');
  const languageDirectionText = document.getElementById('language-bias-direction-gauge');

  const overallBias = parseFloat(bias.biasScore.toFixed(2));
  const pronounBias = parseFloat(bias.pronounScore.toFixed(2));
  const keywordDirectionScore = parseFloat(bias.keywordScore.direction_bias.toFixed(2));
  const keywordOverallScore = parseFloat(bias.keywordScore.score.toFixed(2));
  const adjectiveOverallScore = parseFloat(bias.adjectiveScore.toFixed(2));
  const biasTotal = pronounBias + keywordOverallScore + adjectiveOverallScore;

  let keywordBiasPercent = (keywordOverallScore / biasTotal) * 100;
  keywordBiasPercent = keywordBiasPercent.toFixed(2);
  let pronounBiasPercent = (pronounBias / biasTotal) * 100;
  pronounBiasPercent = pronounBiasPercent.toFixed(2);
  let adjectiveBiasPercent = (adjectiveOverallScore / biasTotal) * 100;
  adjectiveBiasPercent = adjectiveBiasPercent.toFixed(2);
  const biasScores = {
    language: keywordBiasPercent,
    gender: pronounBiasPercent,
    opinion: adjectiveBiasPercent,
  };

  if (pieChart) {
    const chart = new ApexCharts(pieChart, getChartOptions(biasScores, 240));
    chart.render();
  }

  biasGaugeText.innerHTML = `${(overallBias * 100).toFixed()}%`;
  overallGauge.style = `width: ${overallBias * 100}%`;
  opinionBiasText.innerHTML = `${(adjectiveOverallScore * 100).toFixed()}%`;
  opinionGauge.style = `width: ${adjectiveOverallScore * 100}%`;
  genderGaugeText.innerHTML = `${(pronounBias * 100).toFixed()}%`;
  genderGauge.style = `width: ${pronounBias * 100}%`;

  languageGaugeText.innerHTML = `${(keywordOverallScore * 100).toFixed()}%`;
  languageGauge.style = `width: ${keywordOverallScore * 100}%`;
  let directionText = '';
  if (keywordDirectionScore === 0) directionText = 'Neutral';
  else if (keywordDirectionScore < 0) {
    directionText = `${Math.abs(keywordDirectionScore * 100).toFixed()}% Negative`;
    languageDirection.classList.add('-translate-x-[100%]');
    languageDirection.classList.remove('bg-primary');
    languageDirection.classList.add('bg-red-500');
  } else directionText = `${(keywordDirectionScore * 100).toFixed()}% Positive`;
  languageDirectionText.innerHTML = directionText;
  languageDirection.style = `width: ${Math.abs(keywordDirectionScore) * 50}%`;
}
