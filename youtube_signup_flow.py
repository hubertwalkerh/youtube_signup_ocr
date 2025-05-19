import time
import random
import ssl
import os

from clear_safari_app import clear_safari_data

ssl._create_default_https_context = ssl._create_unverified_context
import json
from dataclasses import asdict
from selenium.webdriver.common.by import By
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.keys import Keys
from ocr_utils import (find_text_and_tap,input_text,find_text_and_tap_with_index,wait_and_find_text_and_tap)
from Account import Account
from scroll_utils import (
    scroll_vertical_percentage
)



def signup_account(driver: WebDriver, udid: str):
    clear_safari_data(driver)
    account = Account.random(udid)
    time.sleep(5)
    # tap_at(driver, 500, 500)
    find_text_and_tap(driver, "sign in;Bạn", True)
    if find_text_and_tap(driver, "xong", True):
        find_text_and_tap(driver, "Bạn", True)
        
    wait_and_find_text_and_tap(driver, "Chuyển đổi tài khoản")
    wait_and_find_text_and_tap(driver, "Thêm tài khoản")
    wait_and_find_text_and_tap(driver, "Tiếp tục")
    wait_and_find_text_and_tap(driver, "Tạo tài khoản")
    wait_and_find_text_and_tap(driver, "Dành cho mục đích cá nhân của tôi")

    if find_text_and_tap(driver, "không bắt buộc", False):
        input_text(driver, account.last_name)

    if wait_and_find_text_and_tap(driver, "Tên"):
        input_text(driver, account.first_name,False, 1)

    wait_and_find_text_and_tap(driver, "Tiếp theo")

    if wait_and_find_text_and_tap(driver, "Ngày"):
        input_text(driver, random.randint(10,25),False,0)
    
    if find_text_and_tap(driver, "Tháng"):
        time.sleep(1)
        find_text_and_tap(driver, "Tháng "+ str(random.randint(1,5)))

    if find_text_and_tap(driver, "Năm"):
        time.sleep(1)
        input_text(driver,  random.randint(1990,1999),False,1)

    if find_text_and_tap(driver, "Giới tính"):
        if account.gender == "Nam":
            time.sleep(1)
            find_text_and_tap_with_index(driver, account.gender, 1, True)
        else:
            time.sleep(1)
            find_text_and_tap(driver, account.gender)

    wait_and_find_text_and_tap(driver, "Tiếp theo")

    # find_text_and_tap(driver, "Tiếp theo")

    if wait_and_find_text_and_tap(driver, "địa chỉ Gmail của riêng bạn", False):
        #input_text(driver, f"john{int(time.time())}abc")
        input_text(driver, f"{account.username}")
        find_text_and_tap(driver, "Tiếp theo")
    elif wait_and_find_text_and_tap(driver, "Tên người", False):
        #input_text(driver, f"john{int(time.time())}abc")
        input_text(driver, f"{account.username}")
        find_text_and_tap(driver, "Tiếp theo")
    
    if find_text_and_tap(driver, "đã sử dụng", False):
        #input_text(driver, f"john{int(time.time())}abc")
        input_text(driver, f"{account.username}12", True)
        account.username = account.username + "12"
        find_text_and_tap(driver, "Tiếp theo")

    if wait_and_find_text_and_tap(driver, "Mật khẩu"):
        input_text(driver, f"{account.password}")

    # if find_text_and_tap(driver, "Xác nhận"):
    #     input_text(driver, f"{account.password}", True, 1)

    wait_and_find_text_and_tap(driver, "Tiếp theo")
    isRegisterAccountSuccess = False

    if find_text_and_tap(driver, "Xác minh số này", False):
        print("Tao tai khoản thất bại bị xác minh số điện thoại")
        save_account_to_file_json(account, fileNameSave="account_gmail_error")
        return

    if find_text_and_tap(driver, "Xem lại thông tin tài", False):
        print("Tao tai khoản thành công")
        find_text_and_tap(driver, "Tiếp theo")
        scroll_vertical_percentage(driver)
        scroll_vertical_percentage(driver)
        scroll_vertical_percentage(driver)
        scroll_vertical_percentage(driver)
        wait_and_find_text_and_tap(driver, "Tôi đồng ý")
        isRegisterAccountSuccess = True
        save_account_to_file_json(account, fileNameSave="account_gmail_success")

    if isRegisterAccountSuccess :
        print("Tao tai khoản thành công tiến hành tạo kênh và lướt video Short")
        wait_and_find_text_and_tap(driver, "Trang chủ")
        wait_and_find_text_and_tap(driver, "Bạn")
        wait_and_find_text_and_tap(driver, "Tạo kênh")
        wait_and_find_text_and_tap(driver, "Tạo kênh")
        wait_and_find_text_and_tap(driver, "Shorts")
        for _ in range(random.randint(4,10)):
            scroll_vertical_percentage(driver)
            time.sleep(random.randint(5,20))
        print("Đã lướt xong video short nuôi dưỡng")
        driver.execute_script("mobile: pressButton", {"name": "home"})

        

    print("[INFO] Completed input phase. Bạn cần xác minh số điện thoại thủ công nếu có.")

def save_account_to_file_json(account: Account, fileNameSave: str, file_path=None):
    if file_path is None:
        file_path = os.path.join(os.path.expanduser("~"), "Desktop", f"{fileNameSave}.json")
    
    accounts = []
    
    # Đọc file nếu tồn tại
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                accounts = json.load(f)
            except json.JSONDecodeError:
                # File trống hoặc lỗi, khởi tạo lại list rỗng
                accounts = []
    
    # Thêm account mới vào list
    accounts.append(asdict(account))
    
    # Ghi lại toàn bộ mảng accounts ra file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(accounts, f, ensure_ascii=False, indent=2)