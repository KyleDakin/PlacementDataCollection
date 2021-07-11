chrome.runtime.onInstalled.addListener(function () {

    chrome.declarativeContent.onPageChanged.removeRules(undefined, function () {
        chrome.declarativeContent.onPageChanged.addRules([{
            conditions: [
                new chrome.declarativeContent.PageStateMatcher({
                    pageUrl: { urlContains: '127.0.0.1', urlContains: 'google.com/maps/*', },
                }),
            ],
            actions: [new chrome.declarativeContent.ShowPageAction()]
        }]);
    });
});

var baseTab = {
    tabInfo: null,
    get getter() {
        return this.tabInfo;
    },
    set setter(tabData) {
        this.tabInfo = tabData;
    }
};

var newTab = {
    tabInfo: null,
    get getter() {
        return this.tabInfo;
    },
    set setter(tabData) {
        this.tabInfo = tabData;
    }
};

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (baseTab.getter == null) {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            var currTab = tabs[0];
            if (currTab) {
                baseTab.setter = currTab;
            }
        });

    }
    if (newTab.getter == null) {
        chrome.tabs.create({ url: message.message }, function (tab) {
            newTab.setter = tab;
        });
    }
    else {
        chrome.tabs.update(newTab.getter.id, { url: message.message });

    }
    setTimeout(function () {
        sendResponse({ instruction: "Next" });
    }, 1500);


    return true;
})



