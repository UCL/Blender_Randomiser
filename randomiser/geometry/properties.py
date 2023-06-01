from .property_classes import (
    collection_geom_socket_properties,
    collection_gngs,
)

# -----------------------------------------
# Register and unregister functions
# ------------------------------------------


def register():
    collection_geom_socket_properties.register()
    collection_gngs.register()
    print("geometry properties registered")


def unregister():
    collection_geom_socket_properties.unregister()
    collection_gngs.unregister()
    print("geometry properties unregistered")
