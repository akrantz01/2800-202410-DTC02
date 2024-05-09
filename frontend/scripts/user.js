import { auth } from './firebase.js';

/**
 * Get the current user
 *
 * @returns {Promise<import('https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js').User>} the current user
 */
export const currentUser = auth.authStateReady().then(() => auth.currentUser);
