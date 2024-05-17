import {
  Timestamp,
  arrayRemove,
  arrayUnion,
  collection,
  doc,
  getDoc,
  getDocs,
  setDoc,
  updateDoc,
} from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js';

import { firestore } from './firebase.js';
import { currentUser } from './user.js';

/**
 * add history to user database bu providing the articleID as a string
 */
export async function addHistory(articleID) {
  const loggedInUser = await currentUser;
  const userID = loggedInUser.uid;
  const article = doc(firestore, 'users', userID, 'history', articleID);

  await setDoc(article, {
    dateScanned: Timestamp.now(),
  });
}

/**
 * write users history to html
 */
async function writeHistory() {
  const loggedInUser = await currentUser;
  const userID = loggedInUser.uid;
  const user = doc(firestore, 'users', userID);
  const savedSnapshot = await getDoc(user);
  const savedArticles = savedSnapshot.data().savedArticles;
  const historySnapshot = await getDocs(collection(firestore, 'users', userID, 'history'));
  historySnapshot.forEach(async (historicalArticle) => {
    const articleID = historicalArticle.id;
    let articleBody;
    let date = historicalArticle.data().dateScanned.toDate().toString().split(' ');
    date = date.slice(0, 5).join(' ');
    const articleSnapshot = await getDoc(doc(firestore, 'articles', articleID));
    if (articleSnapshot.exists()) {
      articleBody = articleSnapshot.data().scannedText;
      // get other data from article
    } else {
      console.log('article missing from firestore');
      articleBody = 'Article Missing.';
      // Assign defaults if article is missing
    }
    const myTemplate = document.getElementById('history-card');

    const newCard = myTemplate.content.cloneNode(true);
    newCard.querySelector('.analyzed-text').innerHTML = articleBody;
    newCard.querySelector('.ai-gauge').style = 'width: 2%';
    newCard.querySelector('.bias-gauge').style = 'width: 80%';
    newCard.querySelector('.scanned-date').innerHTML = date;
    const buttonID = 'save-' + articleID;
    newCard.querySelector('.save-button').id = buttonID;
    const buttonElement = newCard.getElementById(buttonID);
    if (savedArticles.includes(articleID)) buttonElement.classList.add('fill-primary');
    buttonElement.addEventListener('click', () => {
      saveArticleToggle(articleID);
    });

    document.getElementById('history-cards').appendChild(newCard);
  });
}

/**
 * Toggle articles from save array
 */
export async function saveArticleToggle(articleID) {
  const loggedInUser = await currentUser;
  const userID = loggedInUser.uid;
  const user = doc(firestore, 'users', userID);
  const savedSnapshot = await getDoc(user);
  const savedArticles = savedSnapshot.data().savedArticles;

  if (savedArticles.includes(articleID)) {
    await updateDoc(user, {
      savedArticles: arrayRemove(articleID),
    });
    document.getElementById('save-' + articleID).classList.remove('fill-primary');
  } else {
    await updateDoc(user, {
      savedArticles: arrayUnion(articleID),
    });
    document.getElementById('save-' + articleID).classList.add('fill-primary');
  }
}

if (window.location.href.match('history.html') != null)
  window.addEventListener('load', writeHistory);
