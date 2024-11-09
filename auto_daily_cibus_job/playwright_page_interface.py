import time
from datetime import datetime
from playwright.sync_api import Playwright, sync_playwright, Page, expect, BrowserContext
from datetime import date


class PlaywrightPageInterface:
    _context: BrowserContext

    def __init__(self):
        self._context = None

    def page_init(self, headless):
        playwright = sync_playwright()
        self._context = playwright.start().chromium.launch(headless=headless).new_context()
        self._context.tracing.start(screenshots=True, snapshots=True, sources=True)
        return self._context.new_page()

    def save_trace(self, cibus_username, local_run=None):
        time_stamp = time.strftime("%Y%m%d_%H-%M")
        if local_run == "true":
            save_path = "./"
        else:
            save_path = "/auto_cibus/logs/"
        self._context.tracing.stop(
            path=save_path + f"traces/{cibus_username}/{cibus_username}_{time_stamp}trace.zip"
        )
        return True
