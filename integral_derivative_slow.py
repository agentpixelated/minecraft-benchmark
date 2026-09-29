from manim import *
import numpy as np

# 3Blue1Brown-inspired palette, with a calmer dark background.
BG = "#0B0F14"
BLUE = "#58C4DD"
YELLOW = "#F4D35E"
GREEN = "#6BCB77"
PURPLE = "#C792EA"
PINK = "#FF7AA2"
WHITE_SOFT = "#E8EDF2"
MUTED = "#AAB4C0"
PANEL = "#263342"

config.background_color = BG


class SlowCalculus(Scene):
    def safe_title(self, text, color=WHITE_SOFT):
        t = Text(text, font_size=36, color=color, weight=BOLD)
        t.to_edge(UP, buff=0.28)
        return t

    def panel(self, width=5.0, height=5.3, center=RIGHT*4.0 + DOWN*0.2, color=PANEL):
        p = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.16,
            stroke_color=color,
            stroke_width=2,
            fill_color=BG,
            fill_opacity=0.25,
        )
        p.move_to(center)
        return p

    def construct(self):
        self.camera.background_color = BG

        # ============================================================
        # INTRO
        # ============================================================
        title = Text("Turunan dan Integral dari", font_size=42, color=WHITE_SOFT)
        func = MathTex(r"f(x)=x^2", color=BLUE).scale(1.35)
        intro = VGroup(title, func).arrange(DOWN, buff=0.32)

        self.play(Write(title), run_time=1.8)
        self.play(Write(func), run_time=1.6)
        self.wait(2.2)

        premise = Text(
            "Bukan menghafal rumus. Kita lihat dari mana rumusnya muncul.",
            font_size=25,
            color=MUTED,
        )
        premise.next_to(intro, DOWN, buff=0.65)
        self.play(FadeIn(premise, shift=UP*0.12), run_time=1.4)
        self.wait(2.8)
        self.play(FadeOut(intro), FadeOut(premise), run_time=1.3)

        # ============================================================
        # PART A — DERIVATIVE: SECANT TO TANGENT
        # ============================================================
        section = self.safe_title("1. Turunan: dari garis secant ke garis singgung", YELLOW)
        self.play(Write(section), run_time=1.5)

        axes = Axes(
            x_range=[0, 3.2, 0.5],
            y_range=[0, 9.5, 1],
            x_length=7.0,
            y_length=5.0,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 22, "color": WHITE_SOFT},
        ).move_to(LEFT*3.1 + DOWN*0.35)

        graph = axes.plot(lambda x: x*x, x_range=[0, 3.05], color=BLUE, stroke_width=5)
        graph_label = MathTex(r"f(x)=x^2", color=BLUE).scale(0.85)
        graph_label.move_to(axes.c2p(2.35, 6.3))

        self.play(Create(axes), run_time=1.8)
        self.play(Create(graph), FadeIn(graph_label), run_time=1.8)
        self.wait(1.5)

        x0 = 1.25
        h = ValueTracker(1.15)

        A = Dot(axes.c2p(x0, x0*x0), color=YELLOW, radius=0.08)
        A_label = MathTex("A", color=YELLOW).scale(0.8).next_to(A, DOWN+LEFT, buff=0.12)

        B = always_redraw(
            lambda: Dot(
                axes.c2p(x0+h.get_value(), (x0+h.get_value())**2),
                color=PINK,
                radius=0.08,
            )
        )
        B_label = always_redraw(
            lambda: MathTex("B", color=PINK).scale(0.8).next_to(B, UP+RIGHT, buff=0.1)
        )

        secant = always_redraw(
            lambda: Line(
                axes.c2p(x0-0.35, x0*x0 +
                    (((x0+h.get_value())**2-x0*x0)/h.get_value())*(-0.35)),
                axes.c2p(x0+h.get_value()+0.35, (x0+h.get_value())**2 +
                    (((x0+h.get_value())**2-x0*x0)/h.get_value())*(0.35)),
                color=PINK,
                stroke_width=4,
            )
        )

        dx_line = always_redraw(
            lambda: Line(
                axes.c2p(x0, x0*x0),
                axes.c2p(x0+h.get_value(), x0*x0),
                color=PURPLE,
                stroke_width=4,
            )
        )
        dy_line = always_redraw(
            lambda: Line(
                axes.c2p(x0+h.get_value(), x0*x0),
                axes.c2p(x0+h.get_value(), (x0+h.get_value())**2),
                color=GREEN,
                stroke_width=4,
            )
        )

        dx_label = always_redraw(
            lambda: MathTex(r"\Delta x=h", color=PURPLE).scale(0.66).next_to(dx_line, DOWN, buff=0.1)
        )
        dy_label = always_redraw(
            lambda: MathTex(r"\Delta y", color=GREEN).scale(0.66).next_to(dy_line, RIGHT, buff=0.1)
        )

        self.play(FadeIn(A), Write(A_label), FadeIn(B), FadeIn(B_label), run_time=1.3)
        self.play(Create(secant), Create(dx_line), Create(dy_line), run_time=1.5)
        self.play(FadeIn(dx_label), FadeIn(dy_label), run_time=1.0)
        self.wait(2.0)

        right_panel = self.panel(width=5.2, height=5.25, center=RIGHT*4.15 + DOWN*0.25, color=YELLOW)
        panel_title = Text("Kemiringan secant", font_size=25, color=YELLOW, weight=BOLD)
        panel_title.move_to(right_panel.get_top()+DOWN*0.42)
        self.play(Create(right_panel), Write(panel_title), run_time=1.3)

        slope1 = MathTex(
            r"m_{\text{secant}}=\frac{\Delta y}{\Delta x}",
            color=WHITE_SOFT
        ).scale(0.82)
        slope2 = MathTex(
            r"=\frac{f(x+h)-f(x)}{h}",
            color=WHITE_SOFT
        ).scale(0.82)
        slope3 = MathTex(
            r"=\frac{(x+h)^2-x^2}{h}",
            color=WHITE_SOFT
        ).scale(0.82)

        secant_steps = VGroup(slope1, slope2, slope3).arrange(
            DOWN, aligned_edge=LEFT, buff=0.34
        )
        secant_steps.move_to(right_panel.get_center()+UP*0.55)

        for eq in secant_steps:
            self.play(Write(eq), run_time=1.6)
            self.wait(1.0)

        expansion = MathTex(
            r"(x+h)^2=x^2+2xh+h^2",
            color=PURPLE
        ).scale(0.76)
        expansion.next_to(secant_steps, DOWN, buff=0.45)
        self.play(Write(expansion), run_time=1.5)
        self.wait(1.4)

        simplification = MathTex(
            r"m_{\text{secant}}=2x+h",
            color=GREEN
        ).scale(0.9)
        simplification.next_to(expansion, DOWN, buff=0.38)
        self.play(Write(simplification), run_time=1.5)
        self.wait(2.0)

        # Move B closer to A slowly.
        close_text = Text(
            "Sekarang B kita dekatkan ke A...",
            font_size=23,
            color=MUTED,
        )
        close_text.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(close_text), run_time=1.0)
        self.play(h.animate.set_value(0.55), run_time=2.5)
        self.wait(1.0)
        self.play(h.animate.set_value(0.25), run_time=2.5)
        self.wait(1.0)
        self.play(h.animate.set_value(0.08), run_time=2.8)
        self.wait(1.2)

        limit_eq = MathTex(
            r"h\to 0\quad\Longrightarrow\quad m_{\text{secant}}\to 2x",
            color=YELLOW
        ).scale(0.78)
        limit_eq.move_to(right_panel.get_bottom()+UP*0.46)
        self.play(Transform(simplification, limit_eq), FadeOut(expansion), run_time=1.8)
        self.wait(2.0)

        derivative_eq = MathTex(
            r"\boxed{f'(x)=2x}",
            color=YELLOW
        ).scale(1.15)
        derivative_eq.move_to(right_panel.get_center()+DOWN*0.95)
        self.play(Write(derivative_eq), run_time=1.7)
        self.wait(2.2)

        # Replace secant geometry with actual tangent and demonstrate changing slope.
        self.play(
            FadeOut(B), FadeOut(B_label), FadeOut(dx_line), FadeOut(dy_line),
            FadeOut(dx_label), FadeOut(dy_label), FadeOut(secant),
            FadeOut(close_text),
            run_time=1.2,
        )

        x_tracker = ValueTracker(x0)

        moving_dot = always_redraw(
            lambda: Dot(
                axes.c2p(x_tracker.get_value(), x_tracker.get_value()**2),
                color=YELLOW,
                radius=0.08,
            )
        )

        def tangent_line():
            xv = x_tracker.get_value()
            m = 2*xv
            delta = 0.55
            xa, xb = xv-delta, xv+delta
            ya = xv**2 + m*(xa-xv)
            yb = xv**2 + m*(xb-xv)
            return Line(axes.c2p(xa, ya), axes.c2p(xb, yb), color=YELLOW, stroke_width=5)

        tangent = always_redraw(tangent_line)
        slope_readout = always_redraw(
            lambda: MathTex(
                rf"x={x_tracker.get_value():.1f}\qquad f'(x)={2*x_tracker.get_value():.1f}",
                color=WHITE_SOFT
            ).scale(0.72).move_to(right_panel.get_center()+UP*1.25)
        )

        self.play(FadeOut(A), FadeOut(A_label), FadeIn(moving_dot), Create(tangent), run_time=1.4)
        self.play(FadeOut(secant_steps), FadeOut(simplification), FadeIn(slope_readout), run_time=1.2)

        explanation = VGroup(
            Text("Turunan memberi", font_size=24, color=MUTED),
            Text("kemiringan lokal", font_size=27, color=YELLOW, weight=BOLD),
            Text("di setiap titik.", font_size=24, color=MUTED),
        ).arrange(DOWN, buff=0.18)
        explanation.move_to(right_panel.get_center()+DOWN*0.35)
        self.play(FadeIn(explanation), run_time=1.3)

        for xv in [0.5, 1.0, 1.5, 2.0, 2.5]:
            self.play(x_tracker.animate.set_value(xv), run_time=2.2)
            self.wait(0.8)

        self.wait(2.0)
        self.play(
            FadeOut(section), FadeOut(axes), FadeOut(graph), FadeOut(graph_label),
            FadeOut(right_panel), FadeOut(panel_title), FadeOut(derivative_eq),
            FadeOut(moving_dot), FadeOut(tangent), FadeOut(slope_readout),
            FadeOut(explanation),
            run_time=1.5,
        )

        # ============================================================
        # PART B — INTEGRAL: RIEMANN SUM TO AREA
        # ============================================================
        section = self.safe_title("2. Integral: dari potongan luas ke luas kontinu", GREEN)
        self.play(Write(section), run_time=1.5)

        axes = Axes(
            x_range=[0, 3.2, 0.5],
            y_range=[0, 9.5, 1],
            x_length=7.0,
            y_length=5.0,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 22, "color": WHITE_SOFT},
        ).move_to(LEFT*3.1 + DOWN*0.35)

        graph = axes.plot(lambda x: x*x, x_range=[0, 3.05], color=BLUE, stroke_width=5)
        graph_label = MathTex(r"f(x)=x^2", color=BLUE).scale(0.85)
        graph_label.move_to(axes.c2p(2.35, 6.3))

        self.play(Create(axes), Create(graph), FadeIn(graph_label), run_time=2.0)

        left_bound = DashedLine(axes.c2p(0,0), axes.c2p(0,0.25), color=GREEN)
        right_bound = DashedLine(axes.c2p(2,0), axes.c2p(2,4), color=GREEN)
        self.play(Create(left_bound), Create(right_bound), run_time=1.1)

        right_panel = self.panel(width=5.2, height=5.25, center=RIGHT*4.15 + DOWN*0.25, color=GREEN)
        panel_title = Text("Ide integral", font_size=25, color=GREEN, weight=BOLD)
        panel_title.move_to(right_panel.get_top()+DOWN*0.42)
        self.play(Create(right_panel), Write(panel_title), run_time=1.3)

        idea = VGroup(
            Text("Luas kurva sulit dihitung", font_size=23, color=MUTED),
            Text("sekaligus.", font_size=23, color=MUTED),
            Text("Maka kita pecah menjadi", font_size=23, color=MUTED),
            Text("persegi panjang kecil.", font_size=25, color=GREEN, weight=BOLD),
        ).arrange(DOWN, buff=0.16)
        idea.move_to(right_panel.get_center()+UP*0.75)
        for line in idea:
            self.play(FadeIn(line), run_time=0.75)
        self.wait(1.6)

        rects_05 = axes.get_riemann_rectangles(
            graph, x_range=[0,2], dx=0.5, input_sample_type="right",
            stroke_width=1.3, fill_opacity=0.62, color=[GREEN, BLUE]
        )
        self.play(FadeIn(rects_05), run_time=1.8)

        sum_eq = MathTex(
            r"A\approx\sum f(x_i)\,\Delta x",
            color=WHITE_SOFT
        ).scale(0.82)
        sum_eq.move_to(right_panel.get_center()+DOWN*0.55)
        self.play(Write(sum_eq), run_time=1.6)
        self.wait(2.0)

        dx05 = MathTex(r"\Delta x=0.5", color=PURPLE).scale(0.75)
        dx05.move_to(right_panel.get_bottom()+UP*0.55)
        self.play(Write(dx05), run_time=1.1)

        rects_025 = axes.get_riemann_rectangles(
            graph, x_range=[0,2], dx=0.25, input_sample_type="right",
            stroke_width=0.9, fill_opacity=0.62, color=[GREEN, BLUE]
        )
        dx025 = MathTex(r"\Delta x=0.25", color=PURPLE).scale(0.75).move_to(dx05)

        self.play(ReplacementTransform(rects_05, rects_025), Transform(dx05, dx025), run_time=2.2)
        self.wait(1.5)

        rects_0125 = axes.get_riemann_rectangles(
            graph, x_range=[0,2], dx=0.125, input_sample_type="right",
            stroke_width=0.5, fill_opacity=0.62, color=[GREEN, BLUE]
        )
        dx0125 = MathTex(r"\Delta x=0.125", color=PURPLE).scale(0.75).move_to(dx05)

        self.play(ReplacementTransform(rects_025, rects_0125), Transform(dx05, dx0125), run_time=2.2)
        self.wait(1.5)

        limit_text = MathTex(r"\Delta x\to0", color=YELLOW).scale(0.8).move_to(dx05)
        self.play(Transform(dx05, limit_text), run_time=1.4)
        self.wait(1.2)

        area = axes.get_area(graph, x_range=[0,2], color=GREEN, opacity=0.50)
        integral_symbol = MathTex(
            r"A=\int_0^2 x^2\,dx",
            color=GREEN
        ).scale(0.92)
        integral_symbol.move_to(right_panel.get_center()+DOWN*0.55)

        self.play(FadeOut(rects_0125), FadeIn(area), run_time=1.8)
        self.play(Transform(sum_eq, integral_symbol), run_time=1.5)
        self.wait(2.4)

        self.play(FadeOut(idea), FadeOut(dx05), run_time=1.0)

        # Antiderivative slowly, in a clear panel.
        why = Text("Sekarang: bagaimana menghitung integralnya?", font_size=22, color=MUTED)
        why.move_to(right_panel.get_center()+UP*1.35)
        self.play(FadeIn(why), run_time=1.2)
        self.wait(1.2)

        inverse_hint = MathTex(
            r"\frac{d}{dx}\left(\frac{x^3}{3}\right)=x^2",
            color=YELLOW
        ).scale(0.76)
        inverse_hint.move_to(right_panel.get_center()+UP*0.72)
        self.play(Write(inverse_hint), run_time=1.7)
        self.wait(1.5)

        step1 = MathTex(r"\int_0^2 x^2\,dx", color=WHITE_SOFT).scale(0.82)
        step2 = MathTex(r"=\left[\frac{x^3}{3}\right]_0^2", color=PURPLE).scale(0.82)
        step3 = MathTex(r"=\frac{2^3}{3}-\frac{0^3}{3}", color=PURPLE).scale(0.82)
        step4 = MathTex(r"=\frac{8}{3}", color=GREEN).scale(1.05)

        calc = VGroup(step1, step2, step3, step4).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22
        )
        calc.move_to(right_panel.get_center()+DOWN*0.72)

        self.play(FadeOut(sum_eq), run_time=0.7)
        for step in calc:
            self.play(Write(step), run_time=1.6)
            self.wait(1.0)

        box = SurroundingRectangle(step4, color=GREEN, buff=0.12)
        self.play(Create(box), run_time=1.0)
        self.wait(2.6)

        self.play(
            FadeOut(section), FadeOut(axes), FadeOut(graph), FadeOut(graph_label),
            FadeOut(left_bound), FadeOut(right_bound), FadeOut(area),
            FadeOut(right_panel), FadeOut(panel_title), FadeOut(why),
            FadeOut(inverse_hint), FadeOut(calc), FadeOut(box),
            run_time=1.5,
        )

        # ============================================================
        # PART C — CONNECTION
        # ============================================================
        section = self.safe_title("3. Kenapa turunan dan integral saling terhubung?", PURPLE)
        self.play(Write(section), run_time=1.5)

        left_card = RoundedRectangle(
            width=5.4, height=3.6, corner_radius=0.18,
            stroke_color=YELLOW, stroke_width=2,
            fill_color=BG, fill_opacity=0.3
        ).move_to(LEFT*3.2 + DOWN*0.2)

        right_card = RoundedRectangle(
            width=5.4, height=3.6, corner_radius=0.18,
            stroke_color=GREEN, stroke_width=2,
            fill_color=BG, fill_opacity=0.3
        ).move_to(RIGHT*3.2 + DOWN*0.2)

        self.play(Create(left_card), Create(right_card), run_time=1.5)

        d_title = Text("Turunan", font_size=29, color=YELLOW, weight=BOLD)
        d_title.move_to(left_card.get_top()+DOWN*0.48)
        i_title = Text("Integral", font_size=29, color=GREEN, weight=BOLD)
        i_title.move_to(right_card.get_top()+DOWN*0.48)

        d_eq = MathTex(r"\frac{d}{dx}(x^2)=2x", color=YELLOW).scale(0.95)
        d_eq.move_to(left_card.get_center()+UP*0.35)
        d_txt = Text("mengukur perubahan lokal", font_size=23, color=MUTED)
        d_txt.next_to(d_eq, DOWN, buff=0.45)

        i_eq = MathTex(r"\int x^2\,dx=\frac{x^3}{3}+C", color=GREEN).scale(0.9)
        i_eq.move_to(right_card.get_center()+UP*0.35)
        i_txt = Text("mengukur akumulasi", font_size=23, color=MUTED)
        i_txt.next_to(i_eq, DOWN, buff=0.45)

        self.play(Write(d_title), Write(i_title), run_time=1.1)
        self.play(Write(d_eq), Write(i_eq), run_time=1.7)
        self.play(FadeIn(d_txt), FadeIn(i_txt), run_time=1.1)
        self.wait(2.2)

        bridge = MathTex(
            r"\frac{d}{dx}\left(\int_0^x t^2\,dt\right)=x^2",
            color=PURPLE
        ).scale(1.05)
        bridge.to_edge(DOWN, buff=0.55)

        self.play(Write(bridge), run_time=2.0)
        self.wait(3.0)

        final = VGroup(
            MathTex(r"f'(x)=2x", color=YELLOW),
            MathTex(r"\int_0^2 x^2\,dx=\frac{8}{3}", color=GREEN),
        ).arrange(DOWN, buff=0.35).scale(1.05)

        self.play(
            FadeOut(left_card), FadeOut(right_card), FadeOut(d_title), FadeOut(i_title),
            FadeOut(d_eq), FadeOut(i_eq), FadeOut(d_txt), FadeOut(i_txt),
            FadeOut(bridge), FadeOut(section),
            run_time=1.3,
        )
        self.play(FadeIn(final, shift=UP*0.15), run_time=1.5)
        self.wait(3.5)
