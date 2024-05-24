import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: 'AIzaSyDFLFRGurcbgQHPheZcI14xPRCSegGs6w4',
  authDomain: 'sharp-bivouac-422118-s5.firebaseapp.com',
  projectId: 'sharp-bivouac-422118-s5',
  storageBucket: 'sharp-bivouac-422118-s5.appspot.com',
  messagingSenderId: '866031185534',
  appId: '1:866031185534:web:248d1e3006ad000a3d722f',
};

export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const firestore = getFirestore(app);
