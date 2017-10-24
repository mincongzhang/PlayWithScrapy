//https://stackoverflow.com/questions/32531881/retrieve-fully-populated-dynamic-content-with-phantomjs
//PhantomJS required

var fs = require('fs');
var page = require('webpage').create();

page.open('https://uk.finance.yahoo.com/quote/AAPL?p=AAPL', function (status) {
        console.log("status: " + status);
        if (status !== "success") {
            console.log("Unable to access network");
        } else {
            window.setTimeout(function() {
                    page.render("out.png");
                    //fs.write('out.html', page.content, 'w');
                    phantom.exit();
                }, 10000); // adjust time for every page
        }
    });
