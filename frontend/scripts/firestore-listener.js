import { doc, onSnapshot } from 'firebase/firestore';

import { firestore } from './firebase.js';

export async function listenForDocChanges(docId, updateData) {
  const targetDoc = doc(firestore, 'articles', docId);
  const unsubscribe = onSnapshot(targetDoc, (docSnapshot) => {
    if (docSnapshot.exists()) {
      const data = docSnapshot.data();
      updateData(data);
    } else {
      console.error('Document does not exist');
    }
  });
  return unsubscribe;
}
