function draw_all_data(chartData) {
  var data = [];
  for (var key in chartData) {
    if (key.includes("blade")) {
      data.push(
        {
          name: key,
          type: 'line',
          x: chartData[key][0],
          y: chartData[key][1],
          line: { 
            color: '#343a40', 
            width: 1 
          }
        }
      );
    } else {
      data.push(
        {
          name: key,
          type: 'line',
          x: chartData[key][0],
          y: chartData[key][1],
          line: { 
            color: '#141a40', 
            width: 2 
          }
        }
      );
    };
  };
  
  var layout = { 
    showlegend: false,
    xaxis: { showgrid: false, zeroline: false,  visible: false },
    yaxis: { showgrid: false, zeroline: false, visible: false,  scaleanchor: "x" }
  };
  
  var config = { responsive: true }
  
  Plotly.newPlot( 'chart_area', data, layout, config );
};
