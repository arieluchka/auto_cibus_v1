from playwright.sync_api import Playwright, sync_playwright, Page, expect, Selectors
import time
from datetime import date
from auto_wolt.data.wolt_page import WoltPage

# cookies: Sequence[{name: str, value: str, url: Union[str, None], domain: Union[str, None], path: Union[str, None],
#                    expires: Union[float, None], httpOnly: Union[bool, None], secure: Union[bool, None],
#                    sameSite: Union["Lax", "None", "Strict", None]}]


class WoltInterface:
    def __init__(self, playwright:Playwright, wrtoken, wtoken):
        self._home_page = "https://wolt.com/en/discovery"
        self.__wrtoken = {
            "name": "__wrtoken",
            "value": wrtoken,
            "domain": "wolt.com",
            "path": "/",
            "httpOnly": False,
            "secure": True
        }

        self.__wtoken = {
            "name": "__wtoken",
            "value": wtoken,
            "domain": "wolt.com",
            "path": "/",
            "httpOnly": False,
            "secure": True
        }

        self.__playwright = playwright
        self._context = self.__context_init(playwright=self.__playwright)
        self.wolt_page = WoltPage(self._context.new_page())

    def __context_init(self, playwright: Playwright):
        playwright.selectors.set_test_id_attribute(attribute_name="data-test-id")
        context = playwright.chromium.launch(headless=False).new_context()
        context.add_cookies([self.__wtoken, self.__wrtoken])
        return context

    def check_clear_cart(self):
        self.wolt_page.page.goto("https://wolt.com/en/discovery")
        self.wolt_page.page.wait_for_load_state()  # state="networkidle"
        time.sleep(4)
        try:
            expect(self.wolt_page.cart_button_count).not_to_be_visible()
            print("cart appears empty")
            return True
        except AssertionError:
            print(f"cart is not clean and has {self.wolt_page.cart_button_count.inner_text()} items")
            self.wolt_page.cart_button.click()
            self.wolt_page.cart_edit_button.click()
            self.wolt_page.cart_select_all_button.click()
            self.wolt_page.cart_delete_button.click()
            self.wolt_page.cart_start_shopping.click()

            time.sleep(3)
            if self.check_clear_cart():
                return True

    def add_gift_cards(self, gift_card_sum: int):
        self.wolt_page.page.goto("https://wolt.com/en/isr/tel-aviv/venue/woltilgiftcards")
        time.sleep(5)
        gift_card_dict = self.wolt_page.gift_card_dict_by_price()
        gift_card_dict[gift_card_sum].click()
        time.sleep(1)
        self.wolt_page.add_to_order.click()
        time.sleep(3)

    def checkout(self):
        self.wolt_page.page.goto("https://wolt.com/en/isr/tel-aviv/venue/woltilgiftcards/checkout")
        time.sleep(30)

        # TODO ADD VALIDATION THAT SCRIPT IS USING CIBUS!!!

        # carefull with uncommenting! could finish purchase
        # self.wolt_page.send_order.click()
        # time.sleep(5)
        # self.wolt_page.cibus_username_field.fill("ariel.agra@gmail.com")
        # self.wolt_page.cibus_password_field.fill("ArieLCibuS!123")
        # time.sleep(4)


if __name__ == '__main__':
    from auto_wolt.data.wolt_tokens import wolt_tokens
    with sync_playwright() as playwright:

        wolt = WoltInterface(
            playwright=playwright,
            wrtoken=wolt_tokens["wrtoken"],
            wtoken=wolt_tokens["wtoken"]
        )

        wolt.check_clear_cart()
        print("cart is clear")
        wolt.add_gift_cards(30)
        print("added gift cards")
        time.sleep(3)
        wolt.checkout()
