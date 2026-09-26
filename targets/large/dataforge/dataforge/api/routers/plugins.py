from fastapi import APIRouter
from ...core.registry import registry
from ..schemas import PluginInfo

router = APIRouter(prefix="/plugins", tags=["plugins"])

@router.get("/", response_model=list[PluginInfo])
def list_plugins():
    result = []
    for name in registry._connectors:
        result.append(PluginInfo(plugin_type="connector", name=name))
    for name in registry._transformers:
        result.append(PluginInfo(plugin_type="transformer", name=name))
    for name in registry._validators:
        result.append(PluginInfo(plugin_type="validator", name=name))
    for name in registry._exporters:
        result.append(PluginInfo(plugin_type="exporter", name=name))
    return result
