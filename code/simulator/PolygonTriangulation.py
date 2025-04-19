from manim import *
import numpy as np
import algorithm
import random



class PolygonTriangulation(Scene):
    def get_cone(self, vertices, cone):
        polygon = []
        start = cone[0]
        end = cone[1]
        while start != end:
            polygon.append(vertices[start])
            start = (start + 1) % len(vertices)

        polygon.append(vertices[end])

        if cone[2] != -1:
            polygon.append(vertices[cone[2]])
            fill_color = GREEN
        else:
            fill_color = YELLOW


        return Polygon(*polygon, fill_opacity = 0.3, fill_color = fill_color, stroke_width = 0)


    def construct(self):
        weights = list(range(30, 43))
        random.shuffle(weights)

        # Draw the original polygon
        n = len(weights)
        radius = 2.5
        polygon = RegularPolygon(n=n, radius=radius, color=BLUE)
        center = polygon.get_center()


        # Get the vertices
        vertices = polygon.get_vertices()

        # Labels: can use letters or numbers
        labels = [Text(str(weights[i]), font_size=24) for i in range(n)]  # A, B, C, ...

        animations = []

        # Position labels near the vertices
        for vertex, label in zip(vertices, labels):
            dir = (vertex - center) / np.linalg.norm(vertex - center)
            label.move_to(vertex + dir * 0.3)
            animations.append(Create(Dot(vertex, radius=0.05, color=YELLOW, z_index=1)))
            animations.append(Create(label))
        self.play(AnimationGroup(*animations, lag_ratio = 0.5, run_time = 2))
        self.wait(1)
        self.play(Create(polygon))
        self.wait(1)

        result, edges, cones = algorithm.solve_full(weights)
        cone = self.get_cone(vertices, (0, 0, -1))
        self.add(cone)
        self.wait(1)
        for i in range(len(edges)):
            line = DashedLine(vertices[edges[i][0]], vertices[edges[i][1]], color = YELLOW)
            self.remove(cone)
            cone = self.get_cone(vertices, cones[i])
            self.add(cone)
            self.wait(1)
            self.play(Create(line), run_time = 0.5)
            self.wait(1)

        self.wait(3)

