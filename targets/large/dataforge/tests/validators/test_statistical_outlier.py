from dataforge.validators.statistical_outlier import StatisticalOutlierValidator

def test_single_record_passes_silently():
    # ทดสอบ BUG #9: dataset ที่มี record เดียวจะ "ผ่าน" validator เสมอ
    # โดยไม่มี error หรือ warning ใดๆ ให้เห็นเลย
    validator = StatisticalOutlierValidator(field="amount", std_threshold=3.0)
    data = [{"amount": 999999}]  # ค่าประหลาดขนาดไหนก็ผ่าน เพราะ n < 2
    validator.validate(data)  # ไม่ throw — นี่คือพฤติกรรมของ bug
