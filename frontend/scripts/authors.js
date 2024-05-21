import { doc, getDoc } from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js';

import { firestore } from './firebase.js';
import { saveArticleToggle } from './history.js';
import { currentUser } from './user.js';

/**
 * write author details to html
 */
async function populateAuthorDetails() {
  localStorage.setItem('authorID', 'demo');
  const authorID = localStorage.getItem('authorID');
  const authorArticlesSnapshot = await getDoc(doc(firestore, 'authors', authorID));
  const author = authorArticlesSnapshot.data();
  document.getElementById('author-name').innerHTML = author.name;
  document.getElementById('ai-gauge').style = `width: ${author.aiScore * 100}%`;
  document.getElementById('bias-gauge').style = `width: ${author.biasScore * 100}%`;
  const publishers = document.getElementById('author-publishers');
  publishers.innerHTML = '';
  if (author.publishedFor.length <= 1)
    document.getElementById('drop-button').classList.add('hidden');
  author.publishedFor.forEach(async (publisher) => {
    const publisherCard = document.createElement('p');
    const publisherSnapshot = await getDoc(doc(firestore, 'publishers', publisher));
    publisherCard.innerHTML = publisherSnapshot.data().name;
    publisherCard.addEventListener('click', () => {
      console.log(publisher);
    });
    publishers.appendChild(publisherCard);
  });
}

/**
 * write author articles to html
 */
async function writeAuthorArticles() {
  const authorID = localStorage.getItem('authorID');
  const loggedInUser = await currentUser;
  const userID = loggedInUser.uid;

  const savedSnapshot = await getDoc(doc(firestore, 'users', userID));
  const savedArticles = savedSnapshot.data().savedArticles;

  const authorArticlesSnapshot = await getDoc(doc(firestore, 'authors', authorID));
  const authorArticles = authorArticlesSnapshot.data().articles;
  authorArticles.forEach(async (article) => {
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
    document.getElementById('author-cards').appendChild(newCard);
  });
}

if (window.location.href.match('author.html') != null)
  window.addEventListener('load', async () => {
    writeAuthorArticles();
    populateAuthorDetails();
  });
