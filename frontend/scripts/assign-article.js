import {
  addDoc,
  arrayUnion,
  collection,
  doc,
  getDoc,
  getDocs,
  updateDoc,
} from 'firebase/firestore';

import { firestore } from './firebase.js';

/**
 * update an author and publisher to include new article. If publisher or author does not exist
 * a new publisher or author is created. Publisher will be created before an author
 */
export async function assignArticle(articleID) {
  const articleSnapshot = await getDoc(doc(firestore, 'articles', articleID));
  const authorsSnapshot = await getDocs(collection(firestore, 'authors'));
  const publisherSnapshot = await getDocs(collection(firestore, 'publishers'));
  const article = articleSnapshot.data();
  let authorExists = false;
  authorsSnapshot.forEach((authorInDB) => {
    if (authorInDB.data().name.trim().toLowerCase() === article.author.trim().toLowerCase())
      authorExists = true;
  });
  if (!authorExists) {
    // the author doesnt exist
    let publisherExists = false;
    publisherSnapshot.forEach(async (publisher) => {
      if (publisher.data().name.trim().toLowerCase() === article.publisher.trim().toLowerCase())
        publisherExists = true;
    });
    if (!publisherExists) await createPublisher(article, articleID);

    await createAuthor(article, articleID);
  } else {
    // the author exists
    authorsSnapshot.forEach(async (authorInDB) => {
      // Update AI/Bias scores
      if (authorInDB.data().name.trim().toLowerCase() === article.author.trim().toLowerCase()) {
        await updateDoc(doc(firestore, 'authors', authorInDB.id), {
          articles: arrayUnion(articleID),
        });
        let publisherExists = false;
        publisherSnapshot.forEach(async (publisherInDB) => {
          // Update AI/Bias scores
          if (
            publisherInDB.data().name.trim().toLowerCase() ===
            article.publisher.trim().toLowerCase()
          ) {
            publisherExists = true;
            await updateDoc(doc(firestore, 'publishers', publisherInDB.id), {
              articles: arrayUnion(articleID),
              authors: arrayUnion(authorInDB.id),
            });
            await updateDoc(doc(firestore, 'authors', authorInDB.id), {
              articles: arrayUnion(articleID),
              publishedFor: arrayUnion(publisherInDB.id),
            });
          }
        });
        if (!publisherExists) await createPublisher(article, articleID);
      }
    });
  }
}

async function createAuthor(article, articleID) {
  console.log('here');
  const publisherSnapshot = await getDocs(collection(firestore, 'publishers'));
  publisherSnapshot.forEach(async (publisherInDB) => {
    if (publisherInDB.data().name.trim().toLowerCase() === article.publisher.trim().toLowerCase()) {
      const newAuthor = await addDoc(collection(firestore, 'authors'), {
        aiScore: article.aiDetection / 100,
        articles: [articleID],
        biasScore: article.bias / 100,
        name: article.author,
        publishedFor: [publisherInDB.id],
      });
      await updateDoc(doc(firestore, 'publishers', publisherInDB.id), {
        authors: arrayUnion(newAuthor.id),
      });
    }
  });
}

async function createPublisher(article, articleID) {
  const newPublisher = await addDoc(collection(firestore, 'publishers'), {
    aiScore: article.aiDetection / 100,
    articles: [articleID],
    biasScore: article.bias / 100,
    name: article.publisher,
    authors: [],
  });
  console.log(newPublisher.id);
}
