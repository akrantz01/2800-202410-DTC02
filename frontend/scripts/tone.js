import ApexCharts from 'apexcharts';
import { collection, getDocs } from 'firebase/firestore';

import { firestore } from './firebase.js';
async function fetchArticles() {
  // Get the 'articles' collection from Firestore
  const articlesCollection = collection(firestore, 'articles');

  // Fetch all documents from the 'articles' collection
  const articlesSnapshot = await getDocs(articlesCollection);

  // Map the documents to an array of data
  const articlesList = articlesSnapshot.docs.map((doc) => doc.data());

  // Grab the newest article only
  const articlesListSorted = articlesList.sort((a, b) => b.timestamp - a.timestamp);
  const newestArticle = articlesListSorted[0];

  // Grab the document emotion field
  const docEmotion = newestArticle.tone.document.emotion;

  // Populate options in radar chart
  const options = {
    // radar chart
    series: [
      {
        name: 'Series 1',
        data: [
          docEmotion.joy,
          docEmotion.anger,
          docEmotion.disgust,
          docEmotion.sadness,
          docEmotion.fear,
        ],
      },
    ],
    chart: {
      toolbar: {
        show: false, // Hides hamburger menu
      },
      height: 350,
      type: 'radar',
    },
    // title: {
    //   text: 'Basic Radar Chart',
    // },
    yaxis: {
      stepSize: 0.05,
    },
    xaxis: {
      categories: ['Joy', 'Anger', 'Disgust', 'Sadness', 'Fear'],
    },
  };
  const chart = new ApexCharts(document.querySelector('#chart'), options);

  chart.render();
}

// Fetch and display articles on page load
fetchArticles();
