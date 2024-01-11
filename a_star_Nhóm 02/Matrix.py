import math
import queue

import pygame, sys
import easygui

from Point import Point
from Window import Window


class Matrix():
    def __init__(self, size):
        self.matrix = [] # khởi tạo ma trận rỗng
        self.size = size
        self.start = Point(0, 0)
        self.end = None
        self.n = size[0] // 5 # chia làm tròn xuống
        self.m = size[1] // 5
        self.E = [[0 for i in range(100)] for i in range(100)] # Tạo ra 1 mảng cha chứa 100 mảng con, trong đó mỗi mảng con chứa 100 phần tử chữ số 0.
        self.sets = queue.PriorityQueue() # Hàng đợi ưu tiên để lưu trữ tập các đường đi, bắt đầu từ nút xuất phát.
        self.isFind = True
        for i in range(0, size[0] + 5, 5):
            b = []
            for j in range(0, size[1] + 5, 5):
                b.append(Window(i, j))
            self.matrix.append(b)

    def drawEnd(self, mousepos):  # Hàm này để vẽ ra điểm kết thúc
        x = mouPos[0] // 5
        y = mouPos[1] // 5
        self.matrix[x][y].changeColor('end')
        self.matrix[x][y].draw(window)
        self.end = Point(x, y)
        self.E[x][y] = 0
        t = [1, 0, -1]
        for i in range(0, 3):
            for j in range(0, 3):
                self.E[x + t[i]][y + t[j]] = 0
                self.matrix[x + t[i]][y + t[j]].changeColor('end')
                self.matrix[x + t[i]][y + t[j]].draw(window)

    def drawStart(self, mousepos):  # Hàm này để vẽ ra điểm xuất phát
        x = mouPos[0] // 5
        y = mouPos[1] // 5
        self.matrix[x][y].changeColor('start')
        self.matrix[x][y].draw(window)
        self.start = Point(x, y)
        self.E[x][y] = 0
        t = [1, 0, -1]
        for i in range(0, 3):
            for j in range(0, 3):
                self.E[x + t[i]][y + t[j]] = 0
                self.matrix[x + t[i]][y + t[j]].changeColor('start')
                self.matrix[x + t[i]][y + t[j]].draw(window)
        self.sets.put(self.start)

    def drawS(self):  # Hàm này để vẽ ra điểm xuất phát đầu tiên
        self.matrix[self.start.x][self.start.y].draw(window)
        x = self.start.x
        y = self.start.y
        t = [1, 0, -1]
        for i in range(0, 3):
            for j in range(0, 3):
                self.matrix[x + t[i]][y + t[j]].changeColor('start')
                self.matrix[x + t[i]][y + t[j]].draw(window)

    def draw(self, window, mouse, mousePos):  # Hàm này để vẽ ra chướng ngại vật (sử dụng chuột trái để vẽ)
        if mouse[0]:
            x = mousePos[0] // 5
            y = mousePos[1] // 5
            self.matrix[x][y].changeColor('obstacle')
            self.matrix[x][y].draw(window)
            self.E[x][y] = -1
            t = [1, 0, -1]
            for i in range(0, 3):
                for j in range(0, 3):
                    self.E[x + t[i]][y + t[j]] = -1
                    self.matrix[x + t[i]][y + t[j]].changeColor('obstacle')
                    self.matrix[x + t[i]][y + t[j]].draw(window)

    def drawF(self, window):
        for i in range(0, self.size[0] // 5 + 1):
            for j in range(0, self.size[1] // 5 + 1):
                self.matrix[i][j].draw(window)

    def solve(self, window):  # Thuật toán A*
        self.drawS()
        t = [1, 0, -1]
        for i in range(0, 3):
            for j in range(0, 3):
                self.E[self.end.x + t[i]][self.end.y + t[j]] = 0
                self.matrix[self.end.x + t[i]][self.end.y + t[j]].changeColor('end')
                self.matrix[self.end.x + t[i]][self.end.y + t[j]].draw(window)
                self.E[self.end.x][self.end.y] = 0
        if self.isFind == False:
            return
        # Các ô có thể đi theo 8 hướng.
        pos1 = [0,  0,  1, -1,  1, -1,  1, -1]
        pos2 = [1, -1,  0,  0,  1,  1, -1, -1]
        k = self.sets.get()
        self.matrix[k.x][k.y].changeColor(
            'check')  # Duyệt qua các ô, các ô được duyệt sẽ chuyển sang màu xanh và không duyệt lại
        self.matrix[k.x][k.y].draw(window)
        for i in range(8):
            x = k.x + pos1[i]
            y = k.y + pos2[i]
            if x < 0 or x >= self.n:
                continue
            if y < 0 or y >= self.m:
                continue
            if self.E[x][y] == -1:
                continue
            temp = Point(x, y, k)
            temp.G = k.G + 1
            temp.H = math.sqrt(pow((x - self.end.x),2) + pow((y - self.end.y),2)) #Thuận toán tìm đường.
            self.E[x][y] = -1
            self.sets.put(temp)
            self.matrix[x][y].changeColor('uncheck')  # Các ô đang trong trạng thái chờ duyệt tiếp
            self.matrix[x][y].draw(window)
            if temp.H == 0:
                self.isFind = False
                while temp is not None:
                    self.matrix[temp.x][temp.y].changeColor('road')  # Vẽ ra đường đi tối ưu nhất
                    self.matrix[temp.x][temp.y].draw(window)
                    temp = temp.old # Thoát khỏi vòng lặp.


easygui.msgbox("HƯỚNG DẪN SỬ DỤNG \n"
               "Nhấn giữ nút S và chọn 1 diểm - đó là điểm xuất phát (màu đỏ) \n"
               "Nhấn giữ nút E và chọn 1 diểm - đó là điểm kết thúc (màu tím) \n"
               "Nhấn giữ và kéo thả chuột cho phép vẽ chướng ngại vật \n"
               "Nhấn Space cho phép chạy thuật toán tìm đường \n", title="GUIDE")

size = (500, 500)  # Khai báo giao diện và chạy chương trình.
window = pygame.display.set_mode(size)
FPS = 240
fpsClock = pygame.time.Clock()
maTrix = Matrix(size)
maTrix.drawF(window)
result = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    mouPos = pygame.mouse.get_pos()
    if keys[pygame.K_s]:  # Nút S cho phép vẽ ra vị trí bắt đầu theo vị trí chuột
        maTrix.drawStart(mouPos)
    if keys[pygame.K_e]:  # Nút E cho phép vẽ ra vị trí bắt đầu theo vị trí chuột
        maTrix.drawEnd(mouPos)
    if keys[pygame.K_SPACE]:  # Nút cách cho phép chạy thuật toán
        result = True
    maTrix.draw(window, mouse, mouPos)
    if result:
        maTrix.solve(window)
    pygame.display.flip()
    fpsClock.tick(FPS)

