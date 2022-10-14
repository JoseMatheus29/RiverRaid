from objects2 import Colors

class Shot:
    def __init__(self, win, shoting, x, y):
        self.x = x
        self.y = y
        self.w = 5
        self.h = 15
        self.shoting = shoting
        self.win = win
        self.cor = Colors.cor

    def show(self, planex, planey):
        if self.shoting:
            self.shoting = False
            if self.y <= 0:
                self.x = planex
                self.y = planey
        if self.y > -self.h:
            self.y -= 6
        self.win.fill(self.cor[13], rect=[self.x, self.y, self.w, self.h])
