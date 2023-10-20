import bpy

from .. import config
from ..material.ui import TemplatePanel


# ---------------------------------------------------
# Custom UIlist items
# ----------------------------------------------------
class CUSTOM_UL_items(bpy.types.UIList):
    def draw_item(
        self,
        context,
        layout,
        data,
        item,
        icon,
        active_data,
        active_propname,
        index,
    ):
        split = layout.split(factor=0.3)
        split.label(text="Index: %d" % (index))
        custom_icon = "COLOR"
        split.prop(item, "name", icon=custom_icon, emboss=False, text="")

    def invoke(self, context, event):
        pass


# ---------------------------------------------------
# Common layout for list of UD props to randomise
# ----------------------------------------------------
def draw_sockets_list_UD(
    cs,
    layout,
    list_UD_props,
    sockets_props_collection,
    attribute_only_str,
    full_str,
):
    # Define UI fields for every user defined property
    list_UD_props_sorted = list_UD_props
    row = layout.row()

    row_split = row.split()
    col1 = row_split.column(align=True)
    row_split.column(align=True)
    col3 = row_split.column(align=True)
    col4 = row_split.column(align=True)
    row_split.column(align=True)

    # input node name
    col1.label(text=sockets_props_collection.name)
    col1.alignment = "CENTER"

    # min label
    col3.alignment = "CENTER"
    col3.label(text="min")

    # max label
    col4.alignment = "CENTER"
    col4.label(text="max")

    row = layout.row()
    row_split = row.split()
    col1 = row_split.column(align=True)
    row_split.column(align=True)
    col3 = row_split.column(align=True)
    col4 = row_split.column(align=True)
    col5 = row_split.column(align=True)
    row_split.column(align=True)

    # UD prop name
    col1.alignment = "RIGHT"
    col1.label(text="value")  # text=sckt.name)

    # if UD prop is a color: format min/max as a color picker
    # and an array (color picker doesn't include alpha value)
    sckt = list_UD_props_sorted
    if type(sckt) == bpy.types.NodeSocketColor:
        for m_str, col in zip(["min", "max"], [col3, col4]):
            # color picker
            col.template_color_picker(
                sockets_props_collection,
                m_str + "_" + cs.socket_type_to_attr[type(sckt)],
            )
            # array
            for j, cl in enumerate(["R", "G", "B", "alpha"]):
                col.prop(
                    sockets_props_collection,
                    m_str + "_" + cs.socket_type_to_attr[type(sckt)],
                    icon_only=False,
                    text=cl,
                    index=j,
                )
    # if UD prop is Boolean: add non-editable labels
    elif type(sckt) == bpy.types.NodeSocketBool:
        for m_str, col in zip(["min", "max"], [col3, col4]):
            m_val = getattr(
                sockets_props_collection,
                m_str + "_" + cs.socket_type_to_attr[type(sckt)],
            )
            col.label(text=str(list(m_val)[0]))

    # if UD prop is not color type: format as a regular property
    else:
        objects_in_scene = []
        for key in bpy.data.objects:
            objects_in_scene.append(key.name)

        for m_str, col in zip(["min", "max"], [col3, col4]):
            if "[" in sockets_props_collection.name:
                obj_str = get_obj_str(sockets_props_collection.name)

                for i, obj in enumerate(objects_in_scene):
                    if obj in obj_str:
                        current_obj = obj
                        idx = i

                if "Camera" in current_obj:
                    attr_type = attr_get_type(
                        bpy.data.cameras[idx], attribute_only_str
                    )[0]
                else:
                    attr_type = attr_get_type(
                        bpy.data.objects[idx], attribute_only_str
                    )[0]
            else:
                attr_type = attr_get_type(
                    bpy.context.scene, attribute_only_str
                )[0]

            col.prop(
                sockets_props_collection,
                m_str + "_" + cs.UD_prop_to_attr[attr_type],
                icon_only=True,
            )

    # randomisation toggle
    col5.prop(
        sockets_props_collection,
        "bool_randomise",
        icon_only=True,
    )


def get_obj_str(full_str):
    x = full_str.split(".")
    for i in x:
        if "[" in i:
            ii = i.split("[")
            object_str = ii[1]
            object_str = object_str[:-1]

    return object_str


def attr_get_type(obj, path):
    if "." in path:
        # gives us: ('modifiers["Subsurf"]', 'levels')
        path_prop, path_attr = path.rsplit(".", 1)

        # same as: prop = obj.modifiers["Subsurf"]
        prop = obj.path_resolve(path_prop)
    else:
        prop = obj
        # single attribute such as name, location... etc
        path_attr = path

    # same as: prop.levels = value

    try:
        action = getattr(prop, path_attr)
    except Exception:
        # print("Property does not exist")
        action = "dummy"
        prop = "dummy"
        path_attr = "dummy"

    return type(action), action, prop, path_attr


