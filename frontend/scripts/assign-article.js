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

  const article = articleSnapshot.data();
  if (!(await authorExists(article.author))) {
    // the author doesnt exist
    if (!(await publisherExists(article.publisher))) await createPublisher(article, articleID);
    await createAuthor(article, articleID);
  } else {
    // the author exists
    const authorID = await getAuthorID(article.author);
    const publisherID = await getPublisherID(article.publisher);
    const authorDoc = doc(firestore, 'authors', authorID);
    const publisherDoc = doc(firestore, 'publishers', publisherID);
    await updateDoc(authorDoc, {
      articles: arrayUnion(articleID),
      publishedFor: arrayUnion(publisherID),
    });
    await updateDoc(publisherDoc, {
      articles: arrayUnion(articleID),
      authors: arrayUnion(authorID),
    });
  }
}

/**
 * Check if the author exists in the DB.
 *
 * @param {String} author the author name
 * @returns {bool}        bool if author exists
 */
async function authorExists(author) {
  const authorsSnapshot = await getDocs(collection(firestore, 'authors'));
  for (const authorInDB of authorsSnapshot.docs) {
    if (authorInDB.data().name.trim().toLowerCase() === author.trim().toLowerCase()) return true;
  }
  return false;
}

/**
 * Create an author in the DB.
 *
 * @param {Object} article   a json representing the article from the DB
 * @param {String} articleID the article id
 */
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

/**
 * Check if the publisher exists in the DB.
 *
 * @param {String} publisher  the publisher name
 * @returns {bool}            bool if publisher exists
 */
async function publisherExists(publisher) {
  const publishersSnapshot = await getDocs(collection(firestore, 'publishers'));
  for (const publisherInDB of publishersSnapshot.docs) {
    if (publisherInDB.data().name.trim().toLowerCase() === publisher.trim().toLowerCase())
      return true;
  }
  return false;
}

/**
 * Create a publisher in the DB.
 *
 * @param {Object} article   a json representing the article from the DB
 * @param {String} articleID the article id
 */
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

/**
 * get the author id from firestore
 *
 * @param {String} authorName name of the author
 * @returns {String}          the id of the author
 */
export async function getAuthorID(authorName) {
  const authorSnapshot = await getDocs(collection(firestore, 'authors'));
  let authorFound = false;
  let authorID = '';
  authorSnapshot.forEach((authorInDB) => {
    if (
      authorInDB.data().name.trim().toLowerCase() === authorName.trim().toLowerCase() &&
      !authorFound
    ) {
      authorFound = true;
      authorID = authorInDB.id;
    }
  });
  if (!authorFound) throw new Error('Author does not exist');

  return authorID;
}

/**
 * get the publisher id from firestore
 *
 * @param {String} publisherName  name of the publisher
 * @returns {String}              the id of the publisher
 */
export async function getPublisherID(publisherName) {
  const publisherSnapshot = await getDocs(collection(firestore, 'publishers'));
  let publisherFound = false;
  let publisherID = '';
  publisherSnapshot.forEach((publisherInDB) => {
    if (
      publisherInDB.data().name.trim().toLowerCase() === publisherName.trim().toLowerCase() &&
      !publisherFound
    ) {
      publisherFound = true;
      publisherID = publisherInDB.id;
    }
  });
  if (!publisherFound) throw new Error('Publisher does not exist');

  return publisherID;
}

/**
 * Update the author ai score in firestore.
 *
 * @param {String} author name of the author
 */
export async function updateAuthorAi(author) {
  const authorID = await getAuthorID(author);
  const authorDoc = doc(firestore, 'authors', authorID);
  const authorSnapshot = await getDoc(authorDoc);
  const articles = authorSnapshot.data().articles;
  let totalScore = 0;
  let totalCount = 0;
  for (const article of articles) {
    const articleSnapshot = await getDoc(doc(firestore, 'articles', article));
    if (articleSnapshot.data().ai) {
      totalScore += parseFloat(articleSnapshot.data().ai.aiScore);
      totalCount += 1;
    }
  }
  await updateDoc(authorDoc, {
    aiScore: totalScore / totalCount,
  });
}

/**
 * Update the publisher ai score in firestore.
 *
 * @param {String} publisher name of the publisher
 */
export async function updatePublisherAi(publisher) {
  const publisherID = await getPublisherID(publisher);
  const publisherDoc = doc(firestore, 'publishers', publisherID);
  const publisherSnapshot = await getDoc(publisherDoc);
  const articles = publisherSnapshot.data().articles;
  let totalScore = 0;
  let totalCount = 0;
  for (const article of articles) {
    const articleSnapshot = await getDoc(doc(firestore, 'articles', article));
    if (articleSnapshot.data().ai) {
      totalScore += parseFloat(articleSnapshot.data().ai.aiScore);
      totalCount += 1;
    }
  }
  await updateDoc(publisherDoc, {
    aiScore: totalScore / totalCount,
  });
}

/**
 * Update the author bias score in firestore.
 *
 * @param {String} author name of the author
 */
export async function updateAuthorBias(author) {
  const authorID = await getAuthorID(author);
  const authorDoc = doc(firestore, 'authors', authorID);
  const authorSnapshot = await getDoc(authorDoc);
  const articles = authorSnapshot.data().articles;
  let totalScore = 0;
  let totalCount = 0;
  for (const article of articles) {
    const articleSnapshot = await getDoc(doc(firestore, 'articles', article));
    if (articleSnapshot.data().bias) {
      totalScore += parseFloat(articleSnapshot.data().bias.biasScore);
      totalCount += 1;
    }
  }
  await updateDoc(authorDoc, {
    biasScore: totalScore / totalCount,
  });
}

/**
 * Update the publisher bias score in firestore.
 *
 * @param {String} publisher name of the publisher
 */
export async function updatePublisherBias(publisher) {
  const publisherID = await getPublisherID(publisher);
  const publisherDoc = doc(firestore, 'publishers', publisherID);
  const publisherSnapshot = await getDoc(publisherDoc);
  const articles = publisherSnapshot.data().articles;
  let totalScore = 0;
  let totalCount = 0;
  for (const article of articles) {
    const articleSnapshot = await getDoc(doc(firestore, 'articles', article));
    if (articleSnapshot.data().bias) {
      totalScore += parseFloat(articleSnapshot.data().bias.biasScore);
      totalCount += 1;
    }
  }
  await updateDoc(publisherDoc, {
    biasScore: totalScore / totalCount,
  });
}
