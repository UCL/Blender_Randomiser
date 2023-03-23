from . import properties
from . import ui
from . import operators


def register():
    properties.register()
    ui.register()
    operators.register()


def unregister():
    properties.unregister()
    ui.unregister()
    operators.unregister()
