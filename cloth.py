import pygame
import math
import json
import os


def load_model(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    return json.loads(data)


def save_model(path, data: dict):
    f = open(path, 'w')
    json.dump(data, f)
    f.close()
    # json.load


def get_dis(point_1: list, point_2: list):
    """
    return the magnitude of distance between two points
    """
    return math.sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)


def load_rags(path):
    rag_list = os.listdir(path)

    rags = {}
    for rag in rag_list:
        rags[rag.split('.')[0]] = load_model(path + '/' + rag)
    return rags


class ClothObj():
    points: list[list]
    """
    the points are 2d, first dimension contain current position and the next contain previous position
    """
    sticks: list[list]
    """
    The connection between the points represented by its index,
    first two elements is the index of the two points and the third represented the supposed distance between the two points"""

    def __init__(self, rag) -> None:
        self.points = [p + p for p in rag['points']]
        self.original_points = [p + p for p in rag['points']]
        self.sticks = {}
        self.grounded_point = rag['grounded']
        self.grounded_point_offset = [self.points[p][:2]
                                      for p in self.grounded_point]
        self.scale = rag['scale']
        for i, connection in enumerate(rag['connections']):
            self.sticks[i] = ([connection[0], connection[1], get_dis(
                self.points[connection[0]][:2], self.points[connection[1]][:2])])

            # self.sticks.append([connection[0], connection[1], get_dis(
            #     self.points[connection[0]][:2], self.points[connection[1]][:2])])

    def set_pos(self, pos):
        for point, orig_point in zip(self.points, self.original_points):
            point[0] = orig_point[0] + pos[0]
            point[1] = orig_point[1] + pos[1]
            point[2] = orig_point[2] + pos[0]
            point[3] = orig_point[3] + pos[1]

    def update_grounded_pos(self, mouse: list[float], offset=[0, 0]):
        for i in self.grounded_point:
            self.points[i][0] = self.grounded_point_offset[i][0] + \
                mouse[0] / self.scale
            self.points[i][1] = self.grounded_point_offset[i][1] + \
                mouse[1] / self.scale
            self.points[i][2] = self.points[i][0]
            self.points[i][3] = self.points[i][1]

    def update_pos(self):

        for i, point in enumerate(self.points):
            if i not in self.grounded_point:
                dx = (point[0] - point[2])
                dy = (point[1] - point[3])

                point[2] = point[0]
                point[3] = point[1]
                point[0] += dx
                point[1] += dy
                point[1] += 0.01

        self.__apply_constrain()
        # self.__apply_constrain()
        # self.__apply_constrain()

    def __apply_constrain(self):
        for i in list(self.sticks):
            connection = self.sticks[i]
            dis = get_dis(self.points[connection[0]][:2],
                          self.points[connection[1]][:2])
            if dis > (connection[2] * 4):
                del self.sticks[i]

            dis_dif = connection[2] - dis
            ratio = dis_dif / dis / 2
            dx = self.points[connection[1]][0] - \
                self.points[connection[0]][0]
            dy = self.points[connection[1]][1] - \
                self.points[connection[0]][1]
            if connection[0] not in self.grounded_point:
                self.points[connection[0]][0] -= dx * ratio 
                self.points[connection[0]][1] -= dy * ratio 
            if connection[1] not in self.grounded_point:
                self.points[connection[1]][0] += dx * ratio 
                self.points[connection[1]][1] += dy * ratio 

    def cut(self, position: list):
        threshold = 1
        pos = [0, 0]
        pos[0] = position[0] / self.scale
        pos[1] = position[1] / self.scale

        for connection in list(self.sticks):
            if threshold > self.points[self.sticks[connection][0]][0] - pos[0] > 0 and threshold > self.points[self.sticks[connection][0]][1] - pos[1] > 0:
                del self.sticks[connection]

    def render_point(self, surf, offset=[0, 0], radius=5):
        render_points = [[p[0] * self.scale - offset[0], p[1]
                          * self.scale - offset[1]] for p in self.points]
        for point in render_points:
            pygame.draw.circle(surf, (255, 255, 255),
                               (point[0], point[1]), radius)

    def render_line(self, surf, offset=[0, 0]):
        render_points = [[p[0] * self.scale - offset[0], p[1]
                          * self.scale - offset[0]] for p in self.points]
        for c in self.sticks:
            connection = self.sticks[c]
            pygame.draw.line(surf, (255, 255, 255),
                             render_points[connection[0]], render_points[connection[1]], 1)


if __name__ == "__main__":
    pass