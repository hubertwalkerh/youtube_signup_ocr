import time
import io
import base64
import unicodedata
from PIL import Image
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import easyocr
import numpy as np
from selenium.webdriver.common.by import By
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

reader = easyocr.Reader(['vi'], gpu=False)

def take_screenshot_and_ocr(driver: WebDriver):
    print("Bắt đầu screenshot")
    screenshot_base64 = driver.get_screenshot_as_base64()
    image_bytes = base64.b64decode(screenshot_base64)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    results = reader.readtext(np.array(image))
    print("Server đã trả về kết quả")
    return results, image

def tap_at(driver, x, y):
    finger = PointerInput("touch", "finger")
    actions = ActionBuilder(driver, mouse=finger)  # Truyền finger vào tham số mouse
    
    actions.pointer_action.move_to_location(x, y)
    actions.pointer_action.pointer_down()
    actions.pointer_action.pause(0.1)
    actions.pointer_action.pointer_up()

    actions.perform()

def normalize_text(text):
    """
    Chuyển về chữ thường và loại bỏ dấu tiếng Việt.
    """
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text

def find_text_and_tap(driver: WebDriver, keyword: str, exact_match: bool = True) -> bool:
    
    results, img = take_screenshot_and_ocr(driver)
    print("OCR image size:", img.size)
    window_size = driver.get_window_size()
    print("Device screen size:", window_size)
    scale_x = window_size['width'] / img.size[0]
    scale_y = window_size['height'] / img.size[1]

    keyword_norm = normalize_text(keyword)

    print("[OCR] Các text tìm được trên màn hình:")
    for detection in results:
        text_raw = detection[1].strip()
        print(f"  - {text_raw}")

    for detection in results:
        text_raw = detection[1].strip()
        text_norm = normalize_text(text_raw)

        if (exact_match and keyword_norm == text_norm) or (not exact_match and keyword_norm in text_norm):
            coords = detection[0]
            x = int((coords[0][0] + coords[2][0]) / 2)
            y = int((coords[0][1] + coords[2][1]) / 2)
            print(f"[OCR] Found {'exact match' if exact_match else 'partial match'} '{text_raw}' → Tap at ({x},{y})")
            x_real = int(x * scale_x)
            y_real = int(y * scale_y)
            tap_at(driver, x_real, y_real)
            time.sleep(3)
            return True
    print(f"[OCR] '{keyword}' not found on screen (normalized)")
    return False

def wait_and_find_text_and_tap(driver: WebDriver, keyword: str, exact_match: bool = True) -> bool:
    for _ in range(3):
        results, img = take_screenshot_and_ocr(driver)
        print("OCR image size:", img.size)
        window_size = driver.get_window_size()
        print("Device screen size:", window_size)
        scale_x = window_size['width'] / img.size[0]
        scale_y = window_size['height'] / img.size[1]

        keyword_norm = normalize_text(keyword)

        print("[OCR] Các text tìm được trên màn hình:")
        for detection in results:
            text_raw = detection[1].strip()
            print(f"  - {text_raw}")

        for detection in results:
            text_raw = detection[1].strip()
            text_norm = normalize_text(text_raw)

            if (exact_match and keyword_norm == text_norm) or (not exact_match and keyword_norm in text_norm):
                coords = detection[0]
                x = int((coords[0][0] + coords[2][0]) / 2)
                y = int((coords[0][1] + coords[2][1]) / 2)
                print(f"[OCR] Found {'exact match' if exact_match else 'partial match'} '{text_raw}' → Tap at ({x},{y})")
                x_real = int(x * scale_x)
                y_real = int(y * scale_y)
                tap_at(driver, x_real, y_real)
                time.sleep(3)
                return True
        time.sleep(3)
    print(f"[OCR] '{keyword}' not found on screen (normalized)")
    return False


def find_text_and_tap_with_index(driver: WebDriver, keyword: str, index: int = 0, exact_match: bool = True) -> bool:
    results, img = take_screenshot_and_ocr(driver)

    print("OCR image size:", img.size)
    window_size = driver.get_window_size()
    print("Device screen size:", window_size)
    scale_x = window_size['width'] / img.size[0]
    scale_y = window_size['height'] / img.size[1]

    keyword_norm = normalize_text(keyword)
    matched_elements = []

    print("[OCR] Các text tìm được trên màn hình:")
    for detection in results:
        text_raw = detection[1].strip()
        print(f"  - {text_raw}")

    # Tìm tất cả text khớp
    for detection in results:
        text_raw = detection[1].strip()
        text_norm = normalize_text(text_raw)

        if (exact_match and keyword_norm == text_norm) or (not exact_match and keyword_norm in text_norm):
            matched_elements.append((detection, text_raw))

    # Nếu không có kết quả khớp
    if not matched_elements:
        print(f"[OCR] '{keyword}' not found on screen (normalized)")
        return False

    if index >= len(matched_elements):
        print(f"[OCR] Có {len(matched_elements)} kết quả khớp, nhưng index {index} vượt quá phạm vi.")
        return False

    # Lấy phần tử theo index
    detection, text_raw = matched_elements[index]
    coords = detection[0]
    x = int((coords[0][0] + coords[2][0]) / 2)
    y = int((coords[0][1] + coords[2][1]) / 2)
    x_real = int(x * scale_x)
    y_real = int(y * scale_y)

    print(f"[OCR] Tapping vào kết quả #{index}: '{text_raw}' → Tap at ({x_real},{y_real})")
    tap_at(driver, x_real, y_real)
    time.sleep(3)
    return True


def input_text(driver: WebDriver, text: str, is_password: bool = False, index: int = 0, is_finder: bool = False):
    print(f"[Input] Typing: {text}")
    try:
        # Chọn loại input field theo kiểu (text thường hay password)
        if is_password:
            input_fields = driver.find_elements(By.CLASS_NAME, "XCUIElementTypeSecureTextField")
        elif is_finder:
            input_fields = driver.find_elements(By.CLASS_NAME, "XCUIElementTypeSearchField")
        else:
            input_fields = driver.find_elements(By.CLASS_NAME, "XCUIElementTypeTextField")

        if not input_fields:
            print("[Input] Không tìm thấy ô nhập liệu")
            return

        if index >= len(input_fields):
            print(f"[Input] Index {index} vượt quá số lượng ô nhập ({len(input_fields)})")
            return

        input_field = input_fields[index]
        input_field.click()
        input_field.clear()
        input_field.send_keys(text)
        time.sleep(1)

    except Exception as e:
        print(f"[Input] Lỗi khi nhập text: {e}")
