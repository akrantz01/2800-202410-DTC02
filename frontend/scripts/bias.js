import { doc, getDoc } from 'firebase/firestore';

import { firestore } from './firebase.js';

let bias;

function getChartOptions(biasScores) {
  return {
    series: [
      parseFloat(biasScores.language),
      parseFloat(biasScores.gender),
      parseFloat(biasScores.opinion),
    ],
    colors: ['#1C64F2', '#16BDCA', '#9061F9'],
    chart: {
      height: 420,
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

async function getBias(articleID) {
  const biasDocument = doc(firestore, 'articles', articleID);
  const biasSnapshot = await getDoc(biasDocument);
  bias = biasSnapshot.data().bias;
}

function writeSentences() {
  Object.keys(bias.keywords).forEach((keyword) => {
    let currentWord = bias.keywords[keyword];
    const biasTemplate = document.getElementById('bias-card');
    const newBias = biasTemplate.content.cloneNode(true);
    newBias.querySelector('.keyword').innerHTML = keyword;
    if (currentWord.sentences.length !== 0) {
      currentWord.sentences.forEach((sentence) => {
        const sentenceTemplate = document.getElementById('sentence-template');
        const newSentence = sentenceTemplate.content.cloneNode(true);
        newSentence.querySelector('.quote').innerHTML =
          `<span class="text-2xl">"</span>${sentence.text}<span class="text-2xl">"</span>`;
        newSentence.querySelector('.response').innerHTML = veritasResponse(keyword, currentWord);
        newBias.appendChild(newSentence);
      });
      document.getElementById('bias-cards').appendChild(newBias);
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
  keywordObject.sentences.forEach((sentence) => {});
  return veritas;
}

function populateBiasScores() {
  const overallBias = parseFloat(bias.biasScore.toFixed(2));
  const pronounBias = parseFloat(bias.pronounScore.toFixed(2));
  const maleCount = bias.pronounCount.he;
  const femaleCount = bias.pronounCount.she;
  const keywordDirectionScore = parseFloat(bias.keywordScore.direction_bias.toFixed(2));
  const keywordOverallScore = parseFloat(bias.keywordScore.score.toFixed(2));
  const adjectiveOverallScore = parseFloat(bias.adjectiveScore.toFixed(2));
  const biasTotal = pronounBias + keywordOverallScore + adjectiveOverallScore;
  let keywordBiasPercent = (keywordOverallScore / biasTotal) * 100;
  keywordBiasPercent.toFixed(2);
  let pronounBiasPercent = (pronounBias / biasTotal) * 100;
  pronounBiasPercent.toFixed(2);
  let adjectiveBiasPercent = (adjectiveOverallScore / biasTotal) * 100;
  adjectiveBiasPercent.toFixed(2);
  let biasScores = {
    language: keywordBiasPercent,
    gender: pronounBiasPercent,
    opinion: adjectiveBiasPercent,
  };

  if (document.getElementById('pie-chart') && typeof ApexCharts !== 'undefined') {
    // eslint-disable-next-line no-undef
    const chart = new ApexCharts(document.getElementById('pie-chart'), getChartOptions(biasScores));
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
  if (pronounBias === 0) {
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
  } else directionText = `${(keywordDirectionScore * 100).toFixed}% Positive`;
  document.getElementById('language-bias-direction-gauge').innerHTML = directionText;
  document.querySelector('.language-direction-gauge').style =
    `width: ${Math.abs(keywordDirectionScore) * 50}%`;
}

async function main() {
  await getBias('gL5po1BLAmwEZ9seMnay');
  populateBiasScores();
  writeSentences();
}

main();
