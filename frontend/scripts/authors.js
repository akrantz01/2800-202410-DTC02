import { doc, getDoc } from 'firebase/firestore';

import { getAuthorID } from './assign-article.js';
import { firestore } from './firebase.js';
import { saveArticleToggle } from './history.js';
import { currentUser } from './user.js';

function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

/**
 * write author details to html
 */
async function populateAuthorDetails() {
  const authorName = getQueryParam('name');
  const authorID = await getAuthorID(authorName);
  const authorArticlesSnapshot = await getDoc(doc(firestore, 'authors', authorID));
  const author = authorArticlesSnapshot.data();
  document.getElementById('author-name').innerHTML = author.name;
  document.getElementById('ai-gauge').style = `width: ${author.aiScore * 100}%`;
  document.getElementById('bias-gauge').style = `width: ${author.biasScore * 100}%`;
  const publishers = document.getElementById('author-publishers');
  publishers.innerHTML = '';
  if (author.publishedFor.length <= 1)
    document.getElementById('drop-button').classList.add('hidden');

  document.getElementById('drop-button').addEventListener('click', () => {
    publishers.classList.toggle('line-clamp-1');
    document.getElementById('drop-button').classList.toggle('rotate-180');
  });
  author.publishedFor.forEach(async (publisher) => {
    const publisherCard = document.createElement('p');
    const publisherSnapshot = await getDoc(doc(firestore, 'publishers', publisher));
    publisherCard.classList.add('px-4', 'py-2', 'shadow-md', 'rounded-lg', 'border');
    publisherCard.innerHTML = publisherSnapshot.data().name;
    publisherCard.addEventListener('click', () => {
      window.location.href = `publisher?name=${publisherSnapshot.data().name}`;
    });
    publishers.appendChild(publisherCard);
  });
}

/**
 * write author articles to html
 */
async function writeAuthorArticles() {
  const authorName = getQueryParam('name');
  const authorID = await getAuthorID(authorName);
  const loggedInUser = await currentUser;
  const userID = loggedInUser.uid;

  const savedSnapshot = await getDoc(doc(firestore, 'users', userID));
  const savedArticles = savedSnapshot.data().savedArticles;

  const authorArticlesSnapshot = await getDoc(doc(firestore, 'authors', authorID));
  const authorArticles = authorArticlesSnapshot.data().articles;
  authorArticles.forEach(async (article) => {
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
      console.log('article missing from firestore');
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
      document.getElementById('author-cards').appendChild(newCard);
    } else {
      newCard.querySelector('.link').classList.add('hidden');
      newCard.querySelector('.save-button').classList.add('hidden');
      newCard.querySelector('.gauges').classList.add('hidden');
    }
  });
}

if (window.location.href.match('author') != null)
  window.addEventListener('load', async () => {
    writeAuthorArticles();
    populateAuthorDetails();
  });