def get_attr_only_str(full_str):
    if "data" in full_str:
        mod = 0
    elif "[" in full_str:
        mod = 1
    else:
        mod = 0

    len_path = len(full_str.rsplit(".", config.MAX_NUMBER_OF_SUBPANELS)) - mod
    list_parent_nodes_str = full_str.rsplit(".", len_path - 3)
    attribute_only_str = full_str.replace(list_parent_nodes_str[0] + ".", "")
    return attribute_only_str


# ----------------------
# Main panel
# ---------------------
class MainPanelRandomUD(TemplatePanel):
    """Parent panel to the user defined properties subpanels

    Parameters
    ----------
    TemplatePanel : bpy.types.Panel
        base panel containing parts of the metadata common
        to all panels

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = "UD_PROPS_PT_mainpanel"
    bl_label = "Randomise UD"

    @classmethod
    def poll(cls, context):
        """Determine whether the panel can be displayed.

        This panel is only displayed if there is an active object

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        boolean
            True if there is an active object, False otherwise
        """
        return context.object is not None

    def draw(self, context):
        """Define the content to display in the main panel

        Parameters
        ----------
        context : _type_
            _description_
        """
        column = self.layout.column(align=True)
        column.label(text=("Add properties to randomise"))


class SubPanelUDUIlist(TemplatePanel):
    """Panel containing the UI list

    Parameters
    ----------
    TemplatePanel : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = "UD_PT_subpanel_UIlist"
    bl_parent_id = "UD_PROPS_PT_mainpanel"
    bl_label = ""  # title of the panel displayed to the user
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        """Determine whether the panel can be displayed.

        This panel is only displayed if there is an active object

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        boolean
            True if there is an active object, False otherwise
        """
        return context.object is not None

    def draw(self, context):
        column = self.layout.column(align=True)
        column.label(
            text="Choose property to see available properties to randomise"
        )

        layout = self.layout
        scn = bpy.context.scene

        rows = 2
        row = self.layout.row()
        row.template_list(
            "CUSTOM_UL_items",
            "",
            scn,
            "custom",
            scn,
            "custom_index",
            rows=rows,
        )

        col = row.column(align=True)
        col.operator(
            "custom.list_action", icon="ZOOM_IN", text=""
        ).action = "ADD"
        col.operator(
            "custom.list_action", icon="ZOOM_OUT", text=""
        ).action = "REMOVE"

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("custom.print_items", icon="LINENUMBERS_ON")
        row = col.row(align=True)
        row.operator("custom.clear_list", icon="X")


