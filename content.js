function autoClick() {
    document.getElementById("Submit").click();

}
setTimeout(function () { addData(); }, 1500);
function addData() {
    try {
        var href = document.querySelector("#pano > div > div:nth-child(10) > div.gm-iv-address > div.gm-iv-address-link > a").getAttribute('href');
    } catch (err) {
        var href = "https://www.google.com/maps/@53.6827872,-1.5551093,3a,60y,84.35h,179t/data=!3m6!1e1!3m4!1s1TYhvXV80Wi1HVS9KPjIZg!2e0!7i13312!8i6656"
    }
    var textToSave;
    textToSave = String(href);

    chrome.runtime.sendMessage({
        message: textToSave
    }
        , function (response) {
            console.log(response.instruction);
            if (response.instruction == "Next") {
                document.getElementById("nextButton").click();
            }
        });
}