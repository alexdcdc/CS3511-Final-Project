from manim import *
import numpy as np
import algorithm
import random

# to-do: parallel with matrix multiplication problem

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

    def get_triangle(self, vertices, triangle):
        points = [vertices[i] for i in triangle]

        color = random_bright_color()
        return Polygon(*points, fill_opacity = 0.3, fill_color = color, stroke_width = 0)

    def get_weight_label(self, vertices, weights, triangle):
        weight = weights[triangle[0]] * weights[triangle[1]] * weights[triangle[2]]
        A = vertices[triangle[0]]
        B = vertices[triangle[1]]
        C = vertices[triangle[2]]

        # Compute side lengths
        a = np.linalg.norm(B - C)
        b = np.linalg.norm(C - A)
        c = np.linalg.norm(A - B)

        # Compute incenter
        incenter = (a * A + b * B + c * C) / (a + b + c)

        label = Label(Text(str(weight), font_size = 20))
        label.move_to(incenter)
        return label

    def generate_random_weights(self, n):
        weights = []
        while len(weights) < n:
            next_num = random.randint(1, 20)
            if next_num not in weights:
                weights.append(next_num)

        return weights

    def construct(self):
        weights = [10, 13, 15, 16, 14, 12]
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

        result, edges, cones, triangles = algorithm.solve_full(weights)
        polygon.set_fill(opacity = 0)
        cone = None
        for i in range(len(edges)):
            line = DashedLine(vertices[edges[i][0]], vertices[edges[i][1]], color = YELLOW)
            if cone is not None:
                self.remove(cone)
            cone = self.get_cone(vertices, cones[i])
            self.add(cone)
            self.wait(1)
            self.play(Create(line), run_time = 0.5)

        self.remove(cone)
        final_equation = VGroup()
        weight_labels = []
        for i in range(len(triangles)):
            triangle = self.get_triangle(vertices, triangles[i])
            self.add(triangle)
            label = self.get_weight_label(vertices, weights, triangles[i])
            weight_labels.append(label)
            self.add(label)
            self.wait(0.4)
            triangle_weight = weights[triangles[i][0]] * weights[triangles[i][1]]*weights[triangles[i][2]]
            final_equation.add(MathTex(str(triangle_weight), font_size=32))
            if i != len(triangles) - 1:
                final_equation.add(MathTex("+", font_size=32))

        equals = MathTex("=", font_size=32)
        result = MathTex(str(result), font_size=32)
        final_equation.arrange(RIGHT, buff=0.1).to_edge(DOWN)
        equals.next_to(final_equation, RIGHT)
        result.next_to(equals, RIGHT)

        transforms = []
        for orig_label, target in zip(weight_labels, final_equation[::2]):
            transforms.append(Transform(orig_label, target))

        self.play(*transforms, run_time=1.5)
        self.play(Write(final_equation[1::2]))  # Write the '+' signs
        self.play(Write(equals), Write(result))


        self.wait(3)

