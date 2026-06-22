import re
from abc import ABC, abstractmethod

class BaseLesson(ABC):
    platform_name = "Rikkei Academy LMS"
    base_completion_points = 10

    def __init__(self, lesson_code, title):
        if not self.validate_lesson_code(lesson_code):
            raise ValueError(
                "Ma bai hoc khong hop le! Phai gom dung 10 ky tu va bat dau bang LMS."
            )
        self.lesson_code = lesson_code
        self.title = title
        self.__duration_minutes = 0

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        cleaned = re.sub(r"\s+", " ", value.strip())
        self._title = cleaned.upper()

    @property
    def duration_minutes(self):
        return self.__duration_minutes

    def _add_duration(self, minutes):
        if minutes <= 0:
            raise ValueError(
                "Thoi luong bai hoc va thong so kiem thu khong duoc nho hon hoac bang 0"
            )
        self.__duration_minutes += minutes

    @abstractmethod
    def calculate_completion_score(self):
        raise NotImplementedError

    @abstractmethod
    def update_content(self, new_data):
        raise NotImplementedError

    def __add__(self, other):
        if not isinstance(other, BaseLesson):
            return NotImplemented
        return self.duration_minutes + other.duration_minutes

    def __lt__(self, other):
        if not isinstance(other, BaseLesson):
            return NotImplemented
        return self.duration_minutes < other.duration_minutes

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.lesson_code} - {self.title}>"

    @staticmethod
    def validate_lesson_code(lesson_code):
        return (
            isinstance(lesson_code, str)
            and len(lesson_code) == 10
            and lesson_code.startswith("LMS")
        )

    @classmethod
    def update_base_points(cls, new_points):
        if new_points <= 0:
            raise ValueError("Diem co ban moi phai lon hon 0")
        cls.base_completion_points = new_points


class VideoLesson(BaseLesson):
    def __init__(self, lesson_code, title, video_quality="720p"):
        super().__init__(lesson_code, title)
        self.video_quality = video_quality
        self.view_count = 0

    def calculate_completion_score(self):
        return self.base_completion_points + (self.duration_minutes * 0.5)

    def update_content(self, new_data):
        if not isinstance(new_data, str) or not new_data.strip():
            raise ValueError("Du lieu cap nhat chat luong video khong hop le.")
        self.video_quality = new_data.strip().upper()

    def play_video(self):
        self.view_count += 1


class CodingChallenge(BaseLesson):
    def __init__(self, lesson_code, title, number_of_testcases=0, difficulty_multiplier=1.0):
        super().__init__(lesson_code, title)
        self.number_of_testcases = number_of_testcases
        self.difficulty_multiplier = difficulty_multiplier

    def calculate_completion_score(self):
        return self.base_completion_points * self.number_of_testcases * self.difficulty_multiplier

    def update_content(self, new_data):
        if new_data <= 0:
            raise ValueError(
                "Thoi luong bai hoc va thong so kiem thu khong duoc nho hon hoac bang 0"
            )
        self.number_of_testcases += new_data


class HybridAssessment(VideoLesson, CodingChallenge):
    def __init__(self, lesson_code, title, video_quality="720p",
                 number_of_testcases=0, difficulty_multiplier=1.0):
        VideoLesson.__init__(self, lesson_code, title, video_quality)
        CodingChallenge.__init__(self, lesson_code, title, number_of_testcases, difficulty_multiplier)

    def calculate_completion_score(self):
        video_part = self.duration_minutes * 0.5
        coding_part = self.number_of_testcases * self.difficulty_multiplier * self.base_completion_points
        return self.base_completion_points + video_part + coding_part

    def update_content(self, new_data):
        CodingChallenge.update_content(self, new_data)


class AWSS3StorageService:
    def upload_lesson(self, lesson):
        print("[He thong AWS S3]: Dang khoi tao luong bang thong ket noi toi LMS...")
        print("Xac thuc dich vu bang Duck Typing thanh cong!")
        print(
            f"He thong luu tru dam may da upload toan bo tai nguyen cua bai hoc "
            f"{lesson.lesson_code} len cum may chu an toan."
        )


class GoogleCloudStorageService:
    def upload_lesson(self, lesson):
        print("[He thong Google Cloud Storage]: Dang khoi tao luong bang thong ket noi toi LMS...")
        print("Xac thuc dich vu bang Duck Typing thanh cong!")
        print(
            f"He thong luu tru dam may da upload toan bo tai nguyen cua bai hoc "
            f"{lesson.lesson_code} len cum may chu an toan."
        )


