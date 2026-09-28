from manim import *


class IntegralXSquared(Scene):
    def construct(self):
        title = Text("Visualisasi Integral dari x²", font_size=40)
        subtitle = MathTex(r"\int_0^2 x^2\,dx")
        subtitle.next_to(title, DOWN, buff=0.25)

        self.play(Write(title), Write(subtitle))
        self.wait(0.8)
        self.play(
            title.animate.scale(0.7).to_edge(UP),
            subtitle.animate.scale(0.9).next_to(title, DOWN, buff=0.12),
        )

        axes = Axes(
            x_range=[0, 2.5, 0.5],
            y_range=[0, 4.8, 1],
            x_length=6.2,
            y_length=4.6,
            axis_config={"include_numbers": True},
            tips=False,
        ).shift(DOWN * 0.35)

        x_label = axes.get_x_axis_label(MathTex("x"))
        y_label = axes.get_y_axis_label(MathTex("y"))

        graph = axes.plot(lambda x: x**2, x_range=[0, 2.1], color=BLUE)
        graph_label = MathTex(r"y=x^2", color=BLUE).next_to(
            axes.c2p(1.75, 3.2), RIGHT, buff=0.15
        )

        self.play(Create(axes), FadeIn(x_label, y_label))
        self.play(Create(graph), Write(graph_label))
        self.wait(0.6)

        left_line = DashedLine(axes.c2p(0, 0), axes.c2p(0, 0.25), color=YELLOW)
        right_line = DashedLine(axes.c2p(2, 0), axes.c2p(2, 4), color=YELLOW)
        a_label = MathTex("0").scale(0.8).next_to(axes.c2p(0, 0), DOWN)
        b_label = MathTex("2").scale(0.8).next_to(axes.c2p(2, 0), DOWN)

        self.play(Create(left_line), Create(right_line), FadeIn(a_label, b_label))

        rects = axes.get_riemann_rectangles(
            graph,
            x_range=[0, 2],
            dx=0.5,
            input_sample_type="right",
            stroke_width=1,
            fill_opacity=0.55,
            color=[TEAL, BLUE],
        )

        n_label = MathTex(r"\Delta x=0.5").to_corner(UR).shift(DOWN * 0.9)
        self.play(FadeIn(rects), Write(n_label))
        self.wait(0.7)

        for dx in [0.25, 0.125, 0.0625]:
            new_rects = axes.get_riemann_rectangles(
                graph,
                x_range=[0, 2],
                dx=dx,
                input_sample_type="right",
                stroke_width=max(0.4, 1.5 * dx),
                fill_opacity=0.55,
                color=[TEAL, BLUE],
            )
            new_label = MathTex(rf"\Delta x={dx:g}").move_to(n_label)
            self.play(
                ReplacementTransform(rects, new_rects),
                Transform(n_label, new_label),
                run_time=0.9,
            )
            rects = new_rects

        limit_text = MathTex(r"\Delta x\to 0").move_to(n_label)
        self.play(Transform(n_label, limit_text))

        area = axes.get_area(
            graph,
            x_range=[0, 2],
            color=BLUE,
            opacity=0.45,
        )
        self.play(FadeOut(rects), FadeIn(area), run_time=1.0)

        integral_formula = MathTex(
            r"\int_0^2 x^2\,dx",
            r"=\left[\frac{x^3}{3}\right]_0^2",
            r"=\frac{8}{3}",
        ).scale(0.88)
        integral_formula.to_corner(DR).shift(UP * 0.35)

        self.play(Write(integral_formula[0]))
        self.play(Write(integral_formula[1]))
        self.play(Write(integral_formula[2]))

        result_box = SurroundingRectangle(integral_formula[2], color=YELLOW, buff=0.12)
        self.play(Create(result_box))
        self.wait(2)
