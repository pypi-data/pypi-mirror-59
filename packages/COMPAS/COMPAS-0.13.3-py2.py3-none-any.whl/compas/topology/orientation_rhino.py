from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from Rhino.Geometry import RTree
from Rhino.Geometry import Sphere
from Rhino.Geometry import Point3d

from compas.utilities import pairwise
from compas.geometry import centroid_points
from compas.topology import breadth_first_traverse


__all__ = [
    'face_adjacency_rhino',
    'unify_cycles_rhino',
]


def unify_cycles_rhino(vertices, faces, root=0):
    """"""
    def unify(node, nbr):
        # find the common edge
        for u, v in pairwise(faces[nbr] + faces[nbr][0:1]):
            if u in faces[node] and v in faces[node]:
                # node and nbr have edge u-v in common
                i = faces[node].index(u)
                j = faces[node].index(v)
                if i == j - 1 or (j == 0 and u == faces[node][-1]):
                    # if the traversal of a neighboring halfedge
                    # is in the same direction
                    # flip the neighbor
                    faces[nbr][:] = faces[nbr][::-1]
                    return

    adj = face_adjacency_rhino(vertices, faces)

    visited = breadth_first_traverse(adj, root, unify)

    assert len(list(visited)) == len(faces), 'Not all faces were visited'
    return faces


def face_adjacency_rhino(xyz, faces):
    f = len(faces)

    if f > 100:
        return _face_adjacency(xyz, faces)

    adjacency = {}

    for face, vertices in enumerate(faces):
        nbrs = []
        found = set()

        for u, v in pairwise(vertices + vertices[0:1]):
            for nbr, _ in enumerate(faces):

                if nbr == face:
                    continue
                if nbr in found:
                    continue

                for a, b in pairwise(faces[nbr] + faces[nbr][0:1]):
                    if v == a and u == b:
                        nbrs.append(nbr)
                        found.add(nbr)
                        break

                for a, b in pairwise(faces[nbr] + faces[nbr][0:1]):
                    if u == a and v == b:
                        nbrs.append(nbr)
                        found.add(nbr)
                        break

        adjacency[face] = nbrs

    return adjacency


def _face_adjacency(xyz, faces, nmax=10, radius=2.0):
    """"""
    points = [centroid_points([xyz[index] for index in face]) for face in faces]

    tree = RTree()
    for i, point in enumerate(points):
        tree.Insert(Point3d(* point), i)

    def callback(sender, e):
        data = e.Tag
        data.append(e.Id)

    closest = []
    for i, point in enumerate(points):
        sphere = Sphere(Point3d(* point), radius)
        data = []
        tree.Search(sphere, callback, data)
        closest.append(data)

    adjacency = {}

    for face, vertices in enumerate(faces):
        nbrs = []
        found = set()

        nnbrs = set(closest[face])

        for u, v in pairwise(vertices + vertices[0:1]):
            for nbr in nnbrs:

                if nbr == face:
                    continue
                if nbr in found:
                    continue

                for a, b in pairwise(faces[nbr] + faces[nbr][0:1]):
                    if v == a and u == b:
                        nbrs.append(nbr)
                        found.add(nbr)
                        break

                for a, b in pairwise(faces[nbr] + faces[nbr][0:1]):
                    if u == a and v == b:
                        nbrs.append(nbr)
                        found.add(nbr)
                        break

        adjacency[face] = nbrs

    return adjacency


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
