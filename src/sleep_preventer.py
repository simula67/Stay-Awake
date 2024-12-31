import threading
import pyautogui
import time
import logging
import os


class SleepPreventer:
    def __init__(self, method='volume_toggle', interval=5):
        """
        Initialize the SleepPreventer object.

        Args:
            method (str): The method to prevent sleep ('volume_toggle', 'mouse_move', 'no_op', 'key_press').
            interval (int): Interval between actions in seconds.
        """
        self.method = method.lower()
        self.interval = interval
        self.running = False
        self.thread = None

        # Set up logging
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Validate method
        if self.method not in ['volume_toggle', 'mouse_move', 'no_op', 'key_press']:
            logging.error(
                "Invalid method specified. Supported methods: 'volume_toggle', 'mouse_move', 'no_op', 'key_press'.")
            raise ValueError("Invalid method. Supported methods: 'volume_toggle', 'mouse_move', 'no_op', 'key_press'.")

        logging.info(f"SleepPreventer initialized with method '{self.method}' and interval {self.interval}s.")

    def _volume_toggle(self):
        """
        Simulate volume key presses to prevent sleep.
        """
        pyautogui.press('volumedown')
        logging.debug("Volume down pressed.")
        time.sleep(1)
        pyautogui.press('volumeup')
        logging.debug("Volume up pressed.")

    def _mouse_move(self):
        """
        Simulate mouse movement to prevent sleep.
        """
        pyautogui.move(10, 0)
        logging.debug("Mouse moved right.")
        time.sleep(1)
        pyautogui.move(-10, 0)
        logging.debug("Mouse moved left.")

    def _key_press(self):
        """
        Simulate a harmless key press to prevent sleep.
        """
        pyautogui.press('F13')
        logging.debug("F13 key pressed.")

    def _no_op(self):
        """
        Perform a no-operation action (useful for testing or placeholder).
        """
        logging.debug("No-op method executed.")

    def _prevent_sleep(self):
        """
        Perform the sleep prevention action in a loop.
        """
        try:
            while self.running:
                if self.method == 'volume_toggle':
                    self._volume_toggle()
                elif self.method == 'mouse_move':
                    self._mouse_move()
                elif self.method == 'key_press':
                    self._key_press()
                elif self.method == 'no_op':
                    self._no_op()

                time.sleep(self.interval)
        except Exception as e:
            logging.error(f"An error occurred during sleep prevention: {e}")
            self.running = False

    def start_sleep_prevention(self):
        """
        Start the sleep prevention in a background thread.
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._prevent_sleep, daemon=True)
            self.thread.start()
            logging.info("SleepPreventer started.")
        else:
            logging.warning("SleepPreventer is already running.")

    def stop_sleep_prevention(self):
        """
        Stop the sleep prevention.
        """
        if self.running:
            self.running = False
            if self.thread is not None:
                self.thread.join()
            logging.info("SleepPreventer stopped.")
        else:
            logging.warning("SleepPreventer is not running.")

    def set_method(self, method):
        """
        Set the sleep prevention method.

        Args:
            method (str): The new method ('volume_toggle', 'mouse_move', 'no_op', 'key_press').
        """
        if method.lower() not in ['volume_toggle', 'mouse_move', 'no_op', 'key_press']:
            logging.error(
                "Invalid method specified. Supported methods: 'volume_toggle', 'mouse_move', 'no_op', 'key_press'.")
            raise ValueError("Invalid method. Supported methods: 'volume_toggle', 'mouse_move', 'no_op', 'key_press'.")

        self.method = method.lower()
        logging.info(f"Sleep prevention method updated to '{self.method}'.")

    def set_interval(self, interval):
        """
        Set the interval between actions.

        Args:
            interval (int): The new interval in seconds.
        """
        if interval <= 0:
            logging.error("Interval must be greater than zero.")
            raise ValueError("Interval must be greater than zero.")

        self.interval = interval
        logging.info(f"Interval updated to {self.interval}s.")


# Example usage:
if __name__ == "__main__":
    sp = None
    try:
        sp = SleepPreventer(method='key_press', interval=5)
        sp.start_sleep_prevention()
        iteration_count = 1
        while True:
            logging.info(f'Iteration count {iteration_count}')
            time.sleep(5)
            iteration_count += 1
    except KeyboardInterrupt:
        logging.info("Interrupted by user. Stopping SleepPreventer.")
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
    finally:
        sp.stop_sleep_prevention()
