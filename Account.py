import json
import random
import string
import unicodedata
from datetime import datetime
from dataclasses import dataclass, asdict

def remove_accents(text):
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    text = text.replace('đ', 'd').replace('Đ', 'D')
    return text

@dataclass
class Account:
    first_name: str
    last_name: str
    username: str
    password: str
    udid: str
    created_at: str
    gender: str
    middle_name: str

    @staticmethod
    def random(udid: str) -> 'Account':
        male_first_names = ["Khoa", "Anh", "Huy", "Phúc", "Tú", "Bình", "Trung", "Minh", "Dũng", "Long"]
        female_first_names = ["Thanh", "Tina", "Ngọc", "Lan", "Thảo", "Linh", "Mai", "Hương", "Trang", "Vy"]

        male_middle_names = ["Văn", "Nhật", "Quang", "Trung", "Hải", "Đức", "Khánh", "Bảo"]
        female_middle_names = ["Thị", "Ngọc", "Thu", "Mai", "Hồng", "Diệu", "Bích", "Ánh"]

        last_names = [
            "Phan", "Nguyễn", "Trần", "Lê", "Hoàng", "Đặng", "Võ", "Bùi", "Đỗ", "Phạm", "Dương", "Lâm", "Mai"
        ]

        gender = random.choice(["Nam", "Nữ"])

        if gender == "Nam":
            first = random.choice(male_first_names)
            middle = random.choice(male_middle_names)
        else:
            first = random.choice(female_first_names)
            middle = random.choice(female_middle_names)

        last = random.choice(last_names)
        suffix = ''.join(random.choices(string.ascii_lowercase, k=2))

        username = f"{remove_accents(last.lower())}{remove_accents(middle.lower())}{remove_accents(first.lower())}{suffix}{random.randint(1000,9999)}"
        password = "P@ssword12345"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return Account(first, last, username, password, udid, created_at, gender, middle)
