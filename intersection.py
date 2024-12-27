class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def Intersection(l_1, r_1, l_2, r_2):
    if (l_1.x >= r_2.x or l_2.x >= r_1.x):
        return False

    if (l_1.y >= r_2.y or l_2.y >= r_1.y):
        return False

    return True


# l_1 = Point(100, 100)
# r_1 = Point(250, 50)
# l_2 = Point(245, 150)
# r_2 = Point(300, 75)

# print(Intersection(l_1, r_1, l_2, r_2))