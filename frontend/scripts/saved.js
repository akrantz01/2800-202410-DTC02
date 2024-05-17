import { doc, getDoc } from 'https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js';

import { firestore } from './firebase.js';
import { currentUser } from './user.js';

/**
 * write users saves to html
 */
async function writeSaves() {
  const loggedInUser = await currentUser;
  const userID = loggedInUser.uid;

  const savedSnapshot = await getDoc(doc(firestore, 'users', userID));
  const articles = savedSnapshot.data().savedArticles;
  articles.forEach(async (savedArticle) => {
    const articleID = savedArticle;
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
    // newCard.querySelector('.scanned-date').innerHTML = date;

    document.getElementById('saved-cards').appendChild(newCard);
  });
}

if (window.location.href.match('saved.html') != null) window.addEventListener('load', writeSaves);
