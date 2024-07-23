document.getElementById('register-btn').addEventListener('click', register);
document.getElementById('login-btn').addEventListener('click', login);
document.getElementById('make-note').addEventListener('click', notePage);

async function register() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    await fetch('http://127.0.0.1:8080/api/v1/user/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(async response => {
        return await response.json().then(data => ({ status: response.status, body: data }));
    })
    .then(({ status, body }) => {
        document.getElementById('response').textContent = ''
        document.getElementById('response').style.color = '#c30632';
        switch(status) {
            case 201:
                document.getElementById('response').textContent = 'Успешная регистрация!';
                document.getElementById('response').style.color = 'white';
                break;
            case 400:
                document.getElementById('response').textContent = body.detail;
                break;
            case 422:
                if (body.detail && body.detail.length > 0) {
                    document.getElementById('response').textContent = 'Ошибка: ' + body.detail[0].loc[1] + " " + body.detail[0].msg;
                } else {
                    document.getElementById('response').textContent = 'Ошибка: Некорректный запрос';
                }
                break;
            case 500:
                document.getElementById('response').textContent = 'Ошибка: Внутренняя ошибка сервера';
                break;
            default:
                document.getElementById('response').textContent = 'Ошибка: Что-то пошло не так. Status: ' + status;
        }
    })
    .catch(error => {
        document.getElementById('response').textContent = 'Ошибка: ' + error.message;
    });
}

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    const data = new URLSearchParams();
    data.append('username', username);
    data.append('password', password);
    
    try {
        const response = await fetch('http://127.0.0.1:8080/api/v1/user/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: data
        });
    
        const responseData = await response.json();

        document.getElementById('response').textContent = ''
        document.getElementById('response').style.color = '#c30632';
        switch(response.status) {
            case 200:
                document.getElementById('response').textContent = 'Успешный вход!';
                document.getElementById('response').style.color = 'white';
                chrome.storage.local.set({ jwtToken: responseData.access_token });
                break;
            case 401:
                document.getElementById('response').textContent = responseData.detail;
                break;
            default:
                document.getElementById('response').textContent = 'Ошибка: Что-то пошло не так. Status: ' + response.status;
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Login failed');
    }
}
  
function notePage() {
    window.location.href = 'note.html';
}