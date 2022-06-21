function draw_chart(chartData) {
  var trace0 = {
    type: 'line',
    x: chartData.x0,
    y: chartData.y0,
    line: { color: '#343a40', width: 1 }
  };
  var trace1 = {
    type: 'line',
    x: chartData.x1,
    y: chartData.y1,
    line: { color: '#343a40', width: 1 }
  };
  var trace2 = {
    type: 'line',
    x: chartData.x2,
    y: chartData.y2,
    line: { color: '#343a40', width: 1 }
  };
  
  var data = [ trace0, trace1, trace2 ];
  
  var layout = { 
    showlegend: false,
    xaxis: { showgrid: false, zeroline: false,  visible: false },
    yaxis: { showgrid: false, zeroline: false, visible: false,  scaleanchor: "x" }
  };
  
  var config = { responsive: true }
  
  Plotly.newPlot( 'chart_area', data, layout, config );
};
