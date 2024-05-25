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

  // Grab the relevant fields of the document
  const article = newestArticle.tone;
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

  // Grab title page elements
  // if (article.metadata) {
  //  const titleSection = document.getElementById('accordion-color-heading-2')
  //  titleSection.classList.remove("hidden")
  //  const titleResults = document.getElementById('title-results');
  //  const titleExplanation = document.getElementById('title-explanation');

  // }
  // Display document results
  //

  // Grab documents page elements
  const docResults = document.getElementById('document-results');
  const docExplanation = document.getElementById('document-explanation');
  docResults.innerHTML = `This article suggests an overall feeling of ${article.document.plutchik}`;
  docExplanation.innerHTML = `This conclusion was reached by the combination of the strongest emotions displayed
  collectively throughout the text.`;

  // Grab keywords page elements
  const keywordResults = document.getElementById('keyword-results');
  // const keywordExplanation = document.getElementById('keyword-explanation');

  // Loop through keywords object and print as a list
  Object.entries(article.keywords).forEach((entry) => {
    const { emotion, sentiment } = entry[1];
    console.log(Object.keys(emotion));
    keywordResults.innerHTML += `<li>"<span class="font-bold">${entry[0]}</span>" - ${Object.keys(emotion)}, sentiment: ${Object.values(sentiment)}"</li>`;
    // return count of highest emotion
  });

  // Grab entity page elements
  const entityResultsList = document.getElementById('entity-results-list');
  // const entityExplanation = document.getElementById('entity-explanation');

  // Loop through entities object and append elements to a table
  Object.entries(article.entities).forEach(
    ([
      name,
      {
        type,
        count,
        sentiment: { label: sentiment },
        plutchik,
        relevance,
      },
    ]) => {
      // create the row
      const entityRow = document.createElement('tr');
      // Round float to two decimal places
      const cellData = [
        Math.round((relevance + Number.EPSILON) * 100) / 100,
        name,
        type,
        plutchik.join(', '),
        sentiment,
        count,
      ];

      // populate the data into table cells
      cellData.forEach((data) => {
        const cell = document.createElement('td');

        // Entity type (person, organization, ...)
        if (data === type) {
          cell.className = 'px-2 py-2 text-center text-lg flex flex-col';
          cell.innerHTML = getEmoji('type', type);
          cell.innerHTML += `<span class="text-xxs">${data}</span>`;
        }
        // Sentiment (positive, negative, neutral)
        else if (data === sentiment) {
          // Colour the text
          const colour =
            sentiment === 'positive'
              ? 'green-500'
              : sentiment === 'negative'
                ? 'red-500'
                : 'gray-500';
          cell.className = 'px-2 py-2 text-center text-lg flex flex-col';
          const span = document.createElement('span');
          span.className = `text-${colour} text-xxs`;
          cell.innerHTML = getEmoji('sentiment', sentiment);
          cell.innerHTML += `<span class="text-xxs text-${colour}">${data}</span>`;
        }
        // Emotion
        else if (data === plutchik) {
          cell.className = 'px-2 py-2 text-center text-lg flex flex-col';
        } else {
          cell.className = 'px-2 py-2 text-center text-xs';
          cell.innerHTML = data;
        }
        entityRow.appendChild(cell);
      });
      entityResultsList.appendChild(entityRow);
    },
  );

  function getEmoji(category, value) {
    if (category === 'type') {
      switch (value) {
        case 'Money':
          return '💰';
        case 'Organization':
          return '🏢';
      }
    } else if (category === 'sentiment') {
      switch (value) {
        case 'positive':
          return '➕';
        case 'neutral':
          return '〰';
        case 'negative':
          return '➖';
      }
    } else if (category === 'emotion') {
      switch (value) {
        case 'pride':
          return '😤';
        case 'morbidness':
          return '😏';
        case 'joy':
          return '😊';
        case 'digust':
          return '😖';
        case 'sadness':
          return '😢';
        case 'anger':
          return '😡';
        case 'fear':
          return '😨';
      }
    }
  }
}

// Fetch and display articles on page load
fetchArticles();
