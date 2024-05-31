import ApexCharts from 'apexcharts';
import { doc, onSnapshot } from 'firebase/firestore';
import 'flowbite';

import { firestore } from './firebase.js';

function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

/**
 * Display apex chart with bias scores
 *
 * @param {Object} biasScores Scores of individual biases
 * @param {Integer} chartHeight    Height of element
 * @returns                   Apex chart
 */
export function getChartOptions(biasScores, chartHeight) {
  return {
    series: [
      parseFloat(biasScores.language),
      parseFloat(biasScores.gender),
      parseFloat(biasScores.opinion),
    ],
    colors: ['#1C64F2', '#16BDCA', '#9061F9'],
    chart: {
      height: chartHeight,
      width: '100%',
      type: 'pie',
    },
    stroke: {
      colors: ['white'],
      lineCap: '',
    },
    plotOptions: {
      pie: {
        labels: {
          show: true,
        },
        size: '100%',
        dataLabels: {
          offset: -25,
        },
      },
    },
    labels: ['Language Bias', 'Gender Bias', 'Opinion Bias'],
    dataLabels: {
      enabled: true,
      style: {
        fontFamily: 'Inter, sans-serif',
      },
    },
    legend: {
      position: 'bottom',
      fontFamily: 'Inter, sans-serif',
    },
    yaxis: {
      labels: {
        formatter: function (value) {
          return value + '%';
        },
      },
    },
    xaxis: {
      labels: {
        formatter: function (value) {
          return value + '%';
        },
      },
      axisTicks: {
        show: false,
      },
      axisBorder: {
        show: false,
      },
    },
  };
}

function writeSentences(bias) {
  const biasCards = document.getElementById('bias-cards');
  biasCards.innerHTML = '';

  Object.keys(bias.keywords)
    .toSorted()
    .forEach((keyword) => {
      const currentWord = bias.keywords[keyword];
      const biasTemplate = document.getElementById('bias-card');
      const newBias = biasTemplate.content.cloneNode(true);
      const logo = document.getElementById('logo-display');
      newBias.querySelector('img').src = logo.src;
      newBias.querySelector('.keyword').innerHTML = keyword;
      if (currentWord.sentences.length !== 0) {
        currentWord.sentences.forEach(() => {
          newBias.querySelector('.response').innerHTML = veritasResponse(keyword, currentWord);
        });
        biasCards.appendChild(newBias);
      }
    });
}

function veritasResponse(keyword, keywordObject) {
  let veritas = `
  The language in the sentence has a ${keywordObject.sentiment.label} outlook on the entity "${keyword}"
  <div class="flex items-center gap-4">
  <div class="bg-gray-200 rounded-full h-2.5 flex  w-[150px]">
    <div
      class="language-gauge bg-${keywordObject.sentiment.label === 'negative' ? 'red-500' : 'primary'} h-2.5 rounded-full"
      style="width: ${Math.abs(keywordObject.sentiment.score) * 100}%"
      name="language-bias-gauge"
    ></div>
          
  </div>
  <p class="text-l">${(keywordObject.sentiment.score * 100).toFixed()}%</p>
  </div>`;

  veritas += '<p><span class="text-2xl">"</span>';
  keywordObject.sentences
    .filter((sentence) => sentence.scores !== undefined)
    .forEach((sentence) => {
      const coloredSentence = writeSegments(keyword, sentence);
      const order = Object.keys(coloredSentence);
      order.sort((a, b) => {
        return a - b;
      });
      order.forEach((position) => {
        veritas += coloredSentence[position];
      });
    });
  veritas += '<span class="text-2xl">"</span></p>';

  return veritas;
}

