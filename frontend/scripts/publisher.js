import { doc, getDoc } from 'firebase/firestore';

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
  const publisherID = getQueryParam('publisherID');
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
    authorCard.addEventListener('click', () => {
      console.log(author);
    });
    authorsHTML.appendChild(authorCard);
  });
}

/**
 * write publisher articles to html
 */
async function writePublisherArticles() {
  const publisherID = getQueryParam('publisherID');
  const loggedInUser = await currentUser;
  const userID = loggedInUser.uid;

  const savedSnapshot = await getDoc(doc(firestore, 'users', userID));
  const savedArticles = savedSnapshot.data().savedArticles;

  const publisherArticlesSnapshot = await getDoc(doc(firestore, 'publishers', publisherID));
  const publisherArticles = publisherArticlesSnapshot.data().articles;
  publisherArticles.forEach(async (article) => {
    const articleID = article;
    let articleBody;

    const articleSnapshot = await getDoc(doc(firestore, 'articles', articleID));
    if (articleSnapshot.exists()) {
      articleBody = articleSnapshot.data().scannedText;
      // get other data from article
    } else {
      console.log('article missing from firestore');
      articleBody = 'Article Missing.';
      // Assign defaults if article is missing
    }
    const myTemplate = document.getElementById('saved-card');

    const newCard = myTemplate.content.cloneNode(true);
    newCard.querySelector('.analyzed-text').innerHTML = articleBody;
    newCard.querySelector('.ai-gauge').style = 'width: 2%';
    newCard.querySelector('.bias-gauge').style = 'width: 80%';
    const buttonID = 'save-' + articleID;
    newCard.querySelector('.save-button').id = buttonID;
    const buttonElement = newCard.getElementById(buttonID);
    if (savedArticles.includes(article)) buttonElement.classList.add('fill-primary');
    buttonElement.addEventListener('click', () => {
      saveArticleToggle(articleID);
    });
    document.getElementById('publisher-cards').appendChild(newCard);
  });
}

if (window.location.href.match('publisher.html') != null)
  window.addEventListener('load', async () => {
    writePublisherArticles();
    populatePublisherDetails();
  });
