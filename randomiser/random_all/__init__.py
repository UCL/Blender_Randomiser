from . import properties, ui, operators


def register():
    properties.register()
    ui.register()
    operators.register()


def unregister():
    properties.unregister()
    ui.unregister()
    operators.unregister()
