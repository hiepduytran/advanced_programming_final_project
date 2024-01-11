import pygame


class Window():
    baseColor = (255, 255, 255)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        pygame.draw.rect(window, (0, 0, 0), (self.x, self.y, 5, 5))
        pygame.draw.rect(window, self.baseColor, (self.x + 1, self.y + 1, 3, 3))
        pygame.display.set_caption('Thuật Toán A*')

    def changeColor(self, type):  # Các màu sắc theo từng loại trong bài toán
        if type == 'start':
            self.baseColor = (255, 0, 0)  # Màu đỏ là màu của điểm xuất phát
        elif type == 'obstacle':
            self.baseColor = (30, 144, 255)  # Màu xanh dương là màu của chướng ngại vật
        elif type == 'end':
            self.baseColor = (255, 0, 255)  # Màu tím là màu của điểm cần tìm
        elif type == 'check':
            self.baseColor = (0, 255, 0)  # Màu xanh lá là màu của ô được duyệt
        elif type == 'uncheck':
            self.baseColor = (245, 245, 34)  # Màu vàng là màu của các ô chưa được duyệt
        elif type == 'road':
            self.baseColor = (255, 105, 180)  # Màu hồng là màu của tuyến đường tốt nhất
