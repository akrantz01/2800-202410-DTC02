import { doc, getDoc } from 'firebase/firestore';

import { getPublisherID } from './assign-article.js';
import { firestore } from './firebase.js';
import { saveArticleToggle } from './history.js';
import { currentUser } from './user.js';

function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

/**
 * write publisher details to html
 */
async function populatePublisherDetails() {
  const publisherName = getQueryParam('name');
  const publisherID = await getPublisherID(publisherName);
  const publisherArticlesSnapshot = await getDoc(doc(firestore, 'publishers', publisherID));
  const publisher = publisherArticlesSnapshot.data();
  document.getElementById('publisher-name').innerHTML = publisher.name;
  document.getElementById('ai-gauge').style = `width: ${publisher.aiScore * 100}%`;
  document.getElementById('bias-gauge').style = `width: ${publisher.biasScore * 100}%`;
  const authorsHTML = document.getElementById('publisher-authors');
  authorsHTML.innerHTML = '';
  if (publisher.authors.length <= 1) document.getElementById('drop-button').classList.add('hidden');

  document.getElementById('drop-button').addEventListener('click', () => {
    authorsHTML.classList.toggle('line-clamp-1');

    document.getElementById('drop-button').classList.toggle('rotate-180');
  });
  publisher.authors.forEach(async (author) => {
    const authorCard = document.createElement('p');
    const authorSnapshot = await getDoc(doc(firestore, 'authors', author));
    authorCard.innerHTML = authorSnapshot.data().name;
    authorCard.classList.add('px-4', 'py-2', 'shadow-md', 'rounded-lg', 'border');
    authorCard.addEventListener('click', () => {
      window.location.href = `author?name=${authorSnapshot.data().name}`;
    });
    authorsHTML.appendChild(authorCard);
  });
}

/**
 * write publisher articles to html
 */
async function writePublisherArticles() {
  const publisherName = getQueryParam('name');
  const publisherID = await getPublisherID(publisherName);
  const loggedInUser = await currentUser;
  const userID = loggedInUser.uid;

  const savedSnapshot = await getDoc(doc(firestore, 'users', userID));
  const savedArticles = savedSnapshot.data().savedArticles;

  const publisherArticlesSnapshot = await getDoc(doc(firestore, 'publishers', publisherID));
  const publisherArticles = publisherArticlesSnapshot.data().articles;
  publisherArticles.forEach(async (article) => {
    const articleID = article;
    let articleBody;
    let aiGauge;
    let biasGauge;
    let articleExists = false;

    const articleSnapshot = await getDoc(doc(firestore, 'articles', articleID));
    if (articleSnapshot.exists()) {
      articleBody = articleSnapshot.data().title;
      articleExists = true;
      if (articleSnapshot.data().ai) aiGauge = `width: ${articleSnapshot.data().ai.aiScore * 100}%`;
      if (articleSnapshot.data().bias)
        biasGauge = `width: ${articleSnapshot.data().bias.biasScore * 100}%`;

      // get other data from article
    } else {
      articleBody = 'Article Reference Missing';
      aiGauge = 'width: 0%';
      biasGauge = 'width: 0%';
      // Assign defaults if article is missing
    }
    const myTemplate = document.getElementById('saved-card');

    const newCard = myTemplate.content.cloneNode(true);
    newCard.querySelector('.analyzed-text').innerHTML = articleBody;
    if (aiGauge) newCard.querySelector('.ai-gauge').style = aiGauge;
    else newCard.querySelector('.ai-tag').innerHTML = 'No AI score available';

    if (biasGauge) newCard.querySelector('.bias-gauge').style = biasGauge;
    else newCard.querySelector('.bias-tag').innerHTML = 'No Bias score available';
    if (articleExists) {
      newCard.querySelector('.link').addEventListener('click', () => {
        window.location.href = 'summary?uid=' + articleID;
      });
      const buttonID = 'save-' + articleID;
      newCard.querySelector('.save-button').id = buttonID;
      const buttonElement = newCard.getElementById(buttonID);
      if (savedArticles.includes(article)) buttonElement.classList.add('fill-red-500');
      buttonElement.addEventListener('click', () => {
        saveArticleToggle(articleID);
      });
      document.getElementById('publisher-cards').appendChild(newCard);
    } else {
      newCard.querySelector('.link').classList.add('hidden');
      newCard.querySelector('.save-button').classList.add('hidden');
      newCard.querySelector('.gauges').classList.add('hidden');
    }
  });
}

if (window.location.href.match('publisher') != null)
  window.addEventListener('load', async () => {
    writePublisherArticles();
    populatePublisherDetails();
  });
