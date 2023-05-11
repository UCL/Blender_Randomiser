# Parameters shared across materials modules


# MAX_NUMBER_OF_SUBPANELS: upper limit for the expected
# number of *materials* in a scene.
# This number of subpanels will be defined as classes, but
# only those panels with index < total number of materials
# will be displayed.
MAX_NUMBER_OF_SUBPANELS = 100

# MAX_NUMBER_OF_SUBSUBPANELS: upper limit for the expected
# number of *group nodes in a single material*.
# A total of MAX_NUMBER_OF_SUBPANELS*MAX_NUMBER_OF_SUBSUBPANELS subsubpanels
# will be defined as classes, but only those panels with
# index < total number of group nodes per material
# will be displayed.
MAX_NUMBER_OF_SUBSUBPANELS = 100