# ------------------------------
# Subpanel for each user defined property
# -----------------------------
class SubPanelRandomUD(TemplatePanel):
    """Parent class for the user defined properties
    subpanels

    Parameters
    ----------
    TemplatePanel : bpy.types.Panel
        base panel containing parts of the metadata common
        to all panels

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = "UD_PROPS_PT_subpanel"
    bl_parent_id = "UD_PROPS_PT_mainpanel"
    bl_label = ""  # title of the panel displayed to the user
    bl_options = {"DEFAULT_CLOSED"}
    # NOTE: other bl_options in the link below
    # https://docs.blender.org/api/master/bpy.types.Panel.html#bpy.types.Panel.bl_options

    @classmethod
    def poll(cls, context):
        """Determine whether the UD props subpanel can be displayed.

        To display a subpanel, its index must be lower than the
        total number of UD props defined in the scene and
        the property must be a valid property i.e. not a dummy
        property

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        cs = context.scene

        # force an update on the UD props collection first
        if cs.socket_props_per_UD.update_UD_props_collection:
            print("Collection of UD props updated")

        if cls.subpanel_UD_idx < len(cs.socket_props_per_UD.collection):
            sockets_props_collection = cs.socket_props_per_UD.collection[
                cls.subpanel_UD_idx
            ]

            full_str = sockets_props_collection.name
            attribute_only_str = get_attr_only_str(full_str)

            objects_in_scene = []
            for key in bpy.data.objects:
                objects_in_scene.append(key.name)

            if "[" in full_str:
                obj_str = get_obj_str(full_str)

                for i, obj in enumerate(objects_in_scene):
                    if obj in obj_str:
                        current_obj = obj
                        idx = i

                if "Camera" in current_obj:
                    action = attr_get_type(
                        bpy.data.cameras[idx],
                        attribute_only_str,
                    )[1]

                else:
                    action = attr_get_type(
                        bpy.data.objects[idx],
                        attribute_only_str,
                    )[1]

            elif "bpy.context.scene" in full_str:
                action = attr_get_type(bpy.context.scene, attribute_only_str)[
                    1
                ]

        else:
            action = "dummy"

        return action != "dummy"

    def draw_header(self, context):
        """Define header for the UD subpanel

        The header shows the name of the associated user defined
        property
        Parameters
        ----------
        context : _type_
            _description_
        """
        cs = context.scene

        # get this subpanel's UD prop
        cs.socket_props_per_UD.collection[self.subpanel_UD_idx]

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

    def draw(self, context):
        """Define the content to display in the UD prop subpanel

        Parameters
        ----------
        context : _type_
            _description_
        """
        cs = context.scene

        # get this subpanel's UD prop
        cs.socket_props_per_UD.collection[self.subpanel_UD_idx]

        # get (updated) collection of chosen prop for this subpanel
        sockets_props_collection = cs.socket_props_per_UD.collection[
            self.subpanel_UD_idx
        ]

        # Get list of UD props to randomise for this subpanel's UD prop
        full_str = sockets_props_collection.name
        attribute_only_str = get_attr_only_str(full_str)

        # list_all_UD_props = []
        # for UD_str in bpy.context.scene.custom:
        #     objects_in_scene = []
        #     for key in bpy.data.objects:
        #         objects_in_scene.append(key.name)

        #     if "[" in UD_str.name:
        #         obj_str = get_obj_str(UD_str.name)

        #         for i, obj in enumerate(objects_in_scene):
        #             if obj in obj_str:
        #                 current_obj = obj
        #                 idx = i

        #         if "Camera" in current_obj:
        #             if (
        #                 attr_get_type(
        #                     bpy.data.cameras[idx],
        #                     get_attr_only_str(UD_str.name),
        #                 )[1]
        #                 != "dummy"
        #             ):
        #                 list_all_UD_props.append(UD_str)

        #         else:
        #             if (
        #                 attr_get_type(
        #                     bpy.data.objects[idx],
        #                     get_attr_only_str(UD_str.name),
        #                 )[1]
        #                 != "dummy"
        #             ):
        #                 list_all_UD_props.append(UD_str)

        #     elif (
        #         attr_get_type(
        #             bpy.context.scene, get_attr_only_str(UD_str.name)
        #         )[1]
        #         != "dummy"
        #     ):
        #         list_all_UD_props.append(UD_str)

        # list_current_UD_props = list_all_UD_props[
        #     bpy.context.scene.custom_index
        # ].name

        list_current_UD_props = sockets_props_collection.name

        # Draw UD props to randomise including their
        # min/max boundaries
        draw_sockets_list_UD(
            cs,
            self.layout,
            list_current_UD_props,
            sockets_props_collection,
            attribute_only_str,
            full_str,
        )


# -------------------------------------------
# Subpanel for the 'randomise-all' operator
# -------------------------------------------
class SubPanelRandomUDOperator(TemplatePanel):
    """Panel containing the 'randomise-all' button

    Parameters
    ----------
    TemplatePanel : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """

    bl_idname = "UD_PT_subpanel_operator"
    bl_parent_id = "UD_PROPS_PT_mainpanel"
    bl_label = ""  # title of the panel displayed to the user
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        """Determine whether the panel can be displayed.

        This panel is only displayed if there is an active object

        Parameters
        ----------
        context : _type_
            _description_

        Returns
        -------
        boolean
            True if there is an active object, False otherwise
        """
        return context.object is not None

    def draw(self, context):
        """Define the content to display in the
        randomise-all operator panel

        Parameters
        ----------
        context : _type_
            _description_
        """
        column = self.layout.column(align=True)
        column.operator(
            "node.randomise_all_ud_sockets",
            text="Randomise",
        )


# -----------------------
# Classes to register
# ---------------------

# add Main panel to the list of classes to register
list_classes_to_register = [
    MainPanelRandomUD,
    CUSTOM_UL_items,
]

# Define (dynamically) a subpanel class for each UD prop
# and add them to the list of classes to register
# NOTE: because we don't know the number of UD props that will be
# defined a priori, we define n=MAX_NUMBER_OF_SUBPANELS classes and
# assign an index to each of them. We will only display the subpanels
# whose index is lower than the total number of UD props defined in the scene.
for i in range(config.MAX_NUMBER_OF_SUBPANELS):
    subpanel_class_i = type(
        f"UD_PT_subpanel_{i}",
        (SubPanelRandomUD,),
        {
            "bl_idname": f"UD_PT_subpanel_{i}",
            "subpanel_UD_idx": i,
        },
    )

    # append to list of classes to register
    list_classes_to_register.append(subpanel_class_i)  # type: ignore


# add Subpanel with operator to the list
# NOTE: to render it as the last panel
# we add it as the last one to the list
list_classes_to_register.append(SubPanelUDUIlist)
list_classes_to_register.append(SubPanelRandomUDOperator)


# -----------------------------------------
# Register and unregister functions
# ------------------------------------------
def register():
    for cls in list_classes_to_register:
        bpy.utils.register_class(cls)
    print("UD props UI registered")


def unregister():
    for cls in list_classes_to_register:
        bpy.utils.unregister_class(cls)
    print("UD props UI unregistered")
