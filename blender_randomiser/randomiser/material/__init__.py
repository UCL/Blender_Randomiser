from . import operators, ui
from .properties import all_properties


def register():
    all_properties.register()
    ui.register()
    operators.register()


def unregister():
    all_properties.unregister()
    ui.unregister()
    operators.unregister()
