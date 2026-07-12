#how does timing work for this? how do I keep it running in the backgroud? 

#setup microphone and such 

#call speech to text (buffer, how should this work?)
#parse through text 
# detect text and return command if exists 

import queue
import time
import speech_recognition as sr

class VoiceListener:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Safely passes commands from the voice thread to the main thread.
        self.command_queue: queue.Queue[str] = queue.Queue()
        self.stop_background_listening = None

    @staticmethod
    def parse_command(text: str) -> str | None:
        text = text.lower()
        if "stop" in text:
            return "stop"
        if "reset" in text or "continue" in text:
            return "reset"
        if "pick up trash" in text or "clean the desk" in text:
            return "trash"
        return None

    def _audio_callback(self, recognizer: sr.Recognizer, audio: sr.AudioData,
    ) -> None:
        """
        Runs in the background thread.

        Only recognize speech and place commands into the queue.
        Do not control the robot directly here.
        """
        try:
            #speach to text - needs wifi 
            text = recognizer.recognize_google(audio).lower()
            print(f"\nHeard: {text}")
            command = self.parse_command(text)

            if command is not None:
                self.command_queue.put(command)
                print(f"Command added to queue: {command}")
            else:
                print("No matching command.")

        except sr.UnknownValueError:
            print("\nCould not understand audio.")
        except sr.RequestError as error:
            print(f"\nRecognition service error: {error}")
        except Exception as error:
            print(f"\nUnexpected error: {error}")

    def start(self) -> None:
        """Calibrate the microphone and start background listening."""

        print("microphone set up") 

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=1,
            )

        self.stop_background_listening = (
            self.recognizer.listen_in_background(
                self.microphone,
                self._audio_callback,
                phrase_time_limit=4,
            )
        )

        print("Background listener started.")

    def get_command(self) -> str | None:
        """Return the next command without blocking the main loop."""
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None

    def stop(self) -> None:
        """Stop background microphone listening."""
        if self.stop_background_listening is not None:
            self.stop_background_listening(wait_for_stop=True)
            self.stop_background_listening = None

        print("Background listener stopped.")