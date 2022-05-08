

var keyword = ""

var data ={
    dataName1: "Gender",
    dataList1: ["Men: 60%", "Women: 30%", "Other: 20%"],
    image1: "graph.png",
    dataName2: "Another gender",
    dataList2: ["Men: 50%", "Women: 30%", "Other: 20%"],
    dataName3: "Country",
    dataList3: ["US: 50%", "UK: 30%", "Other: 20%"],

    //For the pie charts
    categoriesGender:["Men", "Women", "Other"],
    percentagesGender:[60, 30, 10],
    categoriesCountry:["US", "UK", "Other"],
    percentagesCountry:[30, 40, 30]

}

Chart.defaults.global.defaultFontFamily = 'Open Sans';
Chart.defaults.global.defaultFontSize = 10;
Chart.defaults.global.defaultFontColor = '#ffffff';
let barColors = [ "#D75D47", "#9DD65C", "#DCD15D"];


// Add fake data for now, 'myChartX' is the id of the new chart
addDataEntry("d1", data.dataName1, data.dataList1, 'myChart1', data.categoriesGender, data.percentagesGender);
addDataEntry("d2", data.dataName2, data.dataList2, 'myChart2', data.categoriesGender, data.percentagesGender);
addDataEntry("d3", data.dataName3, data.dataList3, 'myChart3', data.categoriesCountry, data.percentagesCountry);

var inputBox = document.getElementById("search");

//Get the keyword if the new word is entered into the input text-box
inputBox.addEventListener("keyup", function(event) {
    // Number 13 is the "Enter" key on the keyboard
    if (event.keyCode === 13) {
      // Cancel the default action, if needed
      event.preventDefault();
      // Trigger the button element with a click
      document.getElementById("searchButton").click();
    }
});

//Get the keyword
function getKeyword(){
    //Change the keyword to be the entered value
    keyword = inputBox.value;
    //Display as name of the first tweet to check if works
    document.querySelector("#s1").innerHTML = `<p>Lorem ipsum dolor sit</p><h4>${keyword}</h4>`;
}


//Add hyperlinks to most liked and shared twitter posts
function myhref(id){
    switch(id){
        //most shared
        case 's1': 
            window.open('https://twitter.com/elonmusk/status/1517707521343082496', '_blank');
            break;
        case 's2': 
            window.open('https://twitter.com/elonmusk/status/1517707521343082496', '_blank');
            break;
        case 's3': 
            window.open('https://twitter.com/elonmusk/status/1517707521343082496', '_blank');
            break;
        //most liked
        case 'l1': 
            window.open('https://twitter.com/elonmusk/status/1517707521343082496', '_blank');
            break;
        case 'l2': 
            window.open('https://twitter.com/elonmusk/status/1517707521343082496', '_blank');
            break;
        case 'l3': 
            window.open('https://twitter.com/elonmusk/status/1517707521343082496', '_blank');
            break;
        default: window.open('https://twitter.com/elonmusk/status/1517707521343082496', '_blank');
    }
}

//Update the content of each shown tweet, s is for shared and l for liked
function updateTweets(){
    document.querySelector("#s1").innerHTML = "<h2>Name</h2><p>Lorem ipsum dolor sit</p>";
    document.querySelector("#s2").innerHTML = "<h2>Name</h2><p>Lorem ipsum dolor sit</p>";
    document.querySelector("#s3").innerHTML = "<h2>Name</h2><p>Lorem ipsum dolor sit</p>";
    document.querySelector("#l1").innerHTML = "<h2>Name</h2><p>Lorem ipsum dolor sit</p>";
    document.querySelector("#l2").innerHTML = "<h2>Name</h2><p>Lorem ipsum dolor sit</p>";
    document.querySelector("#l3").innerHTML = "<h2>Name</h2><p>Lorem ipsum dolor sit</p>";
}

//Add a new data entry with the given id, name and data 
function addDataEntry(id, name, dataList, chartId, categories, percentages){
    //Create a new div element
    var div = document.createElement('div');
    //Add a class to inherit css style
    div.setAttribute('class', 'data');
    div.setAttribute('id', id);
    //Add the new element to the section with data
    document.querySelector('#section').appendChild(div);
    //Add the data and a graph/image
    createData(id, name, dataList);
    addGraph(id, chartId, categories, percentages);
}

//Add a new image next to the data (e.g. a graph)
function addGraph(id, canvasId, categories, percentages){
    var div = document.createElement('div');
    div.setAttribute('class', 'graph');
    document.querySelector(`#${id}`).appendChild(div);
    var canvas = document.createElement('canvas');
    canvas.id = canvasId;
    div.appendChild(canvas);
    generateGraph(canvasId, categories, percentages);
}

//Create a list inside data entry
function createData(id, name, dataList){
    //Create a div for the list 
    var div = document.createElement('div')
    document.querySelector(`#${id}`).appendChild(div);
    div.setAttribute('class', 'list');
    //Create a new ul and add it to the div
    var ul = document.createElement('ul');
    div.appendChild(ul);

    //Add name of the data list
    var li = document.createElement('li');
    ul.appendChild(li);
    li.innerHTML= `<h2> ${name} </h2>`;

    dataList.forEach(addDataItems);
    //Add the rest of the items
    function addDataItems(element) {
        var li = document.createElement('li');
        li.setAttribute('class','item');
        ul.appendChild(li);
        li.innerHTML=li.innerHTML + element;
    }
}

//Generate the chart with given id, categories and percentages
function generateGraph(canvasId, categories, percentages){
    let myChart = document.getElementById(canvasId);

    new Chart(myChart, {
        type: "pie",
        data: {
            //Given categories
            labels: categories,
            datasets: [{
                backgroundColor: barColors,
                //Given percentages
                data: percentages,
                borderWidth: 1,
                borderColor: "#244d64",
                hoverOffset: 10
            }]

        },
        options: {
            //Don't display the legend
            legend:{
                display: false,
                labels: {
                    fontColor: "#fff"
                }
            },
            //Display the little labels when hovering
            tooltips:{
                //Add '00' at the end to make transparent
                backgroundColor: '#000000',
                fontColor: '#000',
                titleColor: '#000'
            }
        }
    });

}

var spinnerWrapper = document.querySelector('.loader-wrapper');

window.addEventListener('load', function() {
    spinnerWrapper.style.display = 'none';
});