function writeSegments(keyword, sentence) {
  const mainText = sentence.text;
  const segments = Object.keys(sentence.scores);
  const keywordIndex = mainText.indexOf(keyword);
  const keywordLastIndex = keywordIndex + keyword.length;
  const segmentOrder = {};
  segments.forEach((segment) => {
    const index = mainText.indexOf(segment);
    let color = '';
    if (sentence.scores[segment].sentiment.label === 'positive') color = 'text-primary';
    else if (sentence.scores[segment].sentiment.label === 'negative') color = 'text-red-500';

    if (
      (index >= keywordIndex && index <= keywordLastIndex) ||
      (index + segment.length >= keywordIndex && index + segment.length <= keywordLastIndex) ||
      (index <= keywordIndex && index + segment.length >= keywordLastIndex)
    ) {
      const segmentTokens = segment.split(' ');
      const keywordTokens = keyword.split(' ');
      let segmentText = '';
      segmentTokens.forEach((token) => {
        if (keywordTokens.includes(token.replace(/[!,.?:;()]/g, '')))
          segmentText += `<span class="font-extrabold">${token}</span> `;
        else segmentText += `<span class="${color}">${token}</span> `;
      });
      segmentOrder[index] = segmentText;
    } else segmentOrder[index] = `<span class="${color}">${segment}</span> `;
  });
  return segmentOrder;
}

function populateBiasScores(bias) {
  const overallBias = parseFloat(bias.biasScore.toFixed(2));
  const pronounBias = parseFloat(bias.pronounScore.toFixed(2));
  const maleCount = bias.pronounCount.he;
  const femaleCount = bias.pronounCount.she;
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

  if (document.getElementById('pie-chart')) {
    const chart = new ApexCharts(
      document.getElementById('pie-chart'),
      getChartOptions(biasScores, 420),
    );
    chart.render();
  }
  document.getElementById('overall-bias-gauge').innerHTML = `${(overallBias * 100).toFixed()}%`;
  document.querySelector('.overall-gauge').style = `width: ${overallBias * 100}%`;
  document.getElementById('opinion-bias-gauge').innerHTML =
    `${(adjectiveOverallScore * 100).toFixed()}%`;
  document.querySelector('.opinion-gauge').style = `width: ${adjectiveOverallScore * 100}%`;
  document.getElementById('gender-bias-gauge').innerHTML = `${(pronounBias * 100).toFixed()}%`;
  document.querySelector('.gender-gauge').style = `width: ${pronounBias * 100}%`;
  let genderBreakdown = document.getElementById('gender-breakdown');
  if (pronounBias === 0 && genderBreakdown === document.getElementById('gender-breakdown')) {
    genderBreakdown.innerHTML = 'No pronouns were detected in the text.';
  } else if (maleCount === femaleCount) {
    genderBreakdown = 'The article uses an equal number of "he/him" and "she/her" pronouns.';
  } else if (maleCount > femaleCount) {
    genderBreakdown.innerHTML = `The article is biased towards "he/him" pronouns, with "he/him" appearing ${maleCount} times and "she/her" appearing ${femaleCount} times.`;
  } else {
    genderBreakdown.innerHTML = `The article is biased towards "she/her" pronouns, with "she/her" appearing ${femaleCount} times and "he/him" appearing ${maleCount} times.`;
  }
  document.getElementById('language-bias-gauge').innerHTML =
    `${(keywordOverallScore * 100).toFixed()}%`;
  document.querySelector('.language-gauge').style = `width: ${keywordOverallScore * 100}%`;
  let directionText = '';
  if (keywordDirectionScore === 0) directionText = 'Neutral';
  else if (keywordDirectionScore < 0) {
    directionText = `${Math.abs(keywordDirectionScore * 100).toFixed()}% Negative`;
    document.querySelector('.language-direction-gauge').classList.add('-translate-x-[100%]');
    document.querySelector('.language-direction-gauge').classList.remove('bg-primary');
    document.querySelector('.language-direction-gauge').classList.add('bg-red-500');
  } else directionText = `${(keywordDirectionScore * 100).toFixed()}% Positive`;
  document.getElementById('language-bias-direction-gauge').innerHTML = directionText;
  document.querySelector('.language-direction-gauge').style =
    `width: ${Math.abs(keywordDirectionScore) * 50}%`;
}
function main() {
  const articleID = getQueryParam('uid');
  const ref = doc(firestore, 'articles', articleID);

  let scoresRendered = false;
  onSnapshot(ref, (doc) => {
    const data = doc.data();

    if (data === undefined || data.bias === undefined) return;

    if (!scoresRendered) {
      populateBiasScores(data.bias);
      scoresRendered = true;
    }

    writeSentences(data.bias);
  });
}

if (window.location.href.match('bias') != null) main();
