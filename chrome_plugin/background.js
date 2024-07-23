chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: "saveText",
        title: "Save Text",
        contexts: ["selection"]
    });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "saveText" && info.selectionText) {
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: saveText,
            args: [info.selectionText]
        });
    }
});

function saveText(selectedText) {
    chrome.storage.local.get(['jwtToken'], (result) => {
        const token = result.jwtToken;
        if (!token) {
            console.error("No JWT token found in storage");
            return;
        }

        const data = {
            title: "Title of your note",
            note_text: selectedText
        };

        fetch('http://127.0.0.1:8080/api/v1/note', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
}