import { collection, getDocs } from 'firebase/firestore';

import { firestore } from './firebase.js';

async function fetchBiases() {
  // Get the query string from the URL
  const queryString = window.location.search;

  // Parse the query string to get URL parameters
  const urlParams = new URLSearchParams(queryString);

  // Get the value of the 'bias' parameter
  const biasName = urlParams.get('bias');

  // Example URL: https://example.com/learn.html?bias=Confirmation%20Bias
  // In this URL:
  // - 'learn.html' is the webpage being accessed.
  // - '?bias=Confirmation%20Bias' is the query string.
  //    - 'bias' is the key.
  //    - 'Confirmation%20Bias' is the value (URL-encoded to replace spaces with '%20').

  // Get the 'biases' collection from Firestore
  const biasesCollection = collection(firestore, 'biases');

  // Fetch all documents from the 'biases' collection
  const biasesSnapshot = await getDocs(biasesCollection);

  // Map the documents to an array of data
  const biasesList = biasesSnapshot.docs.map((doc) => doc.data());

  // Get the container element where biases will be displayed
  const biasContainer = document.getElementById('bias-container');

  // Get the error message element
  const errorMessage = document.getElementById('error-message');

  // Clear the container and hide the error message
  biasContainer.innerHTML = '';
  errorMessage.classList.add('hidden');

  // If a bias name is provided in the URL
  if (biasName) {
    // Find the bias matching the provided name
    const filteredBias = biasesList.find(
      (bias) => bias.name.toLowerCase() === biasName.toLowerCase(),
    );

    // If the bias is found, display it
    if (filteredBias) {
      biasContainer.innerHTML = createBiasCard(filteredBias);
    } else {
      // If not found, show an error message
      errorMessage.textContent = 'No information found for the specified bias.';
      errorMessage.classList.remove('hidden');
    }
  } else {
    // If no bias name is provided, display all biases
    biasesList.forEach((bias) => {
      biasContainer.innerHTML += createBiasCard(bias);
    });
  }
}

// Function to create an HTML card for a bias
function createBiasCard(bias) {
  return `
    <div class="bg-white shadow-md rounded-lg p-4 border border-gray-300">
      <h2 class="text-2xl font-bold text-primary mb-2">${bias.name}</h2>
      <p class="text-gray-500"><strong class="text-black">Description:</strong> ${bias.description}</p>
      <p class="text-gray-500"><strong class="text-black">Example:</strong> ${bias.example}</p>
      <p class="text-gray-500"><strong class="text-black">Impact:</strong> ${bias.impact}</p>
    </div>
  `;
}

// Fetch and display biases on page load
fetchBiases();
