from manim import *
import numpy as np

BG = "#0D1117"
CURVE = "#58C4DD"
AREA = "#83C167"
DERIV = "#FFDD57"
ACCENT = "#C792EA"
TEXT = "#E6EDF3"
GRID = "#334155"

config.background_color = BG


class IntegralAndDerivativeSlow(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Turunan dan Integral dari y = x²", color=TEXT, font_size=42)
        subtitle = Text("Pelan-pelan, fokus ke proses", color="#B8C0CC", font_size=26)
        subtitle.next_to(title, DOWN, buff=0.25)

        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle, shift=DOWN * 0.2), run_time=1.5)
        self.wait(2)
        self.play(
            title.animate.scale(0.72).to_edge(UP, buff=0.25),
            subtitle.animate.scale(0.72).next_to(title, DOWN, buff=0.12),
            run_time=1.6,
        )

        axes = Axes(
            x_range=[-0.5, 3.2, 0.5],
            y_range=[-0.5, 9.5, 1],
            x_length=7.2,
            y_length=4.8,
            axis_config={"include_numbers": True, "font_size": 24, "color": TEXT},
            tips=False,
        )
        axes.shift(LEFT * 1.5 + DOWN * 0.35)
        x_label = axes.get_x_axis_label(MathTex("x", color=TEXT).scale(0.9))
        y_label = axes.get_y_axis_label(MathTex("y", color=TEXT).scale(0.9))

        graph = axes.plot(lambda x: x**2, x_range=[0, 3], color=CURVE, stroke_width=5)
        graph_label = MathTex("y=x^2", color=CURVE).next_to(
            axes.c2p(2.4, 5.8), RIGHT, buff=0.15
        )

        self.play(Create(axes), FadeIn(x_label, y_label), run_time=2)
        self.play(Create(graph), Write(graph_label), run_time=2)
        self.wait(1.5)

        deriv_title = Text(
            "1. Turunan = kemiringan garis singgung",
            color=DERIV,
            font_size=28,
        )
        deriv_title.to_corner(UR).shift(LEFT * 0.3 + DOWN * 0.2)
        self.play(FadeIn(deriv_title, shift=LEFT * 0.2), run_time=1.5)

        x_tracker = ValueTracker(1.4)

        p = always_redraw(
            lambda: Dot(
                axes.c2p(x_tracker.get_value(), x_tracker.get_value() ** 2),
                color=DERIV,
                radius=0.08,
            )
        )
        def tangent_line():
            x0 = x_tracker.get_value()
            slope = 2 * x0
            half_width = 0.75
            x1 = x0 - half_width
            x2 = x0 + half_width
            y1 = x0**2 + slope * (x1 - x0)
            y2 = x0**2 + slope * (x2 - x0)
            return Line(
                axes.c2p(x1, y1),
                axes.c2p(x2, y2),
                color=DERIV,
                stroke_width=5,
            )

        tan = always_redraw(tangent_line)
        x_line = always_redraw(
            lambda: DashedLine(
                axes.c2p(x_tracker.get_value(), 0),
                axes.c2p(x_tracker.get_value(), x_tracker.get_value() ** 2),
                color=DERIV,
                stroke_opacity=0.65,
            )
        )
        slope_formula = always_redraw(
            lambda: MathTex(
                rf"f'(x)=2x\quad\Rightarrow\quad f'({x_tracker.get_value():.1f})={2*x_tracker.get_value():.1f}",
                color=TEXT,
            ).scale(0.72).move_to(RIGHT * 3.7 + UP * 0.75)
        )

        concept_box = RoundedRectangle(
            width=4.3,
            height=1.6,
            corner_radius=0.16,
            stroke_color=DERIV,
        )
        concept_box.move_to(RIGHT * 3.7 + UP * 0.75)

        self.play(Create(concept_box), run_time=1.2)
        self.play(FadeIn(p), Create(tan), Create(x_line), run_time=1.8)
        self.play(Write(slope_formula), run_time=1.8)
        self.wait(2)

        for x in [0.8, 1.0, 1.5, 2.0, 2.5]:
            self.play(x_tracker.animate.set_value(x), run_time=2.4)
            self.wait(0.8)

        deriv_steps = VGroup(
            Text("Untuk y = x²:", color=TEXT, font_size=25),
            MathTex(r"\frac{d}{dx}(x^2)=2x", color=DERIV).scale(0.95),
            Text("Artinya: makin besar x,", color=TEXT, font_size=23),
            Text("makin curam grafiknya.", color=TEXT, font_size=23),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        deriv_steps.move_to(RIGHT * 3.7 + DOWN * 1.3)

        self.play(FadeIn(deriv_steps, shift=UP * 0.2), run_time=1.6)
        self.wait(3)
        self.play(
            FadeOut(deriv_steps),
            FadeOut(concept_box),
            FadeOut(slope_formula),
            run_time=1.2,
        )
        self.play(
            FadeOut(tan),
            FadeOut(p),
            FadeOut(x_line),
            FadeOut(deriv_title),
            run_time=1.2,
        )
        self.wait(0.8)

        integ_title = Text(
            "2. Integral = luas yang terakumulasi",
            color=AREA,
            font_size=28,
        )
        integ_title.to_corner(UR).shift(LEFT * 0.3 + DOWN * 0.2)
        self.play(FadeIn(integ_title, shift=LEFT * 0.2), run_time=1.5)

        area = axes.get_area(graph, x_range=[0, 2], color=AREA, opacity=0.55)
        left_line = DashedLine(axes.c2p(0, 0), axes.c2p(0, 0.2), color=AREA)
        right_line = DashedLine(axes.c2p(2, 0), axes.c2p(2, 4), color=AREA)

        self.play(Create(left_line), Create(right_line), run_time=1.5)

        area_box = RoundedRectangle(
            width=4.4,
            height=3.5,
            corner_radius=0.16,
            stroke_color=AREA,
        )
        area_box.move_to(RIGHT * 3.7 + DOWN * 0.05)
        self.play(Create(area_box), run_time=1.2)

        rects1 = axes.get_riemann_rectangles(
            graph,
            x_range=[0, 2],
            dx=0.5,
            input_sample_type="right",
            stroke_width=1,
            fill_opacity=0.6,
            color=[AREA, CURVE],
        )
        rects2 = axes.get_riemann_rectangles(
            graph,
            x_range=[0, 2],
            dx=0.25,
            input_sample_type="right",
            stroke_width=0.8,
            fill_opacity=0.6,
            color=[AREA, CURVE],
        )
        rects3 = axes.get_riemann_rectangles(
            graph,
            x_range=[0, 2],
            dx=0.125,
            input_sample_type="right",
            stroke_width=0.5,
            fill_opacity=0.6,
            color=[AREA, CURVE],
        )

        riemann_text = VGroup(
            Text("Mulai dari pendekatan luas", color=TEXT, font_size=23),
            MathTex(r"\sum f(x_i)\,\Delta x", color=AREA).scale(0.95),
        ).arrange(DOWN, buff=0.18)
        riemann_text.move_to(RIGHT * 3.7 + UP * 1.15)

        self.play(FadeIn(riemann_text), run_time=1.4)
        self.play(FadeIn(rects1), run_time=1.8)
        self.wait(1.6)
        self.play(ReplacementTransform(rects1, rects2), run_time=1.8)
        self.wait(1.4)
        self.play(ReplacementTransform(rects2, rects3), run_time=1.8)
        self.wait(1.4)
        self.play(FadeOut(rects3), FadeIn(area), run_time=1.6)
        self.wait(1.5)

        integral_steps = VGroup(
            MathTex(r"\int_0^2 x^2\,dx", color=TEXT),
            MathTex(r"=\left[\frac{x^3}{3}\right]_0^2", color=ACCENT),
            MathTex(r"=\frac{2^3}{3}-0", color=ACCENT),
            MathTex(r"=\frac{8}{3}", color=AREA).scale(1.05),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        integral_steps.scale(0.86)
        integral_steps.move_to(RIGHT * 3.7 + DOWN * 0.35)

        for step in integral_steps:
            self.play(Write(step), run_time=1.7)
            self.wait(1.1)

        result_box = SurroundingRectangle(
            integral_steps[-1], color=AREA, buff=0.14
        )
        self.play(Create(result_box), run_time=1.2)
        self.wait(2.5)

        self.play(
            FadeOut(area_box),
            FadeOut(riemann_text),
            FadeOut(result_box),
            *[FadeOut(mob) for mob in integral_steps],
            FadeOut(integ_title),
            FadeOut(area),
            FadeOut(left_line),
            FadeOut(right_line),
            run_time=1.5,
        )

        connect_title = Text(
            "3. Hubungan turunan dan integral",
            color=ACCENT,
            font_size=30,
        )
        connect_title.to_corner(UR).shift(LEFT * 0.3 + DOWN * 0.2)

        connection = VGroup(
            MathTex(r"\frac{d}{dx}(x^2)=2x", color=DERIV),
            MathTex(r"\int x^2\,dx=\frac{x^3}{3}+C", color=AREA),
            Text("Turunan memberi laju perubahan.", color=TEXT, font_size=24),
            Text("Integral memberi akumulasi luas.", color=TEXT, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        connection.scale(0.9)
        connection.move_to(RIGHT * 3.8 + DOWN * 0.25)

        self.play(FadeIn(connect_title), run_time=1.2)
        for item in connection:
            self.play(Write(item), run_time=1.5)
            self.wait(1.0)

        final_text = MathTex(
            r"\int_0^2 x^2\,dx=\frac{8}{3}",
            color=AREA,
        ).scale(1.15)
        final_text.to_edge(DOWN, buff=0.35)

        self.play(Write(final_text), run_time=1.7)
        self.wait(3)
