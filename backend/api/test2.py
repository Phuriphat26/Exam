from datetime import datetime, time

class Scheduler:
    """คลาสสำหรับจัดการและตรวจสอบตารางเวลาว่าง"""

    def __init__(self):
        # สร้าง list สำหรับเก็บกฎของเวลาที่ว่าง
        # รูปแบบ: (day_of_week, start_time, end_time)
        # day_of_week: 0=จันทร์, 1=อังคาร, ..., 6=อาทิตย์ หรือ None=ทุกวัน
        self.availability_rules = []

    def add_availability(self, day_of_week, start_time, end_time):
        """
        เพิ่มกฎของช่วงเวลาที่ว่าง
        - day_of_week: ใช้วันในสัปดาห์ (0-6) หรือ None หากต้องการให้เป็นทุกวัน
        - start_time: เวลาเริ่มต้น (ใช้ đối tượng time)
        - end_time: เวลาสิ้นสุด (ใช้ đối tượng time)
        """
        rule = (day_of_week, start_time, end_time)
        self.availability_rules.append(rule)
        print(f"✅ เพิ่มกฎใหม่: {'ทุกวัน' if day_of_week is None else f'วันที่ {day_of_week}'} เวลา {start_time} - {end_time}")

    def is_available(self, check_datetime):
        """
        ตรวจสอบว่าเวลาที่ระบุ (check_datetime) ว่างหรือไม่
        - check_datetime: เวลาที่ต้องการตรวจสอบ (ใช้ đối tượng datetime)
        """
        check_day = check_datetime.weekday() # 0=จันทร์, ..., 6=อาทิตย์
        check_time = check_datetime.time()

        # วนลูปเพื่อเช็กกฎทุกข้อ
        for day_rule, start_time, end_time in self.availability_rules:
            # เช็กวันในสัปดาห์
            # ถ้ากฎเป็น 'ทุกวัน' (None) หรือ วันตรงกัน ให้เช็กเวลาต่อ
            day_matches = (day_rule is None) or (day_rule == check_day)

            if day_matches:
                # เช็กช่วงเวลา
                if start_time <= check_time < end_time:
                    return True # เจอช่วงเวลาที่ว่างแล้ว

        return False # ไม่ตรงกับกฎข้อไหนเลย

# --- ตัวอย่างการใช้งาน ---
if __name__ == "__main__":
    # 1. สร้างตารางเวลา
    my_scheduler = Scheduler()

    # 2. เพิ่มกฎตามที่ต้องการ
    # ว่าง "ทุกวัน" เวลา 18:00 ถึง 20:00
    my_scheduler.add_availability(None, time(18, 0), time(20, 0))

    # เพิ่มกฎอื่น: ว่าง "ทุกวันพุธ" (weekday=2) เวลา 10:00 ถึง 12:00
    my_scheduler.add_availability(2, time(10, 0), time(12, 0))
    
    print("\n--- เริ่มการตรวจสอบ ---")

    # 3. ลองตรวจสอบเวลาต่างๆ
    # วันพุธ เวลา 19:00 -> ควรจะ "ว่าง" (ตรงกับกฎทุกวัน)
    time_to_check1 = datetime(2025, 10, 15, 19, 0)
    print(f"กำลังเช็ก {time_to_check1}: ว่างหรือไม่? 👉 {my_scheduler.is_available(time_to_check1)}")

    # วันพุธ เวลา 21:00 -> ควรจะ "ไม่ว่าง"
    time_to_check2 = datetime(2025, 10, 15, 21, 0)
    print(f"กำลังเช็ก {time_to_check2}: ว่างหรือไม่? 👉 {my_scheduler.is_available(time_to_check2)}")

    # วันพฤหัสบดี เวลา 18:30 -> ควรจะ "ว่าง" (ตรงกับกฎทุกวัน)
    time_to_check3 = datetime(2025, 10, 16, 18, 30)
    print(f"กำลังเช็ก {time_to_check3}: ว่างหรือไม่? 👉 {my_scheduler.is_available(time_to_check3)}")
    
    # วันพุธ เวลา 11:00 -> ควรจะ "ว่าง" (ตรงกับกฎวันพุธ)
    time_to_check4 = datetime(2025, 10, 15, 11, 0)
    print(f"กำลังเช็ก {time_to_check4}: ว่างหรือไม่? 👉 {my_scheduler.is_available(time_to_check4)}")

    # วันอังคาร เวลา 11:00 -> ควรจะ "ไม่ว่าง" (กฎ 10:00-12:00 เป็นของวันพุธเท่านั้น)
    time_to_check5 = datetime(2025, 10, 14, 11, 0)
    print(f"กำลังเช็ก {time_to_check5}: ว่างหรือไม่? 👉 {my_scheduler.is_available(time_to_check5)}")