document.getElementById('login-btn').addEventListener('click', loginPage);
document.getElementById('send-note-btn').addEventListener('click', saveText);


function isLogin() {
    chrome.storage.local.get(['jwtToken'], async (result) => {
        const token = result.jwtToken;
        if (!token) {
            document.getElementById('send-note-btn').style.display = 'none';
            document.getElementById('is-login').style.color = '#c30632';
            document.getElementById('is-login').textContent = 'Вход в аккаунт не выполнен';
            return;
        }

        await fetch('http://127.0.0.1:8080/api/v1/user/me', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`
            },
        })
        .then(async response => {
            return await response.json().then(data => ({ status: response.status, body: data }));
        })
        .then(({ status, body }) => {
            if (status == 200) {
                chrome.storage.local.get('savedText', (result) => {
                    if (result.savedText !== undefined) {
                        document.getElementById('note-text').value = result.savedText;
                    }
                });
                document.getElementById('login-btn').style.display = 'none';
                document.getElementById('is-login').color = '#white';
                document.getElementById('is-login').textContent = body.username;
            } else {
                chrome.storage.local.remove('jwtToken');
                document.getElementById('send-note-btn').style.display = 'none';
                document.getElementById('is-login').style.color = '#c30632';
                document.getElementById('is-login').textContent = 'Вход в аккаунт не выполнен';
            }
        })
    });
}

function saveText() {
    isLogin();

    chrome.storage.local.get(['jwtToken'], async (result) => {
        const token = result.jwtToken;
        if (!token) {
            chrome.storage.local.remove('jwtToken');
            document.getElementById('send-note-btn').style.display = 'none';
            document.getElementById('is-login').style.color = '#c30632';
            document.getElementById('is-login').textContent = 'Вход в аккаунт не выполнен';
            return;
        }

        const data = {
            title: document.getElementById('title').value,
            note_text: document.getElementById('note-text').value,
            comment: document.getElementById('comment').value,
        };

        await fetch('http://127.0.0.1:8080/api/v1/note', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(async response => {
            return await response.json().then(data => ({ status: response.status, body: data }));
        })
        .then(({ status, body }) => {
            if (status == 201) {
                chrome.storage.local.remove('savedText');
                document.getElementById('response').textContent = 'Отправлено!';
                document.getElementById('response').style.color = 'white';
                document.getElementById('note-text').value = '';
                document.getElementById('title').value = '';
                document.getElementById('comment').value = '';
            } else {
                document.getElementById('response').textContent = 'Ошибка: ' + body.detail;
                document.getElementById('response').style.color = '#c30632';
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
}

function loginPage() {
    window.location.href = 'popup.html';
}

isLogin();