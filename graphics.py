import threading
import time

import pygame

from config import WINDOW_DIMENSION, WINDOW_UPDATE_PERIOD_MS, WINDOW_THREAD_NAME


class Window:

    def __init__(self):
        pygame.display.init()
        self.surface = pygame.display.set_mode(WINDOW_DIMENSION)

        self._stop_event = threading.Event()

        self.thread = threading.Thread(target=self._loop, name=WINDOW_THREAD_NAME)
        self.thread.start()

    def _loop(self):
        while True:

            if self._stop_event.is_set():
                break

            pygame.display.flip()
            time.sleep(WINDOW_UPDATE_PERIOD_MS)

        pygame.display.quit()

    def stop(self):
        self._stop_event.set()
