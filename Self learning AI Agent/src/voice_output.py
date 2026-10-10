import re
import subprocess
import sys


def clean_for_speech(text: str) -> str:
    """
    Remove Markdown formatting before sending text to the speaker.
    """

    # Remove horizontal separators such as ---
    text = re.sub(r"^\s*-{3,}\s*$", "", text, flags=re.MULTILINE)

    # Remove Markdown headings: #, ##, ###
    text = re.sub(r"^\s*#{1,6}\s*", "", text, flags=re.MULTILINE)

    # Remove bold and italic markers: **text**, *text*
    text = text.replace("**", "")
    text = text.replace("*", "")

    # Remove bullet-point dashes at the beginning of lines
    text = re.sub(r"^\s*-\s+", "", text, flags=re.MULTILINE)

    # Remove unnecessary Markdown backticks
    text = text.replace("```", "")
    text = text.replace("`", "")

    # Clean excessive blank lines
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


def speak(text: str) -> None:
    text = clean_for_speech(text)

    if not text:
        return

    script = f"""
import pyttsx3

engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

engine.say({text!r})
engine.runAndWait()
engine.stop()
"""

    subprocess.run(
        [sys.executable, "-c", script],
        check=True,
    )