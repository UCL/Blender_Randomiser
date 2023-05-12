from .property_classes import (
    collection_geom_socket_properties,
    collection_node_groups,
)

# -----------------------------------------
# Register and unregister functions
# ------------------------------------------


def register():
    collection_geom_socket_properties.register()
    collection_node_groups.register()
    print("geometry properties registered")


def unregister():
    collection_geom_socket_properties.unregister()
    collection_node_groups.unregister()
    print("geometry properties unregistered")
