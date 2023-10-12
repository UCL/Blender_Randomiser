import bpy

from .. import config
from ..material.ui import TemplatePanel  # draw_sockets_list


# ---------------------------------------------------
# Custom UIlist items
# ----------------------------------------------------
class CUSTOM_UL_items(bpy.types.UIList):
    print("hello UIlist")

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
# Common layout for list of sockets to randomise
# ----------------------------------------------------
def draw_sockets_list_UD(
    cs,
    layout,
    list_UD_props,
    sockets_props_collection,
    attribute_only_str,
    full_str,
):
    # Define UI fields for every socket property
    # NOTE: if I don't sort the input nodes, everytime one of the nodes is
    # selected in the graph it moves to the bottom of the panel.
    list_UD_props_sorted = list_UD_props
    # sorted(list_UD_props, key=lambda x: x.name)
    # print("IN draw_sockets_list_UD ==== ", list_UD_props_sorted)
    # for i_n, UD_str in enumerate(list_UD_props_sorted):
    row = layout.row()

    # if first node: add labels for
    # name, min, max and randomisation toggle
    # if i_n == 0:
    row_split = row.split()
    col1 = row_split.column(align=True)
    row_split.column(align=True)
    col3 = row_split.column(align=True)
    col4 = row_split.column(align=True)
    row_split.column(align=True)

    # input node name
    # print(list_UD_props_sorted)
    col1.label(text=sockets_props_collection.name)  # UD.name
    col1.alignment = "CENTER"

    # min label
    col3.alignment = "CENTER"
    col3.label(text="min")

    # max label
    col4.alignment = "CENTER"
    col4.label(text="max")

    # if not first node: add just node name
    # else:
    #     row.separator(factor=1.0)  # add empty row before each node
    #     row = layout.row()

    #     row.label(text=UD_str) #UD.name

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

    # socket current value
    # if "bpy.context.scene" in full_str:
    #     col2.prop(
    #         getattr(
    #             bpy.context.scene,
    #             attribute_only_str
    #         )
    #     # sockets_props_collection,
    #     # "default_value", #####Default value not found
    #     # icon_only=True,
    #     )
    # elif "bpy.data.objects" in full_str:
    #     col2.prop(
    #         getattr(
    #             bpy.data.objects["Cube"],
    #             attribute_only_str
    #         )
    #     )
    # col2.enabled = False  # current value is not editable

    # # socket min and max columns
    # socket_id = UD.name + "_" + sckt.name
    # if (UD.id_data.name in bpy.data.node_groups) and (
    #     bpy.data.node_groups[UD.id_data.name].type != "GEOMETRY"
    # ):  # only for SHADER groups
    #     socket_id = UD.id_data.name + "_" + socket_id

    # if socket is a color: format min/max as a color picker
    # and an array (color picker doesn't include alpha value)
    sckt = list_UD_props_sorted  # UD.name
    if type(sckt) == bpy.types.NodeSocketColor:
        for m_str, col in zip(["min", "max"], [col3, col4]):
            # color picker
            col.template_color_picker(
                sockets_props_collection,  # [socket_id],
                m_str + "_" + cs.socket_type_to_attr[type(sckt)],
            )
            # array
            for j, cl in enumerate(["R", "G", "B", "alpha"]):
                col.prop(
                    sockets_props_collection,  # [socket_id],
                    m_str + "_" + cs.socket_type_to_attr[type(sckt)],
                    icon_only=False,
                    text=cl,
                    index=j,
                )
    # if socket is Boolean: add non-editable labels
    elif type(sckt) == bpy.types.NodeSocketBool:
        for m_str, col in zip(["min", "max"], [col3, col4]):
            m_val = getattr(
                sockets_props_collection,  # [socket_id],
                m_str + "_" + cs.socket_type_to_attr[type(sckt)],
            )
            col.label(text=str(list(m_val)[0]))

    # if socket is not color type: format as a regular property

    ##### REFACTOR EASY CASE FIRST
    # (may not need other cases)
    else:  # bpy.types.NodeSocketBool:
        objects_in_scene = []
        for key in bpy.data.objects:
            objects_in_scene.append(key.name)

        for m_str, col in zip(["min", "max"], [col3, col4]):
            print(
                "DRAW SOCKETS LIST sockets_props_collection.name ====== ",
                sockets_props_collection.name,
            )
            if "[" in sockets_props_collection.name:
                print(
                    "DRAW SOCKETS LIST sockets_props_collection.name ====== ",
                    sockets_props_collection.name,
                )
                print(
                    "DRAW SOCKETS LIST attribute_only_str ====== ",
                    attribute_only_str,
                )

                obj_str = get_obj_str(sockets_props_collection.name)
                # print(obj_str)

                for i, obj in enumerate(objects_in_scene):
                    #        regex=re.compile(r'^test-\d+$')

                    if obj in obj_str:
                        current_obj = obj
                        # print("Found ", current_obj)

                        idx = i
                # attr_type = attr_get_type(
                #     bpy.context.scene.objects["Cube"], attribute_only_str
                # )[0]
                if "Camera" in current_obj:
                    attr_type = attr_get_type(
                        bpy.data.cameras[idx], attribute_only_str
                    )[0]
                else:
                    attr_type = attr_get_type(
                        bpy.data.objects[idx], attribute_only_str
                    )[0]
                print("DRAW SOCKETS LIST attr_type ====== ", attr_type)
            else:
                print(
                    "DRAW SOCKETS LIST sockets_props_collection.name ====== ",
                    sockets_props_collection.name,
                )
                print(
                    "DRAW SOCKETS LIST attribute_only_str ====== ",
                    attribute_only_str,
                )
                attr_type = attr_get_type(
                    bpy.context.scene, attribute_only_str
                )[0]
                print("DRAW SOCKETS LIST attr_type ====== ", attr_type)

            # print(
            #     "sockets_props_collection ???????",
            #     sockets_props_collection,
            # )
            # print("type ??????????? ", attribute_only_str, attr_type)

            print("ERROR HERE in line 172 of ui.py")
            col.prop(
                sockets_props_collection,  # [socket_id],
                m_str + "_" + cs.UD_prop_to_attr[attr_type],
                icon_only=True,
            )
            # np.array(getattr(self, m_str + "_min"))
            # getattr(context.scene.camera, location)[0]
            # e.g. min_float_1d so m_str + "_" + float_1d

    # randomisation toggle
    col5.prop(
        sockets_props_collection,  # [socket_id],
        "bool_randomise",
        icon_only=True,
    )


