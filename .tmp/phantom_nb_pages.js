var page = require('webpage').create();
url = "https://www.scribd.com/doc/231257564/Rules-and-Guidance-for-Pharmaceutical-Manufacturers-and-Distributors-2007-Aka-the-Orange-Guide"
page.open(url, function () {
    console.log(page.content);
    phantom.exit();
});
// Avoid error messages
page.onError = function(msg, trace) {
};

