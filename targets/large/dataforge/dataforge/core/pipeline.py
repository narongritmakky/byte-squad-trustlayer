from .context import PipelineContext
from .config import PipelineConfig
from .registry import registry
from .hooks import HookManager
from .exceptions import ConnectorError, TransformerError, ValidationError

class Pipeline:
    def __init__(self, config: PipelineConfig, hooks: HookManager = None):
        self.config = config
        self.hooks = hooks or HookManager()

    def run(self) -> PipelineContext:
        context = PipelineContext(self.config.name)

        for step in self.config.steps:
            self.hooks.fire_before_step(step.plugin_name, context)
            try:
                self._execute_step(step, context)
            except (ConnectorError, TransformerError, ValidationError) as exc:
                context.add_error(step.plugin_name, exc)
                self.hooks.fire_error(step.plugin_name, context, exc)
                # BUG #1 (High): pipeline ยังเดินต่อไปแม้ step ก่อนหน้า fail
                # ไม่มีการเช็ค config ว่า step นี้เป็น "critical" หรือ optional
                # ผลคือ downstream steps อาจได้รับ context.data ที่เป็น None/เก่า
                # แล้วดันไม่ throw ทำให้ pipeline รายงานว่า "เสร็จ" ทั้งที่ข้อมูลพัง
                continue
            self.hooks.fire_after_step(step.plugin_name, context)

        return context

    def _execute_step(self, step, context: PipelineContext) -> None:
        if step.plugin_type == "connector":
            plugin_cls = registry.get_connector(step.plugin_name)
            plugin = plugin_cls(**step.params)
            context.set_data(plugin.extract())
        elif step.plugin_type == "transformer":
            plugin_cls = registry.get_transformer(step.plugin_name)
            plugin = plugin_cls(**step.params)
            context.set_data(plugin.transform(context.data))
        elif step.plugin_type == "validator":
            plugin_cls = registry.get_validator(step.plugin_name)
            plugin = plugin_cls(**step.params)
            plugin.validate(context.data)
        elif step.plugin_type == "exporter":
            plugin_cls = registry.get_exporter(step.plugin_name)
            plugin = plugin_cls(**step.params)
            plugin.export(context.data)
