import { doc, onSnapshot } from 'firebase/firestore';

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
      newBias.querySelector('img').src =
        `data:image/svg+xml,%3c?xml%20version='1.0'%20encoding='UTF-8'%20standalone='no'?%3e%3csvg%20version='1.1'%20id='Layer_1'%20x='0'%20y='0'%20viewBox='0%200%2083.849548%2041.518794'%20xml:space='preserve'%20width='83.849548'%20height='41.518791'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:svg='http://www.w3.org/2000/svg'%3e%3cdefs%20id='defs16'%20/%3e%3cstyle%20id='style1'%3e%20.st0{fill:%23fff}%20%3c/style%3e%3clinearGradient%20id='SVGID_1_'%20gradientUnits='userSpaceOnUse'%20x1='-0.212'%20y1='282.879'%20x2='101.724'%20y2='341.73199'%20gradientTransform='matrix(1,0,0,-1,0,371.896)'%3e%3cstop%20offset='0'%20stop-color='%2310e7ff'%20id='stop1'%20/%3e%3cstop%20offset='.103'%20stop-color='%2333d5ff'%20id='stop2'%20/%3e%3cstop%20offset='.255'%20stop-color='%2360bdff'%20id='stop3'%20/%3e%3cstop%20offset='.408'%20stop-color='%2386aaff'%20id='stop4'%20/%3e%3cstop%20offset='.56'%20stop-color='%23a39aff'%20id='stop5'%20/%3e%3cstop%20offset='.71'%20stop-color='%23b790ff'%20id='stop6'%20/%3e%3cstop%20offset='.858'%20stop-color='%23c489ff'%20id='stop7'%20/%3e%3cstop%20offset='1'%20stop-color='%23c887ff'%20id='stop8'%20/%3e%3c/linearGradient%3e%3clinearGradient%20id='SVGID_2_'%20gradientUnits='userSpaceOnUse'%20x1='31.374001'%20y1='303.384'%20x2='81.931999'%20y2='332.57401'%20gradientTransform='matrix(1,0,0,-1,130.5037,372.23674)'%3e%3cstop%20offset='0'%20stop-color='%2310e7ff'%20id='stop9'%20/%3e%3cstop%20offset='.103'%20stop-color='%2333d5ff'%20id='stop10'%20/%3e%3cstop%20offset='.255'%20stop-color='%2360bdff'%20id='stop11'%20/%3e%3cstop%20offset='.408'%20stop-color='%2386aaff'%20id='stop12'%20/%3e%3cstop%20offset='.56'%20stop-color='%23a39aff'%20id='stop13'%20/%3e%3cstop%20offset='.71'%20stop-color='%23b790ff'%20id='stop14'%20/%3e%3cstop%20offset='.858'%20stop-color='%23c489ff'%20id='stop15'%20/%3e%3cstop%20offset='1'%20stop-color='%23c887ff'%20id='stop16'%20/%3e%3c/linearGradient%3e%3cpath%20id='path26'%20style='fill:%2300aef4;fill-opacity:1;stroke-width:1.00061'%20d='M%2083.849547,41.516948%2059.871883,0.01879296%2047.134615,0%2070.667181,41.518793%20Z'%20/%3e%3cpath%20id='path22'%20style='fill:%2300cbf4;fill-opacity:1;stroke-width:1.00061'%20d='m%2035.182393,41.518793%2017.719923,-31.3%20L%2047.150086,0.01879296%2023.56831,41.518793%20Z%20m%2035.543097,0%20L%2047.143714,0.01879296%2041.400417,10.218793%20l%2017.71099,31.3%20z%20m%200,0%20L%2047.151526,0.01879296%2041.41148,10.218793%20l%2017.699927,31.3%20z%20m%20-35.543097,0%2017.70428,-31.3%20L%2047.150086,0.01879296%2023.56831,41.518793%20Z'%20/%3e%3cpath%20id='path16-9-1'%20style='fill:%2317da7c;fill-opacity:1;stroke-width:1.00061'%20d='M%2035.543096,0.01879296%2017.854461,31.318793%20l%205.728755,10.2%2023.573963,-41.50000004%20z%20m%20-35.543096,0%2023.581775,41.50000004%205.744408,-10.2%20-17.7121,-31.30000004%20z%20m%200,0%2023.581775,41.50000004%205.736587,-10.2%20L%2011.614083,0.01879296%20Z%20m%2035.543096,0%20-17.688635,31.30000004%205.728755,10.2%2023.573963,-41.50000004%20z'%20/%3e%3c/svg%3e`;
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

  if (document.getElementById('pie-chart') && typeof ApexCharts !== 'undefined') {
    // eslint-disable-next-line no-undef
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
