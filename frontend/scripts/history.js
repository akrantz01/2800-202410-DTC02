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
} from 'firebase/firestore';

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
    const articleSnapshot = await getDoc(doc(firestore, 'articles', articleID));
    let articleBody;
    let date = historicalArticle.data().dateScanned.toDate().toString().split(' ');
    let aiGauge;
    let biasGauge;
    let articleExists = false;
    date = date.slice(0, 5).join(' ');

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
      date = 'N/A';

      // Assign defaults if article is missing
    }
    const myTemplate = document.getElementById('history-card');

    const newCard = myTemplate.content.cloneNode(true);
    newCard.querySelector('.analyzed-text').innerHTML = articleBody;
    if (aiGauge) newCard.querySelector('.ai-gauge').style = aiGauge;
    else newCard.querySelector('.ai-tag').innerHTML = 'No AI score available';

    if (biasGauge) newCard.querySelector('.bias-gauge').style = biasGauge;
    else newCard.querySelector('.bias-tag').innerHTML = 'No Bias score available';
    newCard.querySelector('.scanned-date').innerHTML = date;
    if (articleExists) {
      newCard.querySelector('.link').addEventListener('click', () => {
        window.location.href = 'summary?uid=' + articleID;
      });
      const buttonID = 'save-' + articleID;
      newCard.querySelector('.save-button').id = buttonID;
      const buttonElement = newCard.getElementById(buttonID);
      if (savedArticles.includes(articleID)) buttonElement.classList.add('fill-red-500');
      buttonElement.addEventListener('click', () => {
        saveArticleToggle(articleID);
      });
      document.getElementById('history-cards').appendChild(newCard);
    } else {
      newCard.querySelector('.link').classList.add('hidden');
      newCard.querySelector('.save-button').classList.add('hidden');
      newCard.querySelector('.gauges').classList.add('hidden');
    }
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
    document.getElementById('save-' + articleID).classList.remove('fill-red-500');
  } else {
    await updateDoc(user, {
      savedArticles: arrayUnion(articleID),
    });
    document.getElementById('save-' + articleID).classList.add('fill-red-500');
  }
}

if (window.location.href.match('history') != null) window.addEventListener('load', writeHistory);
