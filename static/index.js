google.charts.load('current', {
    'packages': ['geochart'],
    // Note: you will need to get a mapsApiKey for your project.
    // See: https://developers.google.com/chart/interactive/docs/basic_load_libs#load-settings
    'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
});

google.charts.setOnLoadCallback(drawRegionsMap);

function drawRegionsMap() {
    var data = google.visualization.arrayToDataTable([
        ['Country', 'Greenness'],
        ['Australia', 200]
    ]);

    var options = {};

    var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));

    chart.draw(data, options);
}


google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    var data = google.visualization.arrayToDataTable([
        ['Energy Type', 'kWh'],
        ['Fossil Fuel',     11],
        ['Solar',      2],
        ['Wind',  2],
        ['Hydro', 2],
        ['Nuclear',    7]
    ]);

    var options = {
        title: 'Energy Mix'
    };

    var chart = new google.visualization.PieChart(document.getElementById('piechart'));
chart.draw(data, options);
}