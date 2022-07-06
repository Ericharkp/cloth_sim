from collections import defaultdict
import json
import pygame



class ClothEditor():

    def __init__(self, surf: pygame.display, grid_size) -> None:
        """the resolution of the pygame display should be divisible by grid size"""

        self.draw_grid(surf, grid_size)
        self.surf = surf
        self.points = {}
        self.connection = defaultdict(list)
        # self.connection = {}
        self.grid_total_size = surf.get_size()
        self.grid_size = grid_size
        self.horizontal_grid_number = self.grid_total_size[0]//self.grid_size
        self.vertical_grid_number = self.grid_total_size[1]//self.grid_size

    def add_point(self, location: list[float]):
        point = location[0]//self.grid_size + \
            (location[1]//self.grid_size *
             self.horizontal_grid_number) # transform the position to 1D

        location = [location[0]//self.grid_size * self.grid_size,  # snap the point to the grid
                    location[1]//self.grid_size * self.grid_size]

        if point not in self.points:
            self.points[point] = 1
            self.__draw_point(point)


    def add_grounded_point(self, p1):
        p1_hashed = p1[0]//self.grid_size + p1[1]//self.grid_size * self.horizontal_grid_number
        if p1_hashed in self.points:
            self.points[p1_hashed] = 2
            p1d = [(p1_hashed % self.horizontal_grid_number) * self.grid_size, (p1_hashed // self.horizontal_grid_number) * self.grid_size] # convert back to 2d coordinate from 1d
            pygame.draw.circle(self.surf, (255, 255, 0), p1d, 2)


    def add_line(self, p1, p2):
        p1_hashed = p1[0]//self.grid_size + p1[1]//self.grid_size * self.horizontal_grid_number
        p2_hashed = p2[0]//self.grid_size + p2[1]//self.grid_size * self.horizontal_grid_number
        if p1_hashed in self.points and p2_hashed in self.points:
            if p2_hashed not in self.connection[p1_hashed]:
                self.connection[p1_hashed].append(p2_hashed)
                print(self.connection)
            self.__draw_temp_line(p1, [p2[0], p2[1]])

    def __draw_temp_line(self, p1, p2):

        p1[0] = p1[0]//self.grid_size * self.grid_size
        p1[1] = p1[1]//self.grid_size * self.grid_size

        p2[0] = p2[0]//self.grid_size * self.grid_size
        p2[1] = p2[1]//self.grid_size * self.grid_size
        
        pygame.draw.line(self.surf, (255, 255, 255), p1, p2)

    def __draw_point(self, point):
        p2d = [(point % self.horizontal_grid_number) * self.grid_size,
               (point // self.horizontal_grid_number) * self.grid_size] # convert back to 2d coordinate from 1d
        pygame.draw.circle(self.surf, (255, 255, 255), p2d, 2)

    def earse_point(self, location):
        point = location[0]//self.grid_size + \
            (location[1]//self.grid_size *
             self.grid_total_size[0]//self.grid_size)

        location = [location[0]//self.grid_size * self.grid_size,  # snap the point to the grid
                    location[1]//self.grid_size * self.grid_size]
        if point in self.points:
            print('delete', point)
            del self.points[point]

        self.surf.fill((0, 0, 0))
        self.draw_grid(self.surf, self.grid_size)
        for i in self.points:
            self.__draw_point(i)
        pygame.display.update()

    def draw_grid(self, surf: pygame.display, grid_size):
        window_size = surf.get_size()
        grid_width = window_size[0]//grid_size
        grid_height = window_size[1]//grid_size

        for i in range(grid_width):
            pygame.draw.line(surf, (155, 155, 155), (grid_size *
                                                     i, 0), (grid_size * i, window_size[1]))
        for i in range(grid_height):
            pygame.draw.line(surf, (155, 155, 155),
                             (0, grid_size * i), (window_size[0], grid_size*i))


    def save_as_json(self, file_name, scale):
        points = []
        coordinates = []
        connections = []
        ground = []
        save_data = {}

        for point in self.points:
            points.append(point)
            if self.points[point] == 2:
                ground.append(point)

        for c1 in self.connection:
            for c2 in self.connection[c1]:
                c = [points.index(c1), points.index(c2)]
                connections.append(c)
        
        for i, p in enumerate(ground):
            ground[i] = points.index(p)


        for point in points:
            p = [(point % self.horizontal_grid_number), (point // self.horizontal_grid_number)]
            coordinates.append(p)

        print(coordinates, points, connections, ground)

        if len(points) - 1 > len(connections):
            print("There is some loose point")
        
        else:
            save_data["points"] = coordinates
            save_data["connections"] = connections
            save_data["scale"] = scale
            save_data["grounded"] = ground
            with open('test_mesh.mesh', 'w') as file:
                json.dump(save_data, file)

