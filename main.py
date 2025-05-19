from appium import webdriver
from appium.options.ios import XCUITestOptions
from youtube_signup_flow import signup_account

options = XCUITestOptions()
options.platform_name = "iOS"
options.platform_version = "16.7"
options.device_name = "iPhone"
options.automation_name = "XCUITest"
options.udid = "bc2d0436363deaaa51013825f70069952c62a31a"
options.bundle_id = "com.apple.Preferences"
options.no_reset = True

driver = webdriver.Remote(
    command_executor="http://localhost:4723",
    options=options
)

print("Khởi tạo driver thành công")
signup_account(driver, "bc2d0436363deaaa51013825f70069952c62a31a")
driver.quit()