def get_obj_str(full_str):
    x = full_str.split(".")
    # print(path_prop)
    for i in x:
        if "[" in i:
            ii = i.split("[")
            object_str = ii[1]
            object_str = object_str[:-1]

    return object_str


def attr_get_type(obj, path):
    # if '[' in path:
    #     print(' [ is in path')

    if "." in path:
        # gives us: ('modifiers["Subsurf"]', 'levels')
        # len_path = len(full_str.rsplit(".", config.MAX_NUMBER_OF_SUBPANELS))
        path_prop, path_attr = path.rsplit(".", 1)

        # print("if statement ==== ")
        # print(
        #     "FROM rsplit . path_prop for resolve = ",
        #     path_prop,
        #     " and path_attr  for getattr = ",
        #     path_attr,
        # )
        # print("obj used for path_resolve = ", obj)

        # same as: prop = obj.modifiers["Subsurf"]
        prop = obj.path_resolve(path_prop)
        # print("prop from path_resolve  for get_attr = ", prop)
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
        # print(action, prop, path_attr)
        # print(type(action))
    # action = getattr(prop, path_attr)

    return type(action), action, prop, path_attr
    # setattr(prop, path_attr, value)


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
class MainPanelRandomUD(
    TemplatePanel
):  # MainPanelRandomGeometryNodes(TemplatePanel):
    """Parent panel to the geometry node groups' subpanels

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

    bl_idname = "UD_PROPS_PT_mainpanel"  # "NODE_GEOMETRY_PT_mainpanel"
    bl_label = "Randomise UD"  # "Randomise GEOMETRY"

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
        # column.prop(context.scene.custom_props, "custom_input", text="")
        # column.operator("opr.add_custom_prop_to_list",
        # text="Add to Custom List")

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
        # col.separator()
        # col.operator(
        #     "custom.list_action", icon="TRIA_UP", text=""
        # ).action = "UP"
        # col.operator(
        #     "custom.list_action", icon="TRIA_DOWN", text=""
        # ).action = "DOWN"

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator(
            "custom.print_items", icon="LINENUMBERS_ON"
        )  # LINENUMBERS_OFF, ANIM
        row = col.row(align=True)
        row.operator("custom.clear_list", icon="X")


# ------------------------------
# Subpanel for each node group
# -----------------------------
class SubPanelRandomUD(
    TemplatePanel
):  # SubPanelRandomGeometryNodes(TemplatePanel):
    """Parent class for the geometry node groups' (GNG)
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
        """Determine whether the GNG subpanel can be displayed.

        To display a subpanels, its index must be lower than the
        total number of GNGs defined in the scene

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

        ##### CHECK VALID PROPERTY
        # force an update on the group nodes collection first
        if cs.socket_props_per_UD.update_UD_props_collection:
            print("Collection of UD props updated")

        if cls.subpanel_UD_idx < len(cs.socket_props_per_UD.collection):
            # pdb.set_trace()
            sockets_props_collection = cs.socket_props_per_UD.collection[
                cls.subpanel_UD_idx
            ]

            full_str = sockets_props_collection.name
            attribute_only_str = get_attr_only_str(full_str)
            print("SUBPANEL poll attribute_only_str ", attribute_only_str)

            objects_in_scene = []
            for key in bpy.data.objects:
                objects_in_scene.append(key.name)

            if "[" in full_str:
                obj_str = get_obj_str(full_str)
                # print(obj_str)

                for i, obj in enumerate(objects_in_scene):
                    #        regex=re.compile(r'^test-\d+$')

                    if obj in obj_str:
                        current_obj = obj
                        # print("Found ", current_obj)

                        idx = i

                if "Camera" in current_obj:
                    prop_type, action, prop, path_attr = attr_get_type(
                        bpy.data.cameras[idx], attribute_only_str
                    )[0]

                else:
                    prop_type, action, prop, path_attr = attr_get_type(
                        bpy.data.objects[idx], attribute_only_str
                    )[0]
                    # prop_type, action, prop, path_attr = attr_get_type(
                    #     bpy.data.objects["Cube"], attribute_only_str
                    # )[0]

            elif "bpy.context.scene" in full_str:
                prop_type, action, prop, path_attr = attr_get_type(
                    bpy.context.scene, attribute_only_str
                )[0]

            # print("prop_type", prop_type)
            # print("action", action)
            # print("prop", prop)
            # print("path_attr", path_attr)

        else:
            action = "dummy"
            # bpy.ops.custom.list_action(action='UP')
            # pdb.set_trace()
            # print('action',action)

        return action != "dummy"

    # , getattr(prop, path_attr, None)
    # clc.subpanel defined in operators.py
    # only display subpanels for which this is true

    def draw_header(
        self, context
    ):  # maybe needed for the name of custom props
        # but no need graph to be displayed
        """Define header for the GNG subpanel

        The header shows the name of the associated geometry node group
        (GNG) inside a button. The button is linked to the view-graph
        operator.

        Parameters
        ----------
        context : _type_
            _description_
        """
        cs = context.scene

        # get this subpanel's GNG
        cs.socket_props_per_UD.collection[self.subpanel_UD_idx]

        # add view graph operator to layout
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        # layout.operator(
        #     f"node.view_graph_for_gng_{self.subpanel_UD_prop_idx}",
        #     text=subpanel_UD_prop.name,
        #     emboss=True,
        # )  #operator defined once node.view_graph_for_gng
        # # - not needed for custom props?

    def draw(self, context):
        """Define the content to display in the GNG subpanel

        Parameters
        ----------
        context : _type_
            _description_
        """
        cs = context.scene

        # get this subpanel's GNG
        cs.socket_props_per_UD.collection[self.subpanel_UD_idx]

        # print("subpanel_UD_prop = ", subpanel_UD_prop)
        # print("self.subpanel_UD_idx = ", self.subpanel_UD_idx)

        # # force an update
        # (##### CHECK VALID PROPERTY orchecked elsewhere?)
        # if cs.socket_props_per_UD[
        #     self.subpanel_UD_idx
        # ].update_collection:
        #     print("Collection of UD properties updated")

        # get (updated) collection of chosen propr for this subpanel
        sockets_props_collection = cs.socket_props_per_UD.collection[
            self.subpanel_UD_idx
        ]  # .collection

        # print("sockets_props_collection = ", sockets_props_collection)
        # print(" and name ========== ", sockets_props_collection.name)

        # # Get list of input nodes to randomise for this subpanel's GNG
        # [sckt.name.split("_")[0] for sckt in sockets_props_collection]

        # Get list of input nodes to randomise for this subpanel's GNG
        full_str = sockets_props_collection.name
        attribute_only_str = get_attr_only_str(full_str)

        # len_path = len(full_str.rsplit(".", config.MAX_NUMBER_OF_SUBPANELS))
        # list_parent_nodes_str = full_str.rsplit(".", len_path - 3)
        # attribute_only_str = full_str.replace(
        #     list_parent_nodes_str[0] + ".", ""
        # )

        # print("list_parent_nodes_str = ", attribute_only_str)

        # full_list = [prop.name for prop in list(C.scene.custom)]
        list_all_UD_props = []
        for UD_str in bpy.context.scene.custom:
            # print("ERROR ====== UD_str", UD_str)
            objects_in_scene = []
            for key in bpy.data.objects:
                objects_in_scene.append(key.name)

            if "[" in UD_str.name:
                obj_str = get_obj_str(UD_str.name)
                # print(obj_str)

                for i, obj in enumerate(objects_in_scene):
                    #        regex=re.compile(r'^test-\d+$')

                    if obj in obj_str:
                        current_obj = obj
                        # print("Found ", current_obj)

                        idx = i

                # if (
                #     attr_get_type(
                #         bpy.data.objects["Cube"],
                #         get_attr_only_str(UD_str.name),
                #     )[1]
                #     != "dummy"
                # ):

                if "Camera" in current_obj:
                    if (
                        attr_get_type(
                            bpy.data.cameras[idx],
                            get_attr_only_str(UD_str.name),
                        )[1]
                        != "dummy"
                    ):
                        list_all_UD_props.append(UD_str)

                else:
                    if (
                        attr_get_type(
                            bpy.data.objects[idx],
                            get_attr_only_str(UD_str.name),
                        )[1]
                        != "dummy"
                    ):
                        list_all_UD_props.append(UD_str)

            elif (
                attr_get_type(
                    bpy.context.scene, get_attr_only_str(UD_str.name)
                )[1]
                != "dummy"
            ):
                list_all_UD_props.append(UD_str)
        # list_all_UD_props = [
        #     UD_str
        #     for UD_str in list(bpy.context.scene.custom)
        #     if attr_get_type(
        #         bpy.context.scene, get_attr_only_str(UD_str.name)
        #     )[1]
        #     != "dummy"
        # ]
        # print("list_all_UD_props ====== ", list_all_UD_props)
        # print(
        #     "bpy.context.scene.custom_index == ",
        #     bpy.context.scene.custom_index,
        # )
        list_current_UD_props = list_all_UD_props[
            bpy.context.scene.custom_index
        ].name
        # print("list_current_UD_props =======", list_current_UD_props)

        # Draw sockets to randomise per input node, including their
        # current value and min/max boundaries
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
class SubPanelRandomUDOperator(
    TemplatePanel
):  # SubPanelRandomGeometryOperator(TemplatePanel): #RANDOMISATION
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

    bl_idname = (
        "UD_PT_subpanel_operator"  # "NODE_GEOMETRY_PT_subpanel_operator"
    )
    bl_parent_id = "UD_PROPS_PT_mainpanel"  # "NODE_GEOMETRY_PT_mainpanel"
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
            "opr.randomise_all_ud_sockets",
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

# Define (dynamically) a subpanel class for each Geometry Node Group (GNGs)
# and add them to the list of classes to register
# NOTE: because we don't know the number of GNGs that will be
# defined a priori, we define n=MAX_NUMBER_OF_SUBPANELS classes and
# assign an index to each of them. We will only display the subpanels
# whose index is lower than the total number of GNGs defined in the scene.
for i in range(config.MAX_NUMBER_OF_SUBPANELS):
    # define subpanel class for GNG i
    # subpanel_class_i = type(
    #     f"NODE_GEOMETRY_PT_subpanel_{i}",
    #     (SubPanelRandomGeometryNodes,),
    #     {
    #         "bl_idname": f"NODE_GEOMETRY_PT_subpanel_{i}",
    #         "subpanel_gng_idx": i,
    #     },
    # )
    subpanel_class_i = type(
        f"UD_PT_subpanel_{i}",
        (SubPanelRandomUD,),
        {
            "bl_idname": f"UD_PT_subpanel_{i}",
            "subpanel_UD_idx": i,  # IN UI AND OPERATORS
        },
    )

    # append to list of classes to register
    list_classes_to_register.append(subpanel_class_i)  # type: ignore


# add Subpanel with operator to the list
# NOTE: to render it as the last panel
# we add it as the last one to the list
list_classes_to_register.append(SubPanelUDUIlist)
list_classes_to_register.append(SubPanelRandomUDOperator)


#     SubPanelRandomUDOperator,
#     SubPanelUDUIlist
# )


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
