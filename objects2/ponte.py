from objects2 import Colors


class Ponte:
    def __init__(self, win, x, y, w, h, ty, out, t_expl):
        self.x = x
        self.dir = 0
        self.y = y
        self.w = w
        self.h = h
        self.ty = ty
        self.out = out
        self.win = win
        self.t_expl = t_expl
        self.cor = Colors.cor
        self.mp = [[[10],          # pistas
                    [10],
                    [11],
                    [11],
                    [11],
                    [11],
                    [11],
                    [1],
                    [11],
                    [11],
                    [11],
                    [11],
                    [11],
                    [10],
                    [10]],

                   [[0,  17,  0,  0,  0, 17,  0],
                    [17, 17, 17, 17, 17, 17, 17],  # ponte
                    [18, 18, 18, 18, 18, 18, 18],
                    [18, 18, 18, 18, 18, 18, 18],
                    [19, 19, 19, 19, 19, 19, 19],
                    [19, 19, 19, 19, 19, 19, 19],
                    [18, 18, 18, 18, 18, 18, 18],
                    [18, 18, 18, 18, 18, 18, 18],
                    [19, 19, 19, 19, 19, 19, 19],
                    [19, 19, 19, 19, 19, 19, 19],
                    [1,   1,  1,  1,  1,  1,  1],
                    [1,   1,  1,  1,  1,  1,  1],
                    [19, 19, 19, 19, 19, 19, 19],
                    [19, 19, 19, 19, 19, 19, 19],
                    [18, 18, 18, 18, 18, 18, 18],
                    [18, 18, 18, 18, 18, 18, 18],
                    [19, 19, 19, 19, 19, 19, 19],
                    [19, 19, 19, 19, 19, 19, 19],
                    [18, 18, 18, 18, 18, 18, 18],
                    [18, 18, 18, 18, 18, 18, 18],
                    [17, 17, 17, 17, 17, 17, 17],  # ponte
                    [0,  17,  0,  0,  0, 17, 0]],

                   [[0, 0, 0, 0, 0, 8, 0, 0],     # 12 esplosão 1
                    [0, 0, 0, 8, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 8, 0],
                    [8, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 6, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 4],
                    [0, 4, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 4, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 4, 0],
                    [9, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 9, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 9, 0, 0]],

                   [[0, 0, 15, 0, 0, 0],          # 13 esplosão 2
                    [0, 0, 0, 0, 15, 0],
                    [15, 0, 0, 0, 0, 0],
                    [0, 0, 0, 15, 0, 0],
                    [0, 15, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 15],
                    [0, 0, 9, 0, 0, 0],
                    [0, 0, 0, 0, 9, 0]]]

    def show(self):
        obj = self.ty
        if self.t_expl > 20:
            obj = 2
        elif self.t_expl:
            obj = 3

        for col in range(len(self.mp[obj][0])):
            for lin in range(len(self.mp[obj])):

                if self.mp[obj][lin][col] and (not self.out or self.t_expl):
                    x = self.x + col * int(self.w / len(self.mp[obj][0]))
                    y = self.y + lin * int(self.h / len(self.mp[obj]))
                    w = int(self.w / len(self.mp[obj][0]))
                    h = int(self.h / len(self.mp[obj]))
                    self.win.fill(self.cor[self.mp[obj][lin][col]], rect=[x, y, w, h])
        if self.t_expl:
            self.t_expl -= 1
