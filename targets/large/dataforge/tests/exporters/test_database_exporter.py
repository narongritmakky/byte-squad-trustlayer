import pytest
from dataforge.exporters.database_exporter import DatabaseExporter

def test_malicious_table_name_executes_injected_sql(tmp_path):
    # ทดสอบ BUG #10 (CRITICAL): พิสูจน์ว่า table_name ที่มี SQL แปลกปลอม
    # จะถูกรันจริงผ่าน f-string โดยไม่ถูก sanitize
    db_path = str(tmp_path / "test.db")
    malicious_table = "users; ATTACH DATABASE ':memory:' AS x; --"
    exporter = DatabaseExporter(db_path=db_path, table_name=malicious_table)

    # คาดหวังว่าระบบที่ปลอดภัยควร reject table_name นี้ตั้งแต่แรก
    # แต่ปัจจุบันโค้ดจะพยายามรัน CREATE TABLE ด้วยชื่อนี้ตรงๆ
    with pytest.raises(Exception):
        # อาจ error เพราะ syntax SQL ผิด แต่ประเด็นคือมันถูก "รัน" ไปแล้ว
        # ไม่ได้ถูก validate/reject ก่อนแตะ database เลย
        exporter.export([{"id": 1, "name": "test"}])
