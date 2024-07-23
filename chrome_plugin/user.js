document.getElementById('show-registration').addEventListener('click', function() {
    document.getElementById('intro').style.display = 'none';
    document.getElementById('make-note').style.display = 'none';
    document.getElementById('form').style.display = 'inline-block';
    document.getElementById('register-text').style.display = 'inline-block';
    document.getElementById('register-btn').style.display = 'inline-block';
    document.getElementById('back').style.display = 'inline-block';
    document.getElementById('form').reset();
});

document.getElementById('show-login').addEventListener('click', function() {
    document.getElementById('intro').style.display = 'none';
    document.getElementById('make-note').style.display = 'none';
    document.getElementById('form').style.display = 'inline-block';
    document.getElementById('login-text').style.display = 'inline-block';
    document.getElementById('login-btn').style.display = 'inline-block';
    document.getElementById('back').style.display = 'inline-block';
    document.getElementById('form').reset();
});

document.getElementById('back').addEventListener('click', function() {
    document.getElementById('intro').style.display = 'inline-block';
    document.getElementById('make-note').style.display = 'inline-block';
    homePage();
});

function homePage() {
    document.getElementById('register-text').style.display = 'none';
    document.getElementById('register-btn').style.display = 'none';
    document.getElementById('login-text').style.display = 'none';
    document.getElementById('login-btn').style.display = 'none';
    document.getElementById('form').style.display = 'none';
    document.getElementById('back').style.display = 'none';
    document.getElementById('form').reset();
    document.getElementById('response').textContent = '';
}

homePage()