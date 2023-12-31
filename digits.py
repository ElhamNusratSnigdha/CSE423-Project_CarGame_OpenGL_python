from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Digits:
    def __init__(self):
        self.__midpoint_points = []

    def find_zone(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1

        if abs(dx) > abs(dy):
            if dx >= 0 and dy >= 0:
                return 0
            elif dx <= 0 and dy >= 0:
                return 3
            elif dx <= 0 and dy <= 0:
                return 4
            elif dx >= 0 and dy <= 0:
                return 7
        else:
            if dx >= 0 and dy >= 0:
                return 1
            elif dx <= 0 and dy >= 0:
                return 2
            elif dx <= 0 and dy <= 0:
                return 5
            elif dx >= 0 and dy <= 0:
                return 6

    def convert_to_zone0(self, x1, y1, zone):
        if zone == 0:
            return x1, y1
        elif zone == 1:
            return y1, x1
        elif zone == 2:
            return y1, -x1
        elif zone == 3:
            return -x1, y1
        elif zone == 4:
            return -x1, -y1
        elif zone == 5:
            return -y1, -x1
        elif zone == 6:
            return -y1, x1
        elif zone == 7:
            return x1, -y1

    def convert_to_original_zone(self, x1, y1, zone):
        if zone == 0:
            return x1, y1
        elif zone == 1:
            return y1, x1
        elif zone == 2:
            return -y1, x1
        elif zone == 3:
            return -x1, y1
        elif zone == 4:
            return -x1, -y1
        elif zone == 5:
            return -y1, -x1
        elif zone == 6:
            return y1, -x1
        elif zone == 7:
            return x1, -y1

    def midpoint(self, x1, y1, x2, y2):
        glBegin(GL_POINTS)

        zone = self.find_zone(x1, y1, x2, y2)

        x1_to_z0, y1_to_z0 = self.convert_to_zone0(x1, y1, zone)
        x2_to_z0, y2_to_z0 = self.convert_to_zone0(x2, y2, zone)

        dy = y2_to_z0 - y1_to_z0
        dx = x2_to_z0 - x1_to_z0
        d = 2 * dy - dx
        d_E = 2 * dy
        d_NE = 2 * (dy - dx)

        x = x1_to_z0
        y = y1_to_z0

        original_x, original_y = self.convert_to_original_zone(x, y, zone)
        glVertex2f(original_x, original_y)

        while x <= x2_to_z0:
            self.__midpoint_points.append((original_x, original_y))

            if d < 0:
                x = x + 1
                d = d + d_E
            else:
                x = x + 1
                y = y + 1
                d = d + d_NE

            original_x, original_y = self.convert_to_original_zone(x, y, zone)
            glVertex2f(original_x, original_y)

        glEnd()

    def draw_digit(self, digit, offset_x=0, offset_y=0, digit_position_x=0):

        digit_lights = {
            0: [self.l_t, self.l_b, self.b, self.r_b, self.r_t, self.t],
            1: [self.r_b, self.r_t],
            2: [self.l_b, self.b, self.r_t, self.t, self.m],
            3: [self.b, self.r_b, self.r_t, self.t, self.m],
            4: [self.l_t, self.r_b, self.r_t, self.m],
            5: [self.l_t, self.b, self.r_b, self.t, self.m],
            6: [self.l_t, self.l_b, self.b, self.r_b, self.t, self.m],
            7: [self.r_b, self.r_t, self.t],
            8: [self.l_t, self.l_b, self.b, self.r_b, self.t, self.r_t, self.m],
            9: [self.l_t, self.b, self.r_b, self.t, self.r_t, self.m]
        }

       
        show_digits = digit

        first_digit = int(show_digits[0])
        if int(digit) > 9:
            second_digit = int(show_digits[1])

        if int(digit) <= 9:
            first_digit = 0
            second_digit = int(show_digits[0])

        for i in digit_lights[first_digit]:
            i(x=digit_position_x + offset_x, y=250 + offset_y)

        for i in digit_lights[second_digit]:
            i(x=digit_position_x + offset_x, y=250 + offset_y, adjust=250)

    def get_midpoint_points(self):
        return self.__midpoint_points

    def r_t(self, adjust=0, x=0, y=0):
        self.midpoint(400 + adjust + x, 400 + y, 400 + adjust + x, 600 + y)

    def r_b(self, adjust=0, x=0, y=0):
        self.midpoint(400 + adjust + x, 200 + y, 400 + adjust + x, 400 + y)

    def l_t(self, adjust=0, x=0, y=0):
        self.midpoint(200 + adjust + x, 400 + y, 200 + adjust + x, 600 + y)

    def l_b(self, adjust=0, x=0, y=0):
        self.midpoint(200 + adjust + x, 200 + y, 200 + adjust + x, 400 + y)

    def b(self, adjust=0, x=0, y=0):
        self.midpoint(200 + adjust + x, 200 + y, 400 + adjust + x, 200 + y)

    def t(self, adjust=0, x=0, y=0):
        self.midpoint(200 + adjust + x, 600 + y, 400 + adjust + x, 600 + y)

    def m(self, adjust=0, x=0, y=0):
        self.midpoint(200 + adjust + x, 400 + y, 400 + adjust + x, 400 + y)
