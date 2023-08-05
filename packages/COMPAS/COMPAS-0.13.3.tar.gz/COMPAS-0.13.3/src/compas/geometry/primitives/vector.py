from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas import PRECISION

from compas.geometry.basic import length_vector
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import dot_vectors
from compas.geometry.angles import angle_vectors
from compas.geometry.angles import angle_vectors_signed
from compas.geometry.angles import angles_vectors

from compas.geometry.transformations import transform_vectors

from compas.geometry.primitives import Primitive

__all__ = ['Vector']


class Vector(Primitive):
    """A vector is defined by XYZ components and a homogenisation factor.

    Parameters
    ----------
    x : float
        The X component of the vector.
    y : float
        The Y component of the vector.
    z : float
        The Z component of the vector.
    precision : integer, optional
        The number of fractional digits used in the representation of the coordinates of the vector.
        Default is ``3``.

    Examples
    --------
    >>> u = Vector(1, 0, 0)
    >>> v = Vector(0, 1, 0)
    >>> u
    Vector(1.000, 0.000, 0.000)
    >>> v
    Vector(0.000, 1.000, 0.000)
    >>> u.x
    1.0
    >>> u[0]
    1.0
    >>> u.length
    1.0
    >>> u + v
    Vector(1.000, 1.000, 0.000)
    >>> u + [0.0, 1.0, 0.0]
    Vector(1.000, 1.000, 0.000)
    >>> u * 2
    Vector(2.000, 0.000, 0.000)
    >>> u.dot(v)
    0.0
    >>> u.cross(v)
    Vector(0.000, 0.000, 1.000)

    """

    __slots__ = ['_x', '_y', '_z']

    def __init__(self, x, y, z=0):
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def transform_collection(collection, X):
        """Transform a collection of ``Vector`` objects.

        Parameters
        ----------
        collection : list of compas.geometry.Vector
            The collection of vectors.

        Returns
        -------
        None
            The vectors are modified in-place.

        Examples
        --------
        >>> R = Rotation.from_axis_and_angle(Vector.Zaxis(), radians(90))
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> vectors = [u]
        >>> Vector.transform_collection(vectors, R)
        >>> v = vectors[0]
        >>> v
        Vector(0.000, 1.000, 0.000)
        >>> u is v
        True

        """
        data = transform_vectors(collection, X)
        for vector, xyz in zip(collection, data):
            vector.x = xyz[0]
            vector.y = xyz[1]
            vector.z = xyz[2]

    @staticmethod
    def transformed_collection(collection, X):
        """Create a collection of transformed ``Vector`` objects.

        Parameters
        ----------
        collection : list of compas.geometry.Vector
            The collection of vectors.

        Returns
        -------
        list of compas.geometry.Vector
            The transformed vectors.

        Examples
        --------
        >>> R = Rotation.from_axis_and_angle(Vector.Zaxis(), radians(90))
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> vectors = [u]
        >>> vectors = Vector.transformed_collection(vectors, R)
        >>> v = vectors[0]
        >>> v
        Vector(0.000, 1.000, 0.000)
        >>> u is v
        False

        """
        vectors = [vector.copy() for vector in collection]
        Vector.transform_collection(vectors, X)
        return vectors

    # ==========================================================================
    # factory
    # ==========================================================================

    @classmethod
    def Xaxis(cls):
        """Construct a unit vector along the X axis.

        Returns
        -------
        Vector
            A vector with components ``x = 1.0, y = 0.0, z = 0.0``.

        Examples
        --------
        >>> Vector.Xaxis()
        Vector(1.000, 0.000, 0.000)

        """
        return cls(1.0, 0.0, 0.0)

    @classmethod
    def Yaxis(cls):
        """Construct a unit vector along the Y axis.

        Returns
        -------
        Vector
            A vector with components ``x = 0.0, y = 1.0, z = 0.0``.

        Examples
        --------
        >>> Vector.Yaxis()
        Vector(0.000, 1.000, 0.000)

        """
        return cls(0.0, 1.0, 0.0)

    @classmethod
    def Zaxis(cls):
        """Construct a unit vector along the Z axis.

        Returns
        -------
        Vector
            A vector with components ``x = 0.0, y = 0.0, z = 1.0``.

        Examples
        --------
        >>> Vector.Zaxis()
        Vector(0.000, 0.000, 1.000)

        """
        return cls(0.0, 0.0, 1.0)

    @classmethod
    def from_start_end(cls, start, end):
        """Construct a ``Vector`` from start and end points.

        Parameters
        ----------
        start : point
            The start point.
        end : point
            The end point.

        Returns
        -------
        Vector
            The vector from start to end.

        """
        v = subtract_vectors(end, start)
        return cls(*v)

    @classmethod
    def from_data(cls, data):
        return cls(*data)

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def data(self):
        """Returns the data dictionary that represents the vector.

        Returns
        -------
        dict
            The vector's data.
        """
        return list(self)

    @data.setter
    def data(self, data):
        self.x = data[0]
        self.y = data[1]
        self.z = data[2]

    @property
    def x(self):
        """float: The X coordinate of the point."""
        return self._x

    @x.setter
    def x(self, x):
        self._x = float(x)

    @property
    def y(self):
        """float: The Y coordinate of the point."""
        return self._y

    @y.setter
    def y(self, y):
        self._y = float(y)

    @property
    def z(self):
        """float: The Z coordinate of the point."""
        return self._z

    @z.setter
    def z(self, z):
        self._z = float(z)

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Vector({0:.{3}f}, {1:.{3}f}, {2:.{3}f})'.format(self.x, self.y, self.z, PRECISION[:1])

    def __len__(self):
        return 3

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self[i] for i in range(*key.indices(len(self)))]
        i = key % 3
        if i == 0:
            return self.x
        if i == 1:
            return self.y
        if i == 2:
            return self.z
        raise KeyError

    def __setitem__(self, key, value):
        i = key % 3
        if i == 0:
            self.x = value
            return
        if i == 1:
            self.y = value
            return
        if i == 2:
            self.z = value
            return
        raise KeyError

    def __iter__(self):
        return iter([self.x, self.y, self.z])

    # ==========================================================================
    # comparison
    # ==========================================================================

    def __eq__(self, other):
        """Is this vector equal to the other vector? Two vectors are considered
        equal if their XYZ components are identical.

        Parameters
        ----------
        other : vector
            The vector to compare.

        Returns
        -------
        bool
            True if the vectors are equal.
            False otherwise.

        """
        return self.x == other[0] and self.y == other[1] and self.z == other[2]

    # ==========================================================================
    # operators
    # ==========================================================================

    def __add__(self, other):
        """Return a ``Vector`` that is the the sum of this ``Vector`` and another vector.

        Parameters
        ----------
        other : vector
            The vector to add.

        Returns
        -------
        Vector
            The resulting new ``Vector``.

        """
        return Vector(self.x + other[0], self.y + other[1], self.z + other[2])

    def __sub__(self, other):
        """Return a ``Vector`` that is the the difference between this ``Vector`` and another ``Vector``.

        Parameters
        ----------
        other : vector
            The vector to subtract.

        Returns
        -------
        Vector
            The resulting new ``Vector``.

        """
        return Vector(self.x - other[0], self.y - other[1], self.z - other[2])

    def __mul__(self, n):
        """Return a ``Vector`` that is the scaled version of this ``Vector``.

        Parameters
        ----------
        n : float
            The scaling factor.

        Returns
        -------
        Vector
            The resulting new ``Vector``.

        """
        return Vector(self.x * n, self.y * n, self.z * n)

    def __truediv__(self, n):
        """Return a ``Vector`` that is the scaled version of this ``Vector``.

        Parameters
        ----------
        n : float
            The scaling factor.

        Returns
        -------
        Vector
            The resulting new ``Vector``.

        """
        return Vector(self.x / n, self.y / n, self.z / n)

    def __pow__(self, n):
        """Create a ``Vector`` from the components of the current ``Vector`` raised
        to the given power.

        Parameters
        ----------
        n : float
            The power.

        Returns
        -------
        Vector
            A new point with raised coordinates.

        """
        return Vector(self.x ** n, self.y ** n, self.z ** n)

    # ==========================================================================
    # in-place operators
    # ==========================================================================

    def __iadd__(self, other):
        """Add the components of the other vector to this ``Vector``.

        Parameters
        ----------
        other : vector
            The vector to add.

        """
        self.x += other[0]
        self.y += other[1]
        self.z += other[2]
        return self

    def __isub__(self, other):
        """Subtract the components of the other vector from this ``Vector``.

        Parameters
        ----------
        other : vector
            The vector to subtract.

        """
        self.x -= other[0]
        self.y -= other[1]
        self.z -= other[2]
        return self

    def __imul__(self, n):
        """Multiply the components of this ``Vector`` by the given factor.

        Parameters
        ----------
        n : float
            The multiplication factor.

        """
        self.x *= n
        self.y *= n
        self.z *= n
        return self

    def __itruediv__(self, n):
        """Divide the components of this ``Vector`` by the given factor.

        Parameters
        ----------
        n : float
            The multiplication factor.

        """
        self.x /= n
        self.y /= n
        self.z /= n
        return self

    def __ipow__(self, n):
        """Raise the components of this ``Vector`` to the given power.

        Parameters
        ----------
        n : float
            The power.

        """
        self.x **= n
        self.y **= n
        self.z **= n
        return self

    # ==========================================================================
    # static methods
    # ==========================================================================

    @staticmethod
    def length_vectors(vectors):
        return [length_vector(vector) for vector in vectors]

    @staticmethod
    def sum_vectors(vectors):
        return Vector(* [sum(axis) for axis in zip(* vectors)])

    @staticmethod
    def dot_vectors(left, right):
        return [Vector.dot(u, v) for u, v in zip(left, right)]

    @staticmethod
    def cross_vectors(left, right):
        return [Vector.cross(u, v) for u, v in zip(left, right)]

    @staticmethod
    def angles_vectors(left, right):
        return [angles_vectors(u, v) for u, v in zip(left, right)]

    @staticmethod
    def angle_vectors(left, right):
        return [angle_vectors(u, v) for u, v in zip(left, right)]

    @staticmethod
    def angle_vectors_signed(left, right, normal):
        return [angle_vectors_signed(u, v, normal) for u, v in zip(left, right)]

    @staticmethod
    def homogenise_vectors(vectors):
        pass

    @staticmethod
    def dehomogenise_vectors(vectors):
        pass

    @staticmethod
    def orthonormalize_vectors(vectors):
        pass

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def length(self):
        """float: The length of this ``Vector``."""
        return length_vector(self)

    # ==========================================================================
    # helpers
    # ==========================================================================

    def copy(self):
        """Make a copy of this ``Vector``.

        Returns
        -------
        Vector
            The copy.

        """
        cls = type(self)
        return cls(self.x, self.y, self.z)

    # ==========================================================================
    # methods
    # ==========================================================================

    def unitize(self):
        """Scale this ``Vector`` to unit length."""
        length = self.length
        self.x = self.x / length
        self.y = self.y / length
        self.z = self.z / length

    def unitized(self):
        """Returns a unitized copy of this ``Vector``.

        Returns
        -------
        :class:`Vector`

        """
        v = self.copy()
        v.unitize()
        return v

    def scale(self, n):
        """Scale this ``Vector`` by a factor n.

        Parameters
        ----------
        n : float
            The scaling factor.

        """
        self.x *= n
        self.y *= n
        self.z *= n

    def scaled(self, n):
        """Returns a scaled copy of this ``Vector``.

        Parameters
        ----------
        n : float
            The scaling factor.

        Returns
        -------
        :class:`Vector`

        """
        v = self.copy()
        v.scale(n)
        return v

    def dot(self, other):
        """The dot product of this ``Vector`` and another vector.

        Parameters
        ----------
        other : vector
            The other vector.

        Returns
        -------
        float
            The dot product.

        """
        return dot_vectors(self, other)

    def cross(self, other):
        """The cross product of this ``Vector`` and another vector.

        Parameters
        ----------
        other : vector
            The other vector.

        Returns
        -------
        Vector
            The cross product.

        """
        return Vector(* cross_vectors(self, other))

    def angle(self, other):
        """Compute the smallest angle between this ``Vector`` and another vector.

        Parameters
        ----------
        other : vector
            The other vector.

        Returns
        -------
        float
            The smallest angle between the two vectors.

        """
        return angle_vectors(self, other)

    def angle_signed(self, other, normal):
        """Compute the signed angle between this ``Vector`` and another vector.

        Parameters
        ----------
        other : vector
            The other vector.
        normal : vector
            The plane's normal spanned by this and the other vector.

        Returns
        -------
        float
            The signed angle between the two vectors.

        """
        return angle_vectors_signed(self, other, normal)

    def angles(self, other):
        """Compute both angles between this ``Vector`` and another vector.

        Parameters
        ----------
        other : vector
            The other vector.

        Returns
        -------
        tuple of float
            The angles between the two vectors, with the smallest angle first.

        """
        return angles_vectors(self, other)

    # ==========================================================================
    # transformations
    # ==========================================================================

    def transform(self, matrix):
        """Transform this ``Vector`` using a given transformation matrix.

        Parameters
        ----------
        matrix : list of list
            The transformation matrix.

        """
        point = transform_vectors([self], matrix)[0]
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]

    def transformed(self, matrix):
        """Return a transformed copy of this ``Vector`` using a given transformation matrix.

        Parameters
        ----------
        matrix : list of list
            The transformation matrix.

        Returns
        -------
        Vector
            The transformed copy.

        """
        vector = self.copy()
        vector.transform(matrix)
        return vector


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest

    from math import radians  # noqa F401
    from compas.geometry import Rotation  # noqa F401

    doctest.testmod(globs=globals())
