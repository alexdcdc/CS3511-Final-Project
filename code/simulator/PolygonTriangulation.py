from manim import *
import numpy as np
import algorithm


class PolygonTriangulation(Scene):
    def construct(self):
        weights = [6, 10, 2, 1, 4, 3, 8, 5] # Vertex weights of polygon

        # Draw the original polygon
        n = len(weights)
        radius = 2.5
        polygon = RegularPolygon(n=n, radius=radius, color=BLUE)
        center = polygon.get_center()

        # Add the polygon
        self.play(Create(polygon))

        # Get the vertices
        vertices = polygon.get_vertices()

        # Labels: can use letters or numbers
        labels = [Text(str(weights[i]), font_size=24) for i in range(n)]  # A, B, C, ...

        # Position labels near the vertices
        for vertex, label in zip(vertices, labels):
            dir = (vertex - center) / np.linalg.norm(vertex - center)
            label.move_to(vertex + dir * 0.3)
            self.add(Dot(vertex, radius=0.05, color=YELLOW))
            self.add(label)

        result, edges = algorithm.solve_full(weights)
        for i, j in edges:
            line = DashedLine(vertices[i], vertices[j], color = YELLOW)
            self.play(Create(line))
            self.wait(2)

