from . import properties, ui


def register():
    properties.register()
    ui.register()


def unregister():
    properties.unregister()
    ui.unregister()
