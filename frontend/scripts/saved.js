import { doc, getDoc } from 'firebase/firestore';

import { firestore } from './firebase.js';
import { saveArticleToggle } from './history.js';
import { currentUser } from './user.js';

/**
 * write users saves to html
 */
async function writeSaves() {
  const loggedInUser = await currentUser;
  const userID = loggedInUser.uid;

  const savedSnapshot = await getDoc(doc(firestore, 'users', userID));
  const savedArticles = savedSnapshot.data().savedArticles;
  if (savedArticles) {
    savedArticles.forEach(async (savedArticle) => {
      const articleID = savedArticle;
      let articleBody;
      let aiGauge;
      let biasGauge;
      let articleExists = false;

      if (articleID) {
        const articleSnapshot = await getDoc(doc(firestore, 'articles', articleID));
        if (articleSnapshot.exists()) {
          articleBody = articleSnapshot.data().title;
          articleExists = true;
          if (articleSnapshot.data().ai)
            aiGauge = `width: ${articleSnapshot.data().ai.aiScore * 100}%`;
          if (articleSnapshot.data().bias)
            biasGauge = `width: ${articleSnapshot.data().bias.biasScore * 100}%`;

          // get other data from article
        } else {
          console.log('article missing from firestore');
          articleBody = 'Article Reference Missing';
          aiGauge = 'width: 0%';
          biasGauge = 'width: 0%';
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
          buttonElement.addEventListener('click', () => {
            saveArticleToggle(articleID);
          });
          document.getElementById('saved-cards').appendChild(newCard);
        } else {
          newCard.querySelector('.link').classList.add('hidden');
          newCard.querySelector('.save-button').classList.add('hidden');
          newCard.querySelector('.gauges').classList.add('hidden');
        }
      }
    });
  }
}

if (window.location.href.match('saved') != null) window.addEventListener('load', writeSaves);
