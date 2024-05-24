async function loadPaginationTemplate() {
  const xhr = new XMLHttpRequest();
  xhr.open('GET', '/frontend/html/templates/analysis-navigation-template.html', true);

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      document.getElementById('analysis-navigation-placeholder').innerHTML = xhr.responseText;
      // highlightActiveLink();
    }
  };

  xhr.send();
}

// async function highlightActiveLink() {
//   const currentPath = window.location.pathname.split('/').pop();
//   const links = document.querySelectorAll('#pagination-placeholder a');

//   console.log(currentPath, links, 'asdf');
//   links.forEach((link) => {
//     if (link.getAttribute('href') === currentPath) {
//       console.log('asdf');
//     }
//   });
// }

document.addEventListener('DOMContentLoaded', function () {
  loadPaginationTemplate();
});
