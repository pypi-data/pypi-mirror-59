# from .vector import Vector

class Point(object):
    """Point Class"""
    x = None
    y = None
    z = None
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def to_vector(self):
        """Returns the vector from origin to this point"""
        x = self.x
        y = self.y
        z = self.z
        return Vector(x, y, z)
    def distance_from_origin(self):
        """Returns the distance from origin to this point"""
        vec = self.to_vector()
        return vec.return_magnitude()
    def __eq__(self, obj):
        if isinstance(obj, Point):
            return self.x == obj.x and self.y == obj.y and self.z == obj.z
    def __add__(self, obj):
        if isinstance(obj, Vector):
            return Point(self.x+obj.x, self.y+obj.y, self.z+obj.z)
    def __sub__(self, obj):
        if isinstance(obj, Vector):
            return Point(self.x-obj.x, self.y-obj.y, self.z-obj.z)
    def __repr__(self):
        chx = isinstance(self.x, float)
        chy = isinstance(self.y, float)
        chz = isinstance(self.z, float)
        if chx and chy and chz:
            frmstr = '<Point: {:.8g}, {:.8g}, {:.8g}>'
        else:
            frmstr = '<Point: {:}, {:}, {:}>'
        return frmstr.format(self.x, self.y, self.z)
    def __str__(self):
        chx = isinstance(self.x, float)
        chy = isinstance(self.y, float)
        chz = isinstance(self.z, float)
        if chx and chy and chz:
            frmstr = '{:.8g}\t{:.8g}\t{:.8g}'
        else:
            frmstr = '{:}\t{:}\t{:}'
        return frmstr.format(self.x, self.y, self.z)

def point_from_lists(x, y, z):
    """Create a list of Point objects"""
    return [Point(x[i], y[i], z[i]) for i in range(len(x))]

def midpoint_of_points(pnts):
    num = len(pnts)
    x = sum(pnt.x for pnt in pnts)/num
    y = sum(pnt.y for pnt in pnts)/num
    z = sum(pnt.z for pnt in pnts)/num
    return Point(x, y, z)
