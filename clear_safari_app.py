import time
from appium.webdriver.common.appiumby import AppiumBy
from ocr_utils import (find_text_and_tap,
            find_text_and_tap_with_index)
from scroll_utils import scroll_vertical_percentage

def open_app(driver, bundleId:str, nameApp: str):
    f"""
    Mở ứng dụng Cài đặt {nameApp} bằng driver đã có sẵn.
    Yêu cầu: driver đã được khởi tạo với Appium và có quyền thực hiện mobile:launchApp.
    """
    #"com.apple.Preferences"
    try:
        driver.execute_script("mobile: launchApp", {"bundleId": bundleId})
        print(f"✅ Đã mở ứng dụng {nameApp}.")
    except Exception as e:
        print(f"❌ Lỗi khi mở {nameApp}: {e}")

def set_airplane_mode(driver, enable: bool):
    switches = driver.find_elements(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeSwitch')
    if not switches:
        print("[Error] Không tìm thấy switch")
        return

    airplane_switch = switches[0]  # giả định đầu tiên là switch của máy bay
    current_value = airplane_switch.get_attribute("value")  # "1" hoặc "0"
    print("[Status] Airplane mode hiện tại:", current_value)

    if (enable and current_value == "0") or (not enable and current_value == "1"):
        airplane_switch.click()
        print(f"[Action] Đã {'bật' if enable else 'tắt'} chế độ máy bay.")
    else:
        print("[Action] Trạng thái đã đúng, không cần thay đổi.")

def clear_safari_data(driver):
    open_app(driver,"com.apple.Preferences", "Settings")
    time.sleep(4)
    set_airplane_mode(driver, True)
    isHaveApplication = False
    print("[Safari] Đang tìm Ứng dụng...")
    for _ in range(8):
        if find_text_and_tap(driver, "Safari"):
            print("Đã click vào ứng dụng Safari")
            break
        elif find_text_and_tap(driver, "Ứng dụng") or find_text_and_tap(driver, "dụng",True):
            isHaveApplication = True
            break
        scroll_vertical_percentage(driver, start_percent=0.8, end_percent=0.3, x_percent=0.5)
        time.sleep(1)
    else:
        print("❌ Không tìm thấy Safari. hay Ung Dung")
        return
    
    if isHaveApplication :
        print("[Safari] Đang tìm Safari...")
        for _ in range(18):
            if find_text_and_tap(driver, "Safari"):
                print("Đã click vào ứng dụng Safari")
                break
            scroll_vertical_percentage(driver, start_percent=0.8, end_percent=0.3, x_percent=0.5)
            time.sleep(1)
        else:
            print("❌ Không tìm thấy Safari. hay Ung Dung")
            return

    print("[Safari] Đang tìm nút tính năng Ẩn địa chỉ IP...")
    for _ in range(8):
        if find_text_and_tap(driver, "Ẩn địa chỉ IP", exact_match=False):
            find_text_and_tap(driver, "Tắt")
            time.sleep(1)
            find_text_and_tap(driver, "Từ trình theo dõi") or \
            find_text_and_tap(driver, "Trình theo dõi và trang web") or \
            find_text_and_tap(driver, "Chỉ trình theo dõi")
            time.sleep(1)
            find_text_and_tap(driver, "Tắt")
            time.sleep(1)
            find_text_and_tap(driver, "Từ trình theo dõi") or \
            find_text_and_tap(driver, "Trình theo dõi và trang web") or \
            find_text_and_tap(driver, "Chỉ trình theo dõi")
            time.sleep(1)
            print("Đã bật trình theo dõi")
            find_text_and_tap(driver, "Safari")
            time.sleep(1)
            break
        scroll_vertical_percentage(driver, start_percent=0.8, end_percent=0.3, x_percent=0.5)
        time.sleep(1)
    else:
        print("❌ Không tìm thấy nút Ẩn địa chỉ IP.")
        return

    print("[Safari] Đang tìm nút xoá dữ liệu...")
    for _ in range(5):
        if find_text_and_tap(driver, "Xóa lịch sử", exact_match=True) or \
           find_text_and_tap(driver, "và dữ liệu", exact_match=False):
            break
        scroll_vertical_percentage(driver, start_percent=0.8, end_percent=0.3, x_percent=0.5)
        time.sleep(1)
    else:
        print("❌ Không tìm thấy nút xóa dữ liệu.")
        return

    time.sleep(2)
    find_text_and_tap(driver, "Xóa lịch sử và dữ liệu", exact_match=True) or \
          find_text_and_tap_with_index(driver, "Xóa lịch sử",index=1, exact_match=True)
    time.sleep(2)
    find_text_and_tap(driver, "Đóng các tab", exact_match=True)
    time.sleep(2)
    print("✅ Đã xoá dữ liệu lịch sử Safari.")
    find_text_and_tap(driver, "Ứng dụng", exact_match=True)
    time.sleep(2)
    find_text_and_tap(driver, "Cài đặt", exact_match=True)
    time.sleep(8)

    print("Scroll lên tìm chế độ máy bay...")
    for _ in range(5):
        scroll_vertical_percentage(driver, start_percent=0.3, end_percent=0.8, x_percent=0.5)
        time.sleep(1)

    for _ in range(10):
        if find_text_and_tap(driver, "Chế độ máy bay", exact_match=True):
            time.sleep(1)
            print("Đã tìm được mục chế độ máy bay")
            set_airplane_mode(driver, False)
            break
        scroll_vertical_percentage(driver, start_percent=0.3, end_percent=0.8, x_percent=0.5)
        time.sleep(1)
    else:
        print("❌ Không tìm thấy nút xóa dữ liệu.")
        return

    driver.execute_script("mobile: pressButton", {"name": "home"})
    time.sleep(2)
    open_app(driver,"com.google.ios.youtube", "Youtube")
    time.sleep(12)
