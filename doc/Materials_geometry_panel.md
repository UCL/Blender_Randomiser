## Materials
- A panel to randomise properties relative to the material nodes:
    - nodes and node groups are aggregated based on the material they belong to.
    - only materials with use_nodes=True are added to the panel. By default, use_nodes is set to True, but this is a convenient way to add/remove materials from the panel.
    - If new nodes that are marked for randomisation are added or deleted, these appear automatically in the randomisation panel.
    - Recursive node groups are accepted.
    - Convenience functions were added to visualise the node graph per material, constrain the min and max values for the randomisation and unselect nodes that are candidates for randomisation but are unlinked.

### When is a new material slot automatically added?
Clicking the name of the material in a subpanel header shows its node graph. If a material is clicked and it has no slot assigned, a new slot will be created for it



## Geometry
- A panel to randomise properties relative to the geometry nodes:
    - nodes are aggregated based on the node group they belong to.
    - Same functionalities as in material nodes panel: new or deleted nodes are automatically added, recursive node groups are accepted,etc.


### When is a new modifier automatically added to an object’s geometry?
If a geometry node group is not inside another node group, and is not linked to a modifier of the currently active object, a new modifier is created and the geometry node group is linked to it.
