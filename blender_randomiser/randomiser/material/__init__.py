from . import operators, properties, ui


def register():
    properties.register()
    ui.register()
    operators.register()


def unregister():
    properties.unregister()
    ui.unregister()
    operators.unregister()
