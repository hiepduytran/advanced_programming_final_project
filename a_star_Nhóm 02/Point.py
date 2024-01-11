class Point():
    def __init__(self, x, y, old=None):
        self.x = x
        self.y = y
        self.G = 0
        self.H = 0
        self.old = old

    def __gt__(self, other): # nạp chông toán tử so sánh hai đối tượng
        if self.G + self.H >= other.G + other.H:
            return True
        else:
            return False

a = Point(1,2,0)
a.G = 2
a.H = 4

b = Point(1,2,0)
b.G = 3
b.H = 6

print(a < b)