window.addEventListener('pywebviewready', function() {
  async function getPortfolio() {
      document.getElementById("loading").setAttribute("aria-busy", "true");
      document.getElementById("loading").setAttribute("aria-label", "Loading");
      const portfolio = pywebview.api.getPortfolio()
          .then((response) => { return JSON.parse(response) });
      const portfolio_ = await portfolio;
      console.log(portfolio_);
      const htmltable = ConvertJsonToTable(portfolio_);
      document.getElementById("portfolioTable").innerHTML = htmltable;
      const chartSymbols = portfolio_.map(item => item.Symbol);
      const chartValues = portfolio_.map(item => item.Value);
      const chartDiv = document.getElementById('portfolioChart');
      const chartData = {
        labels: chartSymbols,
        datasets: [{
          label: 'Portfolio',
          data: chartValues,
          backgroundColor: [
            'rgb(19,24,98)',
            'rgb(46,68,130)',
            'rgb(84,107,171)',
            'rgb(135,136,156)',
            'rgb(190,169,222)'
          ],
          hoverOffset: 4
        }]
      };
      const config = {
        type: 'pie',
        data: chartData,
      };
      const myChart = new Chart(chartDiv.getContext('2d'), config);
      document.getElementById("loading").setAttribute("aria-busy", "false");
      document.getElementById("loading").removeAttribute("aria-label");
  };
  getPortfolio();
  //document.getElementById("getPortfolioBtn").addEventListener("click", getPortfolio);
});

