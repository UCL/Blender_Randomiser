from . import operators, ui, properties


def register():
    properties.register()
    ui.register()
    operators.register()


def unregister():
    properties.unregister()
    ui.unregister()
    operators.unregister()
