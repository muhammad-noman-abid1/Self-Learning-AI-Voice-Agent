import speech_recognition as sr


recognizer = sr.Recognizer()


def listen() -> str:
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        print("I couldn't understand that.")
        return ""

    except sr.RequestError as error:
        print(f"Speech recognition error: {error}")
        return ""


def wait_for_wake_word() -> None:
    while True:
        with sr.Microphone() as source:
            print("Waiting for wake word...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            text = text.lower()

            print(f"Heard: {text}")

            if "nom nom"  in text or "naam naam" in text or "ram ram"in text or "raam raam" in text: 
                print("Awaked!")
                return

        except sr.UnknownValueError:
            pass

        except sr.RequestError as error:
            print(f"Speech recognition error: {error}")