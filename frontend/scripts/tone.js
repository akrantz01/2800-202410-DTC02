// Radar
const options = {
  series: [
    {
      name: 'Series 1',
      data: [80, 50, 30, 40, 100, 20],
    },
  ],
  chart: {
    toolbar: {
      show: false, // Hides hamburger menu
    },
    height: 350,
    type: 'radar',
  },
  // title: {
  //   text: 'Basic Radar Chart',
  // },
  yaxis: {
    stepSize: 20,
  },
  xaxis: {
    categories: ['January', 'February', 'March', 'April', 'May', 'June'],
  },
};

// eslint-disable-next-line no-undef
const chart = new ApexCharts(document.querySelector('#chart'), options);

chart.render();
