import Queue

import pyjulius

running = True
queue = Queue.Queue()
STOP_TOKEN = object()
wait_for_julius = False


def stop(recognizer):
    print "Stopping"
    global running
    running = False
    queue.put(STOP_TOKEN)
    recognizer.interrupt()


def recognize(playback, recognizer, data):
    playback.play_high_beep()

    print("Recognizing input...")

    try:
        text = str(recognizer.recognize(data))
        print("You said " + text)

        playback.play_tts(text)
    except LookupError as e:
        playback.play_low_beep()
        print(e.message)

    return True


def is_activated(julius):
    global wait_for_julius
    result = julius.client.results.get()

    if isinstance(result, pyjulius.Sentence):
        words = [word.word.encode("UTF-8") for word in result.words]

        if "GLADOS" in words:
            return True
        else:
            wait_for_julius = False
            print("Switching to passive...")

    return False


def start_listening(recognizer):
    while running:
        try:
            data = recognizer.listen()

            queue.put(data)
        except KeyboardInterrupt:
            break


def get_recorded():
    data = queue.get(True, 1000)

    if data is STOP_TOKEN:
        return STOP_TOKEN

    result = []

    while queue.qsize() > 0:
        get = queue.get(True, 1000)
        if get is STOP_TOKEN:
            return STOP_TOKEN
        result.append(get)

    result.insert(0, data)

    return "".join(result)


def start_passive_recognizing(playback, recognizer, julius):
    global wait_for_julius

    while running:
        try:

            # condition
            if not wait_for_julius:
                print("Recording for julius")
                data = get_recorded()
                if data is STOP_TOKEN:
                    break
                print("Sending audio to julius")
                julius.send_audio(data)
                wait_for_julius = True
            else:
                if is_activated(julius):
                    print("Waiting for input...")
                    data = get_recorded()
                    if data is STOP_TOKEN:
                        break

                    recognize(playback, recognizer, data)

                    wait_for_julius = False
                    print("Switching to passive...")

        except KeyboardInterrupt:
            break
