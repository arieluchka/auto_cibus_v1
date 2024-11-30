from typing import Dict

from playwright.sync_api import Page, Locator


class WoltPage:
    def __init__(self, page: Page):
        self.page = page

        # main page
        self.cart_button = self.page.get_by_test_id("visible-baskets.shopping-cart-button")
        self.cart_button_count = self.page.get_by_test_id("visible-baskets.shopping-cart-button-count")
        self.cart_edit_button = self.page.get_by_test_id("visible-baskets.edit-mode-button")
        self.cart_select_all_button = self.page.get_by_test_id("visible-baskets.select-unselect-all-button")
        self.cart_delete_button = self.page.get_by_test_id("visible-baskets.cta-confirm-delete")
        self.cart_start_shopping = self.page.get_by_test_id("visible-baskets.shopping-cart-start-shopping-button")


        # gift card page
        self.menu_sec = self.page.get_by_test_id("MenuSection")
        self.item_card_price = "horizontal-item-card-price"

        self.item_add_quantity = self.page.get_by_test_id("product-modal.quantity.increment")
        self.item_remove_quantity = self.page.get_by_test_id("product-modal.quantity.decrement")
        self.item_quantity_count = self.page.get_by_test_id("product-modal.quantity.value")
        self.item_summ_price = self.page.get_by_test_id("product-modal.total-price")
        self.add_to_order = self.page.get_by_test_id("product-modal.submit")

        # checkout
        self.payment_method_button = self.page.get_by_test_id("PaymentMethods.SelectedPaymentMethod")
        self.cibus_warning_message = self.page.get_by_test_id("In selecting Cibus, you agree that any refunds will be received as Wolt Credits (rather than a refund to your Cibus account or a money refund).")

        self.total_price = self.page.get_by_test_id("PriceTotalRow")
        self.send_order = self.page.get_by_test_id("SendOrderButton")

        # cibus overlay
        self.cibus_username_field = self.page.get_by_placeholder("שם משתמש")
        self.cibus_password_field = self.page.get_by_placeholder("סיסמה")

    @property
    def all_items_in_menu(self):
        return self.menu_sec.get_by_test_id("horizontal-item-card").all()

    def gift_card_dict_by_price(self) -> dict[int, Locator]:
        gift_card_items = self.all_items_in_menu
        gift_card_dict = {}
        for gift_card in gift_card_items:
            price = int(gift_card.get_by_test_id(self.item_card_price).inner_text()[1:].split(".")[0].replace(",", ""))
            gift_card_dict[price] = gift_card

        return gift_card_dict
