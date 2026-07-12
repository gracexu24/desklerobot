#chat generated test for voice
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
        """Convert spoken text into one of our program commands."""

        text = text.lower()

        if "stop" in text:
            return "stop"

        if "start" in text or "continue" in text:
            return "start"

        if "pick up trash" in text or "clean the desk" in text:
            return "trash"

        if "open gripper" in text:
            return "open_gripper"

        if "close gripper" in text:
            return "close_gripper"

        if "quit" in text or "exit" in text:
            return "quit"

        return None

    def _audio_callback(
        self,
        recognizer: sr.Recognizer,
        audio: sr.AudioData,
    ) -> None:
        """
        Runs in the background thread.

        Only recognize speech and place commands into the queue.
        Do not control the robot directly here.
        """

        try:
            text = recognizer.recognize_google(audio).lower()
            print(f"\n[Voice] Heard: {text}")

            command = self.parse_command(text)

            if command is not None:
                self.command_queue.put(command)
                print(f"[Voice] Command added to queue: {command}")
            else:
                print("[Voice] No matching command.")

        except sr.UnknownValueError:
            print("\n[Voice] Could not understand audio.")

        except sr.RequestError as error:
            print(f"\n[Voice] Recognition service error: {error}")

        except Exception as error:
            print(f"\n[Voice] Unexpected error: {error}")

    def start(self) -> None:
        """Calibrate the microphone and start background listening."""

        print("[Voice] Calibrating microphone...")
        print("[Voice] Stay quiet for one second.")

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

        print("[Voice] Background listener started.")

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

        print("[Voice] Background listener stopped.")


def test_command_parser() -> None:
    """Test command parsing without using the microphone."""

    test_phrases = [
        "stop",
        "please resume",
        "continue moving",
        "pick up trash",
        "clean the desk",
        "open gripper",
        "close gripper",
        "quit",
        "this is not a command",
    ]

    print("\n--- Testing command parser ---")

    for phrase in test_phrases:
        command = VoiceListener.parse_command(phrase)
        print(f"{phrase!r} -> {command}")

    print("--- Parser test finished ---\n")


def handle_command(command: str) -> bool:
    """
    Simulate handling a robot command.

    Returns False when the program should quit.
    """

    if command == "stop":
        print("[Main] TEST: Robot would stop.")

    elif command == "resume":
        print("[Main] TEST: Robot would resume.")

    elif command == "trash":
        print("[Main] TEST: Trash collection policy would start.")

    elif command == "open_gripper":
        print("[Main] TEST: Gripper would open.")

    elif command == "close_gripper":
        print("[Main] TEST: Gripper would close.")

    elif command == "quit":
        print("[Main] TEST: Quit command received.")
        return False

    else:
        print(f"[Main] Unknown command: {command}")

    return True


def main() -> None:
    # First test the parser using hard-coded sentences.
    test_command_parser()

    listener = VoiceListener()
    running = True

    print("Available voice commands:")
    print('  "stop"')
    print('  "resume" or "continue"')
    print('  "pick up trash" or "clean the desk"')
    print('  "open gripper"')
    print('  "close gripper"')
    print('  "quit" or "exit"')
    print()
    print("Press Ctrl+C to stop the program manually.")

    try:
        listener.start()

        while running:
            # Process all commands currently waiting in the queue.
            while True:
                command = listener.get_command()

                if command is None:
                    break

                running = handle_command(command)

                if not running:
                    break

            # Simulates the main robot loop continuing to run.
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n[Main] Keyboard interrupt received.")

    finally:
        listener.stop()
        print("[Main] Test finished.")


if __name__ == "__main__":
    main()