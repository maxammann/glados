import Queue
import pyjulius
import time

running = True

passive = True


def wakeup(playback, recognizer):
    global passive

    passive = False
    print("Detected wake up")
    playback.play_high_beep()

    time.sleep(0.5)
    print("Waiting for input")

    data = recognizer.listen()

    try:
        text = str(recognizer.recognize(data))
        print("You said " + text)

        playback.play_low_beep()

        playback.play_tts(text)
    except LookupError as e:
        print e.message

    passive = True


def loop(playback, recognizer, julius):
    try:
        result = julius.client.results.get(timeout=1)
    except Queue.Empty:
        return

    if isinstance(result, pyjulius.Sentence):
        words = [word.word.encode("UTF-8") for word in result.words]

        if "GLADOS" in words:
            wakeup(playback, recognizer)


def start_passive_listening(recognizer, julius):
    while running:
        try:
            if passive:
                data = recognizer.listen()
                julius.send_audio(data)
            time.sleep(0.1)
        except KeyboardInterrupt:
            break


def start_passive_recognizing(playback, recognizer, julius):
    while running:
        try:
            loop(playback, recognizer, julius)
        except KeyboardInterrupt:
            break
