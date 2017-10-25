//https://stackoverflow.com/questions/32531881/retrieve-fully-populated-dynamic-content-with-phantomjs
//https://stackoverflow.com/questions/25288307/phantomjs-and-clicking-a-form-button

var page = require('webpage').create();

var loadInProgress = false;
var step_index = 0;

// Route "console.log()" calls from within the Page context to the main Phantom context (i.e. current "this")
page.onConsoleMessage = function(msg) {
    console.log(msg);
};

page.onAlert = function(msg) {
    console.log('alert!!> ' + msg);
};

page.onLoadStarted = function() {
    loadInProgress = true;
    console.log("load started");
};

page.onLoadFinished = function(status) {
    loadInProgress = false;
    if (status !== 'success') {
        console.log('Unable to access network');
        phantom.exit();
    } else {
        console.log("load finished");
    }
};

var steps = [
             function() {
                 console.log("Opening page");
                 page.open('https://uk.finance.yahoo.com/quote/AAPL?p=AAPL');
             },

             function() {
                 console.log("Clicking button");
                 //click 1 year
                 page.evaluate(function() {
                         var buttons = document.getElementsByTagName("button");
                         var search_text = "1y";
                         var found_button;

                         for (var i = 0; i < buttons.length; i++) {
                             if (buttons[i].textContent == search_text) {
                                 found_button = buttons[i];
                                 break;
                             }
                         }
                         found_button.click();
                     });
             },


             function() {
                 console.log("Rendering image");
                 page.render("out.png");
             }
             ];

interval = setInterval(function() {
        if (!loadInProgress && typeof steps[step_index] == "function") {
            console.log("step " + (step_index + 1));
            steps[step_index]();
            step_index++;
        }
        if (typeof steps[step_index] != "function") {
            console.log("All done!");
            phantom.exit();
        }
    }, 10000);