def sync_to_cloud(cloud_service, lesson):
    try:
        cloud_service.upload_lesson(lesson)
    except AttributeError:
        print(
            "Dich vu luu tru dam may khong hop le hoac chua ky ket chung chi "
            "API lien thong."
        )


lessons = []
current_lesson = None


def print_header():
    print("\n===== RIKKEI ACADEMY LMS SIMULATOR PRO =====")
    print("1. Khoi tao bai hoc moi (Chon loai bai hoc noi dung)")
    print("2. Xem thong tin bai hoc & Kiem tra thu tu ke thua (MRO)")
    print("3. Cap nhat thoi luong & Noi dung bai hoc (Tinh da hinh)")
    print("4. Xem chi tiet diem thuong hoan thanh bai hoc")
    print("5. Kiem tra gop thoi luong & So sanh do dai bai hoc (Overloading)")
    print("6. Dong bo bai giang len Nen tang Dam may (Duck Typing)")
    print("7. Thoat chuong trinh")
    print("==============================================")


def read_number(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        print("Du lieu nhap khong hop le (phai la so).")
        return None


def menu_create_lesson():
    print("\n--- CHON LOAI BAI HOC KHOI TAO ---")
    print("1. Video Lesson (Bai hoc Video Ly Thuyet)")
    print("2. Coding Challenge (Bai tap Thuc Hanh Code)")
    print("3. Hybrid Assessment (Bai Kiem Tra Tong Hop)")
    choice = input("Chon loai bai hoc (1-3): ").strip()

    lesson_code = input("Nhap ma bai hoc 10 ky tu: ").strip()
    if not BaseLesson.validate_lesson_code(lesson_code):
        print("Ma bai hoc khong hop le! Phai gom dung 10 ky tu va bat dau bang LMS.")
        return

    title = input("Nhap tieu de bai hoc: ")

    global current_lesson
    try:
        if choice == "1":
            new_lesson = VideoLesson(lesson_code, title)
            print(f"Khoi tao bai hoc Video thanh cong!\nTieu de bai hoc: {new_lesson.title}")
        elif choice == "2":
            new_lesson = CodingChallenge(lesson_code, title)
            print(f"Khoi tao bai tap Coding thanh cong!\nTieu de bai hoc: {new_lesson.title}")
        elif choice == "3":
            new_lesson = HybridAssessment(lesson_code, title)
            print(f"Khoi tao bai Hybrid Assessment thanh cong!\nTieu de bai hoc: {new_lesson.title}")
        else:
            print("Lua chon khong hop le.")
            return
    except ValueError as e:
        print(f"Ma bai hoc khong hop le! {e}")
        return

    lessons.append(new_lesson)
    current_lesson = new_lesson


def menu_view_info():
    if current_lesson is None:
        print("Chua co bai hoc nao duoc chon. Vui long khoi tao hoac chon bai hoc truoc.")
        return

    lesson = current_lesson
    print("\n--- THONG TIN BAI HOC HIEN TAI ---")
    print(f"Loai bai hoc: {type(lesson).__name__}")
    print(f"Nen tang: {lesson.platform_name}")
    print(f"Ma bai hoc: {lesson.lesson_code}")
    print(f"Tieu de bai hoc: {lesson.title}")
    print(f"Thoi luong bai hoc: {lesson.duration_minutes} phut")

    if isinstance(lesson, VideoLesson):
        print(f"Chat luong video: {lesson.video_quality}")
        print(f"So luot xem: {lesson.view_count} luot")
    if isinstance(lesson, CodingChallenge):
        print(f"So luong testcase lap trinh: {lesson.number_of_testcases} bai")
        print(f"He so do kho: {lesson.difficulty_multiplier}")

    print("\n--- THU TU KE THUA (MRO) ---")
    mro_names = [klass.__name__ for klass in type(lesson).__mro__]
    print(" -> ".join(mro_names))


def menu_update_content():
    if current_lesson is None:
        print("Chua co bai hoc nao duoc chon.")
        return

    lesson = current_lesson
    print("\n--- CAP NHAT NOI DUNG & THOI LUONG ---")
    print("1. Gia lap hoc vien tang luot xem video (Chi danh cho Video/Hybrid)")
    print("2. Cap nhat thong so bai hoc (Thoi luong, testcase...)")
    task = input("Chon tac vu (1-2): ").strip()

    if task == "1":
        if not isinstance(lesson, VideoLesson):
            print("Chuc nang nay chi danh cho Video Lesson/Hybrid Assessment.")
            return
        lesson.play_video()
        print(
            f"Ghi nhan thanh cong! Hoc vien da xem video bai hoc.\n"
            f"Tong so luot xem hien tai: {lesson.view_count} luot."
        )
    elif task == "2":
        try:
            if isinstance(lesson, CodingChallenge):
                value_str = input("Nhap so luong testcase kiem thu moi bo sung: ").strip()
                value = int(value_str)
                lesson.update_content(value)
                print("\nCap nhat thong so thanh cong!")
                print(f"So luong testcase hien tai tren he thong: {lesson.number_of_testcases} testcases.")
            elif isinstance(lesson, VideoLesson):
                value = input("Nhap chat luong video moi (vd: 1080p, 4K): ").strip()
                lesson.update_content(value)
                print("\nCap nhat thong so thanh cong!")
                print(f"Chat luong video hien tai: {lesson.video_quality}.")
        except ValueError as e:
            print(f"Loi du lieu: {e}")
    else:
        print("Lua chon khong hop le.")


def menu_calculate_score():
    if current_lesson is None:
        print("Chua co bai hoc nao duoc chon.")
        return

    lesson = current_lesson
    score = lesson.calculate_completion_score()

    print("\n--- CHI TIET DIEM THUONG HOAN THANH ---")
    print(f"Bai hoc: {lesson.title} (Loai: {type(lesson).__name__})")
    print(f"Diem co so he thong: {lesson.base_completion_points} XP")
    print(f"Thoi luong tich luy: {lesson.duration_minutes} phut")
    if isinstance(lesson, CodingChallenge):
        print(f"So luong testcase cau hinh: {lesson.number_of_testcases} bai")
    print(f"Tong diem kinh nghiem (XP) nhan duoc khi hoan thanh: {score:,.1f} XP")


def menu_compare_duration():
    if current_lesson is None:
        print("Chua co bai hoc nao duoc chon.")
        return

    others = [l for l in lessons if l is not current_lesson]
    if not others:
        print("Chua co bai hoc khac trong he thong de doi ung so sanh.")
        return

    print("\n--- DONG BO & SO SANH THOI LUONG (OPERATOR OVERLOADING) ---")
    print(f"Bai hoc hien tai (A): {current_lesson.title} (Thoi luong: {current_lesson.duration_minutes} phut)")
    print("Danh sach bai hoc doi ung kha dung:")
    for idx, l in enumerate(others, start=1):
        print(f"{idx}. {l.lesson_code} ({l.title} - Thoi luong: {l.duration_minutes} phut)")

    try:
        idx = int(input("Chon bai hoc doi ung (B) theo so thu tu: "))
    except ValueError:
        print("Lua chon khong hop le.")
        return
    if idx < 1 or idx > len(others):
        print("Lua chon khong hop le.")
        return

    other = others[idx - 1]

    if current_lesson < other:
        print("[Ket qua So sanh (__lt__)]: Thoi luong bai hoc A NGAN HON thoi luong bai hoc B.")
    elif other < current_lesson:
        print("[Ket qua So sanh (__lt__)]: Thoi luong bai hoc A DAI HON thoi luong bai hoc B.")
    else:
        print("[Ket qua So sanh (__lt__)]: Thoi luong cua 2 bai hoc BANG NHAU.")

    total_duration = current_lesson + other
    print(f"[Ket qua Tong hop (__add__)]: Tong thoi luong hoc tap cua ca 2 bai hoc la: {total_duration} phut.")


def menu_sync_to_cloud():
    if current_lesson is None:
        print("Chua co bai hoc nao duoc chon.")
        return

    print("\n--- DONG BO BAI GIANG LEN NEN TANG DAM MAY ---")
    print("1. Dong bo len may chu AWS S3 Storage")
    print("2. Dong bo len may chu Google Cloud Storage")
    choice = input("Chon dich vu luu tru (1-2): ").strip()

    if choice == "1":
        service = AWSS3StorageService()
    elif choice == "2":
        service = GoogleCloudStorageService()
    else:
        print("Lua chon khong hop le.")
        return

    sync_to_cloud(service, current_lesson)


def main():
    while True:
        print_header()
        choice = input("Chon chuc nang (1-7): ").strip()

        if choice == "1":
            menu_create_lesson()
        elif choice == "2":
            menu_view_info()
        elif choice == "3":
            menu_update_content()
        elif choice == "4":
            menu_calculate_score()
        elif choice == "5":
            menu_compare_duration()
        elif choice == "6":
            menu_sync_to_cloud()
        elif choice == "7":
            print("Cam on ban da trai nghiem he thong Quan ly Bai hoc Rikkei Academy LMS Pro!")
            break
        else:
            print("Lua chon khong hop le, vui long chon tu 1-7.")


if __name__ == "__main__":
    main()