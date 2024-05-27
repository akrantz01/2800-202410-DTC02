import { doc, getDoc } from 'firebase/firestore';

import { firestore } from './firebase.js';

let bias = undefined;

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

function populateBiasScores() {
  let overallBias = parseFloat(bias.biasScore.toFixed(2));
  let pronounBias = parseFloat(bias.pronounScore.toFixed(2));
  let maleCount = bias.pronounCount.he;
  let femaleCount = bias.pronounCount.she;
  let keywordDirectionScore = parseFloat(bias.keywordScore.direction_bias.toFixed(2));
  let keywordOverallScore = parseFloat(bias.keywordScore.score.toFixed(2));
  let adjectiveOverallScore = parseFloat(bias.adjectiveScore.toFixed(2));
  let biasTotal = pronounBias + keywordOverallScore + adjectiveOverallScore;
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

  console.log(overallBias);
  console.log(pronounBias);
  console.log(maleCount);
  console.log(femaleCount);
  console.log(keywordDirectionScore);
  console.log(keywordOverallScore);
  console.log(adjectiveOverallScore);
  console.log(biasTotal);
}

async function main() {
  await getBias('gL5po1BLAmwEZ9seMnay');
  populateBiasScores();
}

main();
