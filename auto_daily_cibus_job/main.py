import time
from datetime import date
import datetime
import os

from playwright.sync_api import Playwright, sync_playwright, Page, expect


# WILL ONLY RUN BETWEEN SUNDAY AND THURSDAY

# CIBUS_USERNAME (cibus email)
# CIBUS_PASSWORD
# LIVE=true/false (if wanting to go with purchase or no
# PRICE_OF_COUPON (an int of the price of coupon you want to buy)



# TODO check worker schedule in sela
# TODO change so it won't run on the 1st of every month? (handle cases where there are previous orders at all?

# TODO add logging to a db (to know when and how it saved money)


def check_if_workday():
    # TODO: move to using global date and not by system (to avoid unexpected behaviour when on different TZs)
    week_day = date.today().weekday()  # 0-monday --- 6-sunday
    if week_day == 4 or week_day == 5:
        return False
    else:
        return True


def validate_env_vars():
    if not os.getenv("LINK_TO_COUPON"):
        raise Exception("You have to set '-e LINK_TO_COUPON=<str>")
    if not os.getenv("PRICE_OF_COUPON"):
        raise Exception("You have to set '-e PRICE_OF_COUPON=<int>")
    price_input_verification(os.getenv("PRICE_OF_COUPON"))
    if not os.getenv("CIBUS_USERNAME"):
        raise Exception("You have to set '-e CIBUS_USERNAME=<email>")
    if not os.getenv("CIBUS_PASSWORD"):
        raise Exception("You have to set '-e CIBUS_PASSWORD=<password>")


def price_input_verification(price_input):
    try:
        int(price_input)
    except ValueError:
        raise ValueError(f"""
        The price that was input is incorrect. please make sure it's an int.
        Correct:
            '15'/'30'/'40'
        Incorrect:
            '15.00'/'₪30'
        Your input was:
            {price_input}
        """)


class CibusInterface:
    def __init__(self, page: Page):
        self._page = page
        self._today = date.today()
        self._today_date = self._today.strftime("%d/%m/%Y")

    def login(self, username, password):
        self._page.goto("https://consumers.pluxee.co.il/login")
        self._page.wait_for_load_state(state="networkidle")
        self._page.get_by_label("מייל/מס' נייד/שם משתמש").fill(f"{username}")
        self._page.get_by_label("מייל/מס' נייד/שם משתמש").press("Enter")
        self._page.get_by_label("מה הסיסמה?").fill(f"{password}")
        self._page.get_by_label("מה הסיסמה?").press("Enter")

    def check_if_was_used_today(self):
        self._page.goto("https://consumers.pluxee.co.il/user/orders")
        time.sleep(3)
        self._page.screenshot(path="/tracing/screenshots/default_orders_page.png")
        self._page.get_by_role("button", name="Open calendar").click()
        self._page.get_by_role("button", name="היום").click()
        time.sleep(2)
        self._page.screenshot(path="/tracing/screenshots/today_orders_page.png")
        calendar_date_from_to = self._page.locator(".mat-form-field-flex")
        starting_date = calendar_date_from_to.locator(".mat-date-range-input-mirror").all()[1]
        expect(starting_date).to_contain_text(self._today_date)


        if starting_date.inner_text() == self._today_date and self._page.locator("app-dynamic-table").inner_text() == "לא נמצאו נתונים":
            return False
        else:
            page_history = self._page.get_by_text("פירוט עסקאותבחר טווח תאריכים")
            page_row = page_history.get_by_role("row").all()
            last_order_date = page_row[1].get_by_role("cell").all()[1].inner_text()
            last_order_date_clean = last_order_date[1:-1]
            if last_order_date_clean == self._today_date:
                return True
            else:
                raise Exception("Something is sus...")

    def order_by_link(self, link_to_coupon, price_of_coupon, live="false"):
        self._page.goto(link_to_coupon)
        time.sleep(3)
        all_order_options = self._page.locator("app-rest-menu-card").all()
        for order_option in all_order_options:
            if len(order_option.get_by_text(f"₪{price_of_coupon}.00").all()) > 0:
                order_option.get_by_role(role="button").click()
                time.sleep(2)
                self.pre_order_and_checkout(live=live)
                break

    def pre_order_and_checkout(self, live="false"):
        self._page.goto("https://consumers.pluxee.co.il/restaurants/pickup/preorder")
        self._page.wait_for_load_state()  # state="networkidle"
        time.sleep(1)
        time.sleep(5)
        if live == "true":
            self._page.get_by_role("button", name="אישור ההזמנה").click()
            time.sleep(3)
            print("purchased")


def main():
    validate_env_vars()
    if check_if_workday():
        exit(1)

    link_to_coupon = os.getenv("LINK_TO_COUPON")
    price_of_coupon = os.getenv("PRICE_OF_COUPON")
    cibus_username = os.getenv("CIBUS_USERNAME")
    cibus_password = os.getenv("CIBUS_PASSWORD")
    is_live = os.getenv("LIVE")
    headless = False if os.getenv("HEADLESS") == "false" else True

    # try:
    playwright = sync_playwright()
    context = playwright.start().chromium.launch(headless=headless).new_context()
    # context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    cibus_interface = CibusInterface(page=page)
    cibus_interface.login(
        username=cibus_username,
        password=cibus_password
    )

    time.sleep(3)

    # TODO find better way to exit
    if cibus_interface.check_if_was_used_today():
        raise Exception("""The cibus was used today!""")
    else:
        cibus_interface.order_by_link(link_to_coupon=link_to_coupon, price_of_coupon=price_of_coupon, live=is_live)
        # else:
        #     cibus_interface.order_same_as_last_cibus(live=is_live)
    # except:
    #     print(os.getcwd())
    #     print("stoping trace")
    #     context.tracing.stop(path="/tracing/trace.zip")


if __name__ == '__main__':
    main()

