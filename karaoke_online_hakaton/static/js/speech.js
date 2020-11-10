

window.addEventListener('load', function () {
    window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    let state = false;
    recognition.lang = 'ru-RU';
    recognition.continuous = true;

    let song = document.querySelector('#song');
    let startStop = document.querySelector('#startStop');
    let scoreTracker = document.querySelector('#scoreTracker');

    startStop.addEventListener('click', () => {
        if (state == false) {
            song.play();
            recognition.start();
            startStop.innerHTML = 'Pause';
            state = true;
        } else {
            song.pause();
            recognition.stop();
            startStop.innerHTML = 'Resume';
            state = false;
        }
    });

    let original_text = document.querySelector('#original-lyrics').innerHTML;

    original_text = original_text.replace(/\n|\r|,|\./g, ' ')
        .toLowerCase()
        .replace(/ё/g, 'е');
    let original_words = original_text.split(' ');

    let userLyrics = '';


    let text = document.querySelector('#text');
    recognition.addEventListener('result', e => {
        userLyrics += e.results[e.resultIndex][0].transcript
            .replace(/ё/g, 'е')
            .toLowerCase();

        words_count = (userLyrics.match(/ /g) || []).length + 1;

        original_text_chunk = original_words.slice(0, words_count).join(' ');
        scoreTracker.innerHTML = 'Your current score: ' + Math.round(similarity(userLyrics, original_text_chunk) * 100) +'%';

    });
});

