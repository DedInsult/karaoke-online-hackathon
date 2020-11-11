import os.path
import random


def generate_song_name(obj, file_data):
    return str(random.getrandbits(32)) + '.mp3'

def spanify_text(song):
    stroki = song.lyrics.split("\n")

    text = []
    counter = 0
    for stroka in stroki:
        stroka_texta = []

        slova = stroka.split(' ')

        for slovo in slova:
            counter += 1
            stroka_texta.append(f'<span id={counter}>{slovo}</span>')

        text.append(' '.join(stroka_texta))

    return '\n'.join(text)