import subprocess
import time
import requests
import multiprocessing
import subprocess
from appium import webdriver
from appium.options.ios import XCUITestOptions
from youtube_signup_flow import signup_account

def get_ios_version(udid):
    try:
        result = subprocess.run(
            ["ideviceinfo", "-u", udid, "-k", "ProductVersion"],
            capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        return version
    except subprocess.CalledProcessError:
        return None

def get_connected_udids():
    try:
        result = subprocess.check_output(["idevice_id", "-l"]).decode().strip()
        print(f"get_connected_udids result : {result}")
        return result.splitlines()
    except Exception as e:
        print(f"Error getting UDIDs: {e}")
        return []
    
def wait_for_appium_ready(wda_port, timeout=30):
    url = f"http://localhost:{wda_port}/wd/hub/status"
    for i in range(timeout):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                print(f"✅ Appium tại cổng {wda_port} đã sẵn sàng!")
                return True
            else:
                print(f"✅ Appium tại cổng {wda_port} chua sẵn sàng!")
        except:
            pass
        time.sleep(1)
    print(f"❌ Appium tại cổng {wda_port} không phản hồi sau {timeout} giây.")
    return False

def start_appium_server(wda_port, udid):
    """Chạy 1 phiên Appium server riêng biệt."""
    # log_file = f"appium_{udid}.log"
    # command = [
    #     "appium",
    #     "-p", str(wda_port),
    #     "--base-path", f"/wd/hub",
    #     "--use-drivers", "xcuitest",
    #     "--log", log_file
    # ]

    # print(f"🚀 Đang chạy Appium server cho thiết bị {udid} tại cổng {wda_port}")
    # subprocess.Popen(command)
    subprocess.Popen(
        ["appium", "--port", str(wda_port), "--base-path", "/wd/hub", "--use-driver", "xcuitest"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def run_signup(udid: str, wda_port: int):
    while True:
        try:
            print(f"[{udid}] Bắt đầu chạy automation...")
            start_appium_server(wda_port, udid)
            wait_for_appium_ready(wda_port, timeout=30)
            options = XCUITestOptions()
            options.platform_name = "iOS"
            options.platform_version = get_ios_version(udid)
            options.device_name = "iPhone"
            options.automation_name = "XCUITest"
            options.udid = udid
            options.bundle_id = "com.apple.Preferences"
            options.no_reset = True

            driver = webdriver.Remote(
                command_executor=f"http://localhost:{wda_port}/wd/hub",
                options=options
            )
            try:
                print(f" UDID=: {udid}")
                # Đóng ứng dụng Settings
                driver.terminate_app("com.google.ios.youtube")
                signup_account(driver, udid=udid)
            finally:
                driver.quit()
            print(f"[{udid}] Hoàn tất. Đợi 30 phút trước khi chạy lại...")
            for i in range(30, 0, -1): # từ 30 đến 1
                time.sleep(60)  # 60 giay
                print(f"[{udid}] Còn chờ thêm {i} phút nữa để tạo tài khoản tiếp theo")
        except Exception as e:
            print(f"[{udid}] Lỗi: {e}")
            print(f"[{udid}] Thử lại sau 3 phút...")
            time.sleep(3*60)

if __name__ == "__main__":
    udids = get_connected_udids()
    base_port = 8200

    processes = []
    for index, udid in enumerate(udids):
        port = base_port + index
        p = multiprocessing.Process(target=run_signup, args=(udid, port))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
