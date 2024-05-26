import ApexCharts from 'apexcharts';
import { collection, getDocs } from 'firebase/firestore';

import { firestore } from './firebase.js';
const getEmoji = function (category, value) {
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
      case 'disgust':
        return '😖';
      case 'sadness':
        return '😢';
      case 'anger':
        return '😡';
      case 'fear':
        return '😨';
    }
  }
};

async function fetchArticles() {
  // Get the 'articles' collection from Firestore
  const articlesCollection = collection(firestore, 'articles');
  // Fetch all documents from the 'articles' collection
  const articlesSnapshot = await getDocs(articlesCollection);
  let firestoreDocument;
  articlesSnapshot.forEach((doc) => {
    if (doc.id === 'qPlbTU5PQmb00egJrqMW') {
      firestoreDocument = doc.data();
    }
  });
  // Map the documents to an array of data
  // const articlesList = articlesSnapshot.docs.map((doc) => doc.data());

  // Grab the newest article only
  // const articlesListSorted = articlesList.sort((a, b) => b.timestamp - a.timestamp);
  // const newestArticle = articlesListSorted[0];

  // Grab the relevant fields of the document
  const article = firestoreDocument.tone;
  const docEmotion = firestoreDocument.tone.document.emotion;
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
  // Check for two emojis and add them both if necessary
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

  // const keywordExplanation = document.getElementById('keyword-explanation');
  populateKeywordsTable(article.keywords);
  // Loop through keywords object and print as a list
  populateEntitiesTable(article.entities);
  // const entityExplanation = document.getElementById('entity-explanation');
}
function populateSentimentCell(cell, sentiment, data) {
  // Colour the text
  const colour =
    sentiment === 'positive' ? 'green-500' : sentiment === 'negative' ? 'red-500' : 'gray-500';
  cell.className = 'px-2 py-2 text-center text-sm';
  const span = document.createElement('span');
  span.className = `text-${colour} text-xxs`;
  const emoji = getEmoji('sentiment', sentiment);
  cell.innerHTML = `
            <span class='block'> ${emoji}</span >
            <span class="text-xxs text-${colour}">${data}</span>`;
  return cell;
}
function populateEmotionCell(cell, emotion) {
  cell.className = 'px-2 py-2 text-center text-sm';
  // Check for two emojis and add them both if necessary
  if (emotion.length === 2) {
    cell.innerHTML = `<span class="block" > ${getEmoji('emotion', emotion[0])} / ${getEmoji('emotion', emotion[1])}</span><span class="text-sm">${emotion.join(', ')}</span>`;
  } else {
    cell.innerHTML = `<span class="block">${getEmoji('emotion', emotion[0])}</span><span class="text-sm">${emotion[0]}</span>`;
  }
  return cell;
}

function populateKeywordsTable(keywords) {
  // Grab keywords page elements
  const keywordResults = document.getElementById('keyword-results');

  // loop through every keyword in the object
  Object.entries(keywords).forEach(
    // destructure elements for easier reference
    ([
      text,
      {
        sentiment: { label: sentiment },
        plutchik: emotion,
        relevance,
      },
    ]) => {
      const keywordRow = document.createElement('tr');
      // return count of highest emotion
      const cellData = [
        Math.round((relevance + Number.EPSILON) * 100) / 100,
        text,
        emotion,
        sentiment,
      ];

      // loop through each table cell
      cellData.forEach((data) => {
        let cell = document.createElement('td');

        if (data === text) {
          cell.className = 'px-2 py-2 text-center text-md';
          cell.innerHTML = `
          <span class="text-sm">${data}</span>`;
        } else if (data === sentiment) {
          cell = populateSentimentCell(cell, sentiment, data);
        } else if (data === emotion) {
          cell = populateEmotionCell(cell, emotion);
        } else {
          cell.className = 'px-2 py-1 text-center text-md';
          cell.innerHTML = data;
        }

        keywordRow.appendChild(cell);
      });

      keywordResults.appendChild(keywordRow);
    },
  );
}

function populateEntitiesTable(entities) {
  // Grab entity page elements
  const entityResults = document.getElementById('entity-results');
  // Loop through entities object and append elements to a table
  Object.entries(entities).forEach(
    ([
      name,
      {
        type,
        count,
        sentiment: { label: sentiment },
        plutchik: emotion,
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
        emotion,
        sentiment,
        count,
      ];
      // populate the data into table cells
      cellData.forEach((data) => {
        let cell = document.createElement('td');
        // Entity type (person, organization, ...)
        if (data === type) {
          cell.className = 'px-2 py-2 text-center text-sm';
          const emoji = (cell.innerHTML = getEmoji('type', type));
          cell.innerHTML = `
            <span class="block"> ${emoji}</span>
            <span class="text-xxs">${data}</span>`;
        }
        // Sentiment (positive, negative, neutral)
        else if (data === sentiment) {
          cell = populateSentimentCell(cell, sentiment);
        }
        // Emotion
        else if (data === emotion) {
          cell = populateEmotionCell(cell, emotion, data);
        } else {
          cell.className = 'px-2 py-1 text-center text-xs';
          cell.innerHTML = data;
        }
        entityRow.appendChild(cell);
      });
      entityResults.appendChild(entityRow);
    },
  );
}
// Fetch and display articles on page load
fetchArticles();
