      google.charts.load('current', {'packages':['treemap']});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Category', 'Parent', 'Products in subtree', 'Products in category'],
        ]);

        tree = new google.visualization.TreeMap(document.getElementById('chart_div'));

        tree.draw(data, {
          minColor: '#8da',
          midColor: '#8da',
          maxColor: '#8da',
          headerHeight: 15,
          fontColor: 'black',
          generateTooltip: showFullTooltip
        });
        function showFullTooltip(row, size, value) {
        	return '<div style="background:#fd9; padding:10px; border-style:solid">' +
           '<span style="font-family:Courier"><b>' + data.getValue(row, 0)+ '</span><br>' +
            data.getColumnLabel(2) + ': ' + size + ' </div>';

      }
 }