import ApexCharts from 'apexcharts';
import { collection, getDocs } from 'firebase/firestore';

import { firestore } from './firebase.js';

// load the page
const { article, docEmotion, entityEmotion, keywordEmotion } = await fetchData();

function createApexChart(docEmotion, entityEmotions, keywordEmotions) {
  const options = {
    // Populate options in radar chart
    series: [
      {
        name: 'Entire Article',
        data: [
          docEmotion.joy,
          docEmotion.anger,
          docEmotion.disgust,
          docEmotion.sadness,
          docEmotion.fear,
        ],
      },
      {
        name: 'Entities',
        data: [
          entityEmotions.joy,
          entityEmotions.anger,
          entityEmotions.disgust,
          entityEmotions.sadness,
          entityEmotions.fear,
        ],
      },
      {
        name: 'Keywords',
        data: [
          keywordEmotions.joy,
          keywordEmotions.anger,
          keywordEmotions.disgust,
          keywordEmotions.sadness,
          keywordEmotions.fear,
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
    yaxis: {
      forceNiceScale: true,
    },
    xaxis: {
      forceNiceScale: true,
      categories: ['Joy', 'Anger', 'Disgust', 'Sadness', 'Fear'],
    },
  };
  const chart = new ApexCharts(document.querySelector('#chart'), options);
  chart.render();
}

function createSpan(emoji, data, colour = '') {
  // return span blocks for table cells with emojis stacked on text
  return `<span class='block'>${emoji}</span>
            <span class="text-xxs text-${colour}">${data}</span>`;
}

const evaluateTrust = function (trustResult) {
  return trustResult === 'yes' ? 'trustworthy' : 'untrustworthy';
};
async function fetchData() {
  // Get the 'articles' collection from Firestore
  const articlesCollection = collection(firestore, 'articles');
  // Fetch all documents from the 'articles' collection
  const articlesSnapshot = await getDocs(articlesCollection);
  let firestoreDocument;
  articlesSnapshot.forEach((doc) => {
    if (doc.id === 'J1gwG4YR1y5EMZITRg1a') {
      firestoreDocument = doc.data();
    }
  });
  return {
    article: firestoreDocument.tone,
    docEmotion: firestoreDocument.tone.document.emotion,
    entityEmotion: firestoreDocument.tone.entities['averaged emotions'],
    keywordEmotion: firestoreDocument.tone.keywords['averaged emotions'],
  };
}

// return emoji for a table cell
const getEmoji = function (category, value) {
  if (category === 'type') {
    switch (value) {
      case 'Money':
        return '💰';
      case 'Organization':
        return '🌐';
      case 'Person':
        return '👥';
      case 'Location':
        return '🗺';
      case 'Date':
        return '🗓';
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
      case 'despair':
        return '😭';
      case 'rage':
        return '🤬';
      case 'ecstatic':
        return '😄';
      case 'envy':
        return '😧';
      case 'contempt':
        return '😒';
      case 'melancholy':
        return '🥹';
      case 'remorse':
        return '😩';
      case 'guilt':
        return '😟';
      case 'shame':
        return '😳';
      case 'terror':
        return '😱';
      case 'loathing':
        return '😖';
      case 'grief':
        return '😞';
      case 'serenity':
        return '😇';
      case 'pensiveness':
        return '😔';
      case 'annoyance':
        return '🤨';
      case 'boredeom':
        return '🙄';
    }
  }
};

function emotionIntensity(intensity) {
  if (intensity === 'unchanged') {
    return ['average intensity', 'were left unchanged due to an average score'];
  }
  if (intensity === 'combined') {
    return [
      'moderately strong intensity',
      'had close enough values and were high enough to constitute combining them into a stronger emotion',
    ];
  }
  if (intensity === 'weakened') {
    return ['weak intensity', 'were renamed to reflect a very low intensity'];
  } else {
    return [
      'very strong intensity',
      'had a strong outlier that dominated the others and as a result the intensity was renamed to reflect intensity of the single emotion',
    ];
  }
}
function emotionSummary(type, article, intensity) {
  const emotions = article.plutchik;
  if (type === 'document') {
    if (emotions.length === 3) {
      return `Its dominant emotions are <span class="font-bold">${article.plutchik[0]}</span> and <span class="font-bold">${article.plutchik[1]}</span> and are considered <span class="font-bold">${intensity}</span>`;
    } else {
      return `Its dominant emotion is <span class="font-bold">${article.plutchik[0]}</span> and is considered <span class="font-bold">${intensity}</span>`;
    }
  }
}
function emotionSummaryObjects(type, trend) {
  const trendArray = Object.entries(trend);
  // sort keys, values from largest to smallest
  trendArray.sort((a, b) => b[1] - a[1]);

  let analysisString = ``;
  trendArray.forEach(([key, value]) => {
    const summary = emotionIntensity(key)[1];
    // add a conjunction if this isn't the first part of the string
    analysisString = analysisString.length === 0 ? '' : analysisString + ' and ';
    if (value > 0.7) {
      analysisString += `most ${type} emotions ${summary}`;
    } else if (value > 0.5) {
      analysisString += `the majority of ${type} emotions ${summary}`;
    } else if (value > 0.3) {
      analysisString += `a significant portion of ${type} emotions ${summary}`;
    } else {
      analysisString += `a small percentage of ${type} emotions ${summary}`;
    }
  });
  return analysisString.charAt(0).toUpperCase() + analysisString.slice(1);
}
function relevanceSummary(type, article) {
  if (article['averaged relevance'] > 0.9) {
    return `The ${type} for this article are <span class="font-bold">extremely relevant</span> overall`;
  } else if (article['averaged relevance'] > 0.7) {
    return `The ${type} for this article are <span class="font-bold">mostly relevant</span> overall`;
  } else if (article['averaged relevance'] > 0.5) {
    return `The ${type} for this article are of <span class="font-bold">average relevance</span> overall`;
  } else {
    return `The ${type} for this article are <span class="font-bold">minimal relevance</span> overall`;
  }
}

function prepareSummary(section, article) {
  // return a string summary for a section based on the contents of the category object
  console.log(article);
  if (section === 'document') {
    const docResults = document.getElementById('document-results');
    const docExplanation = document.getElementById('document-explanation');
    const lastElement = article.plutchik[article.plutchik.length - 1];
    const intensity = emotionIntensity(lastElement);
    docResults.innerHTML = `${sentimentSummary(article)}. The emotions were ${emotionSummary('document', article, intensity[0])}. The article may feel ${evaluateTrust(article.trust)} to readers.`;
    docExplanation.innerHTML = `The emotions ${intensity[1]}. Trust is evaluated as true only when a document's 'disgust' rating is close to zero.`;
  }
  if (section === 'keywords' || section === 'entities') {
    const explanationElement =
      section === 'keywords'
        ? document.getElementById('keyword-explanation')
        : document.getElementById('entity-explanation');
    explanationElement.innerHTML = `${relevanceSummary(section, article)}. ${emotionSummaryObjects(section, article['emotion trend'])}. The ${section} overall felt <span class="font-bold">${evaluateTrust(article.trust)}</span> to readers.`;
  }
}

function sentimentSummary(type, article) {
  if (type === 'document') {
    return `The article has a <span class="font-bold">${article.sentiment.label}</span> sentiment to it`;
  }
}
function loadPageElements(article) {
  // create the Apex Chart
  // createApexChart(docEmotion, entityEmotions, keywordEmotions);

  // Grab title page elements
  // if (article.metadata) {
  //  const titleSection = document.getElementById('accordion-color-heading-2')
  //  titleSection.classList.remove("hidden")
  //  const titleResults = document.getElementById('title-results');
  //  const titleExplanation = document.getElementById('title-explanation');
  // }

  populateKeywordsTable(article.keywords);
  populateEntitiesTable(article.entities);
  ['document', 'entities', 'keywords'].forEach((category) => {
    prepareSummary(category, article[`${category}`]);
  });
}

const notInsideEntityOrKeyword = function (text) {
  // checks if you are on the root level of a collection or inside of an entity/keyword
  return !['averaged emotions', 'averaged relevance', 'emotion trend', 'general trust'].includes(
    text,
  );
};

// populate an emotion cell with one or two emojis separated with a /
// and one or more strings separated with a comma
function populateEmotionCell(cell, emotion) {
  cell.className = returnCellStyles('sm');

  // Display one emoji and emotion text underneath
  if (emotion.length === 2) {
    cell.innerHTML = `<span class="block">${getEmoji('emotion', emotion[0])}</span><span class="text-xxs">${emotion[0]}</span>`;
    // display two emojis separated by a slash, and the two emotions underneath
  } else if (emotion.length === 3) {
    const emojis = emotion // slice the emotion name from text and grab both emojis
      .slice(0, 2)
      .map((e) => getEmoji('emotion', e)) // concatenate the emojis and join with a '/'
      .join(' / ');
    cell.innerHTML = `<span class="block">${emojis}</span><span class="text-xxs">${emotion[0]}, ${emotion[1]}</span>`;
  }
  return cell;
}

// populate a sentiment cell with an emoji and coloured text
function populateSentimentCell(cell, sentiment, data) {
  const colour =
    sentiment === 'positive' ? 'green-500' : sentiment === 'negative' ? 'red-500' : 'gray-500';
  cell.className = returnCellStyles('sm');
  const emoji = getEmoji('sentiment', sentiment);
  cell.innerHTML = createSpan(emoji, data, colour);
  return cell;
}

// populate the entities section of the page
function populateEntitiesTable(entities) {
  const entityResults = document.getElementById('entity-results');

  // Loop through entities object and append elements to a table
  Object.entries(entities).forEach(([name, keyword]) => {
    if (notInsideEntityOrKeyword(name)) {
      const {
        // destructure the object for ease of reference
        type,
        count,
        sentiment: { label: sentiment },
        plutchik: emotion,
        relevance,
      } = keyword;

      const entityRow = document.createElement('tr');

      const cellData = [
        Math.round((relevance + Number.EPSILON) * 100) / 100, // Round float to two decimal places
        name,
        type,
        emotion,
        sentiment,
        count,
      ];

      // populate the data into table cells
      cellData.forEach((data) => {
        let cell = document.createElement('td');
        cell.className = returnCellStyles('sm');

        // Entity type (person, organization, ...)
        if (data === type) {
          const emoji = (cell.innerHTML = getEmoji('type', type));
          cell.innerHTML = createSpan(emoji, data);
        }
        // Sentiment (positive, negative, neutral)
        else if (data === sentiment) {
          cell = populateSentimentCell(cell, sentiment, data);
        }
        // Emotion
        else if (data === emotion) {
          cell = populateEmotionCell(cell, emotion, data);
        } else {
          cell.innerHTML = data;
        }
        entityRow.appendChild(cell);
      });
      entityResults.appendChild(entityRow);
    }
  });
}

// populate the keywords section of the page
function populateKeywordsTable(keywords) {
  const keywordResults = document.getElementById('keyword-results');

  Object.entries(keywords).forEach(([text, keyword]) => {
    if (notInsideEntityOrKeyword(text)) {
      const {
        // destructuring for easier referencing inside object
        sentiment: { label: sentiment },
        plutchik: emotion,
        relevance,
      } = keyword;

      const keywordRow = document.createElement('tr');

      const cellData = [
        // round the float to two digits
        Math.round((relevance + Number.EPSILON) * 100) / 100,
        text,
        emotion,
        sentiment,
      ];

      // loop through each table cell
      cellData.forEach((data) => {
        let cell = document.createElement('td');
        cell.className = returnCellStyles('md');

        if (data === text) {
          cell.innerHTML = `<span class="text-sm">${data}</span>`;
        } else if (data === sentiment) {
          cell = populateSentimentCell(cell, sentiment, data);
        } else if (data === emotion) {
          cell = populateEmotionCell(cell, emotion);
        } else {
          cell.innerHTML = data;
        }
        keywordRow.appendChild(cell);
      });
      keywordResults.appendChild(keywordRow);
    }
  });
}

const returnCellStyles = (size) => `px-2 py-2 text-center text-${size}`; // tailwind classes for table cell

createApexChart(docEmotion, entityEmotion, keywordEmotion);
loadPageElements(article);
