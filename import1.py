import gmsh

gmsh.initialize()
gmsh.model.add("My STEP Model")

# ============================================================
# IMPORT STEP
# ============================================================

parts = gmsh.model.occ.importShapes(
    "Assembly.step",
    highestDimOnly=True
)

gmsh.model.occ.synchronize()


# ============================================================
# IMPORTED ENTITIES
# ============================================================

print("\n==============================")
print("IMPORTED ENTITIES")
print("==============================")

for dim, tag in parts:
    name = gmsh.model.getEntityName(dim, tag)

    print(
        f"Dimension: {dim} | "
        f"Tag: {tag} | "
        f"Name: '{name}'"
    )


# ============================================================
# GENERATE MESH
# ============================================================

gmsh.model.mesh.generate(3)


# ============================================================
# NODES
# ============================================================

print("\n==============================")
print("NODES")
print("==============================")

node_tags, node_coords, _ = gmsh.model.mesh.getNodes()

print(f"Total nodes: {len(node_tags)}")

for i in range(min(20, len(node_tags))):

    x = node_coords[3*i]
    y = node_coords[3*i + 1]
    z = node_coords[3*i + 2]

    print(
        f"Node {node_tags[i]}: "
        f"({x:.6g}, {y:.6g}, {z:.6g})"
    )

if len(node_tags) > 20:
    print("...")


# ============================================================
# CAD VOLUMES
# ============================================================

print("\n==============================")
print("CAD VOLUMES")
print("==============================")

volumes = gmsh.model.getEntities(3)

for dim, volume_tag in volumes:

    name = gmsh.model.getEntityName(dim, volume_tag)

    print(
        f"\nVolume {volume_tag}: "
        f"'{name}'"
    )

    # Get CAD surfaces bounding this volume
    boundary = gmsh.model.getBoundary(
        [(3, volume_tag)],
        oriented=False,
        recursive=False
    )

    print("  Bounding surfaces:")

    for surface_dim, surface_tag in boundary:

        surface_name = gmsh.model.getEntityName(
            surface_dim,
            surface_tag
        )

        print(
            f"    Surface {surface_tag}: "
            f"'{surface_name}'"
        )


# ============================================================
# CAD SURFACES
# ============================================================

print("\n==============================")
print("CAD SURFACES")
print("==============================")

surfaces = gmsh.model.getEntities(2)

for dim, surface_tag in surfaces:

    name = gmsh.model.getEntityName(dim, surface_tag)

    print(
        f"\nSurface {surface_tag}: "
        f"'{name}'"
    )

    # Which volumes touch this surface?
    adjacent_volumes = []

    for _, volume_tag in volumes:

        boundary = gmsh.model.getBoundary(
            [(3, volume_tag)],
            oriented=False,
            recursive=False
        )

        if (2, surface_tag) in boundary:
            adjacent_volumes.append(volume_tag)

    print(
        f"  Adjacent volumes: "
        f"{adjacent_volumes}"
    )


# ============================================================
# 3D MESH ELEMENTS
# ============================================================

print("\n==============================")
print("3D MESH ELEMENTS / FVM CELLS")
print("==============================")

for _, volume_tag in volumes:

    print(
        f"\n--- Volume {volume_tag} ---"
    )

    element_types, element_tags, element_nodes = \
        gmsh.model.mesh.getElements(
            3,
            volume_tag
        )

    for j, element_type in enumerate(element_types):

        name, dim, order, num_nodes, _, num_primary_nodes = \
            gmsh.model.mesh.getElementProperties(
                element_type
            )

        tags = element_tags[j]
        nodes = element_nodes[j]

        print(
            f"Element type: {name}"
        )

        print(
            f"Number of elements: {len(tags)}"
        )

        print(
            f"Nodes per element: {num_nodes}"
        )

        # Print first 10 elements
        for i in range(min(10, len(tags))):

            start = i * num_nodes
            end = start + num_nodes

            connectivity = nodes[start:end]

            print(
                f"  Element {tags[i]}: "
                f"nodes {connectivity}"
            )

        if len(tags) > 10:
            print("  ...")


# ============================================================
# 2D MESH ELEMENTS / FACES
# ============================================================

print("\n==============================")
print("2D MESH ELEMENTS / FACES")
print("==============================")

for _, surface_tag in surfaces:

    print(
        f"\n--- Surface {surface_tag} ---"
    )

    element_types, element_tags, element_nodes = \
        gmsh.model.mesh.getElements(
            2,
            surface_tag
        )

    for j, element_type in enumerate(element_types):

        name, dim, order, num_nodes, _, num_primary_nodes = \
            gmsh.model.mesh.getElementProperties(
                element_type
            )

        tags = element_tags[j]
        nodes = element_nodes[j]

        print(
            f"Element type: {name}"
        )

        print(
            f"Number of faces: {len(tags)}"
        )

        print(
            f"Nodes per face: {num_nodes}"
        )

        for i in range(min(5, len(tags))):

            start = i * num_nodes
            end = start + num_nodes

            connectivity = nodes[start:end]

            print(
                f"  Face element {tags[i]}: "
                f"nodes {connectivity}"
            )

        if len(tags) > 5:
            print("  ...")


# ============================================================
# ALL ELEMENT TYPES
# ============================================================

print("\n==============================")
print("ELEMENT TYPES")
print("==============================")

for element_type in gmsh.model.mesh.getElementTypes():

    name, dim, order, num_nodes, local_coords, num_primary_nodes = \
        gmsh.model.mesh.getElementProperties(
            element_type
        )

    print(
        f"Type {element_type}: "
        f"{name} | "
        f"dimension={dim} | "
        f"order={order} | "
        f"nodes={num_nodes}"
    )


# ============================================================
# GUI
# ============================================================

gmsh.fltk.run()

gmsh.finalize()
