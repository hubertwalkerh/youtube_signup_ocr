import subprocess
import time
import os
import multiprocessing
from youtube_signup_flow import signup_account
from appium import webdriver

def start_appium_server(port: int, wda_port: int, log_file: str):
    command = [
        "appium",
        "-p", str(port),
        "--default-capabilities", f'{{"wdaLocalPort": {wda_port}}}'
    ]
    with open(log_file, "w") as f:
        subprocess.Popen(command, stdout=f, stderr=subprocess.STDOUT)
    time.sleep(5)  # Chờ Appium khởi động

def run_signup(udid: str, port: int, wda_port: int, log_path: str):
    start_appium_server(port, wda_port, log_path)

    desired_caps = {
        "platformName": "iOS",
        "platformVersion": "16.0",
        "deviceName": "iPhone",
        "automationName": "XCUITest",
        "udid": udid,
        "bundleId": "com.google.ios.youtube",
        "noReset": True,
        "wdaLocalPort": wda_port,
    }

    driver = webdriver.Remote(f"http://localhost:{port}/wd/hub", desired_caps)
    try:
        signup_account(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    devices = [
        {"udid": "00008030-XXXXXXX1", "port": 4723, "wda_port": 8100},
        {"udid": "00008030-XXXXXXX2", "port": 4725, "wda_port": 8101},
    ]

    os.makedirs("logs", exist_ok=True)
    processes = []
    for i, device in enumerate(devices):
        log_file = f"logs/device_{i+1}.log"
        p = multiprocessing.Process(
            target=run_signup,
            args=(device["udid"], device["port"], device["wda_port"], log_file)
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()