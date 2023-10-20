## User Defined Properties Panel

![UD_props_panel](/docs/images/UD_panel.png)

This example panel set-up can produce an [output_file](/output_randomisations_per_frame1697817657.502794_UD_example.json)

Some examples of useful user-defined properties could be:
- bpy.data.objects["Cube"].location (Float 3D)
- bpy.context.scene.frame_current (int 1D)
- bpy.data.objects["Sphere"].scale (Float 3D)
- bpy.data.objects["Cube"].collision.absorption (Float 1D)
- bpy.data.cameras["Camera"].dof.aperture_fstop (Float 1D)
- bpy.data.objects["Cube"].rotation_euler (Euler)


> [!WARNING]
>  - bpy.data.objects["Cube"].location[0] or bpy.data.cameras["Camera"].location[0] will throw an error if trying to add to the UD panel.
bpy.data.objects["Cube"].location will work fine and if you only want to change the x-location then you can leave the y-/z-location bounds as 0 (min) to 0 (max) and the Cube won't be moved in those directions.
> - Another example that will not work is if the object has a '.' in the middle of the name i.e. "Cube.001" so please remove this if you want to have multiple cubes in your scene.
