

window.addEventListener('load', function () {
    window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    let state = false;
    // change the lang depending on the song
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

        let userLyricsList = userLyrics.split(' ');

        // Lyrics highlighter
        for (let i = 0; i < words_count; i++) {
            let word = document.getElementById(i + 1);

            let target = word.innerHTML.toLowerCase().replace(/ё/g, 'е').replace(',', '')

            if (target.trim() == userLyricsList[i].trim()) {
                word.classList.add('bg-success')
            } else {
                word.classList.add('bg-warning')
            }

        }

        original_text_chunk = original_words.slice(0, words_count);
        scoreTracker.innerHTML = `Your current score: ${Math.round(similarity(userLyricsList, original_text_chunk))}%`
    });
});

