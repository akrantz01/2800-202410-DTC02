// For loading the tempalte into the DOM
async function loadPaginationTemplate() {
  const xhr = new XMLHttpRequest();
  xhr.open('GET', '/templates/analysis-navigation-template.html', true);

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      document.getElementById('analysis-navigation-placeholder').innerHTML = xhr.responseText;

      const hrefArray = getHrefArray();
      setNavClass(hrefArray);
    }
  };

  xhr.send();
}

function getUid() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('uid');
}

// Helper function for getting the file name from the url
function getCurrentFileName() {
  const url = window.location.href;
  const fileName = url.substring(url.lastIndexOf('/') + 1);
  return fileName;
}

// Helper function for getting an array of the available href links
function getHrefArray() {
  const links = document.querySelectorAll('#analysis-navigation-controls a');
  const linksArray = Array.from(links);
  linksArray.forEach((link) => {
    link.setAttribute('href', `${link.getAttribute('href')}?uid=${getUid()}`);
  });
  const hrefArray = linksArray.map((link) => link.getAttribute('href'));

  return hrefArray;
}

// Sets css classes for the currently active navigation page
function setNavClass(hRefArray = []) {
  const fileName = getCurrentFileName();
  fileName.replace('.html', '');
  for (let i = 0; i < hRefArray.length; i++) {
    if (hRefArray[i] === fileName) {
      const element = document.querySelector(
        `#analysis-navigation-controls a[href="${hRefArray[i]}"]`,
      );

      // Disable link when current page
      [`border`, `rounded-lg`, `font-semibold`].map((classGroup) =>
        element.classList.toggle(classGroup),
      );
    }
  }
}

document.addEventListener('DOMContentLoaded', function () {
  loadPaginationTemplate();
});
