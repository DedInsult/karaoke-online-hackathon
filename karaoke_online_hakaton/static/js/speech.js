window.addEventListener('load', function () {
    window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.lang = 'ru-RU';
    recognition.continuous = true;

    let start = document.querySelector('#start');
    let stop = document.querySelector('#stop');

    start.addEventListener('click', () => {
        recognition.start();

    });

    stop.addEventListener('click', () => {
        recognition.stop();
    });

    let userLyrics = '';
    let text = document.querySelector('#text');
    recognition.addEventListener('result', e => {
        console.log(e)
        userLyrics += e.results[e.resultIndex][0].transcript + '<br>';
        text.innerHTML = userLyrics;
    });



});

