from dataforge.core.pipeline import Pipeline
from dataforge.core.config import PipelineConfig, StepConfig
from dataforge.core.registry import registry
from dataforge.connectors.base import BaseConnector
from dataforge.exporters.base import BaseExporter

class _FakeFailingConnector(BaseConnector):
    def extract(self):
        raise ValueError("boom")

class _FakeExporter(BaseExporter):
    captured = []
    def export(self, data):
        _FakeExporter.captured.append(data)

def test_pipeline_continues_after_step_failure():
    # ทดสอบ BUG #1 โดยตรง: ยืนยันว่า pipeline "เดินต่อ" แม้ step แรก fail
    # (นี่คือพฤติกรรมปัจจุบันของระบบ — test นี้ "ยืนยัน bug" ไม่ใช่ "จับ bug")
    registry._connectors["_fake_fail"] = _FakeFailingConnector
    registry._exporters["_fake_export"] = _FakeExporter

    config = PipelineConfig(
        name="test_pipeline",
        steps=[
            StepConfig(plugin_type="connector", plugin_name="_fake_fail"),
            StepConfig(plugin_type="exporter", plugin_name="_fake_export"),
        ],
    )
    pipeline = Pipeline(config)
    context = pipeline.run()

    assert context.has_errors()
    assert len(context.errors) == 1
    # Pipeline ไม่ throw ออกมา — แสดงว่า "silent continue" เกิดขึ้นจริง
