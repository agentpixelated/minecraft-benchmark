from manim import *
import math

config.background_color = "#0f1117"


def fit_width(mob, max_width):
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def make_panel(width, height, title_text):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.16,
        stroke_width=1.5,
        stroke_color=GREY_B,
        fill_color="#171a22",
        fill_opacity=0.97,
    )
    title = Text(title_text, font_size=26, weight=BOLD)
    title.next_to(box.get_top(), DOWN, buff=0.18)
    return VGroup(box, title)


class LinearDragSolution(Scene):
    def construct(self):
        m = 2.5
        F = 10.0
        C = 2.0
        vmax = 4.91
        tau = m / C
        v_terminal = F / C
        t1 = -tau * math.log(1 - vmax / v_terminal)
        t2 = tau * math.log(2)
        total = t1 + t2

        # ---------- OPENING ----------
        title = Text("Balok dengan Hambatan Udara Linear", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.3)

        subtitle = Text(
            "Dua fase: didorong hingga 4,91 m/s, lalu dibiarkan melambat",
            font_size=24,
            color=GREY_A,
        )
        subtitle.next_to(title, DOWN, buff=0.15)

        givens_panel = RoundedRectangle(
            width=11.8,
            height=3.15,
            corner_radius=0.18,
            stroke_color=GREY_B,
            fill_color="#171a22",
            fill_opacity=0.97,
        ).shift(DOWN * 0.55)

        g1 = MathTex(r"m=2.5\,\mathrm{kg}", font_size=34)
        g2 = MathTex(r"F=10\,\mathrm{N}", font_size=34)
        g3 = MathTex(r"F_d=Cv", font_size=34)
        g4 = MathTex(r"C=2\,\mathrm{N/(m\,s^{-1})}", font_size=34)
        g5 = MathTex(r"v_{\max}=4.91\,\mathrm{m/s}", font_size=34)
        g6 = MathTex(r"v_{\text{akhir}}=\frac12 v_{\max}", font_size=34)

        left_g = VGroup(g1, g2, g3).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        right_g = VGroup(g4, g5, g6).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        givens = VGroup(left_g, right_g).arrange(RIGHT, buff=1.25, aligned_edge=UP)
        fit_width(givens, 10.9)
        givens.move_to(givens_panel.get_center())

        goal = MathTex(
            r"t_{\text{total}} = t_1+t_2 = ?",
            font_size=38,
            color=YELLOW,
        ).next_to(givens_panel, DOWN, buff=0.35)

        self.play(Write(title), FadeIn(subtitle))
        self.play(Create(givens_panel), FadeIn(givens))
        self.play(Write(goal))
        self.wait(1.3)
        self.play(FadeOut(givens_panel, givens, goal, subtitle))

        # ---------- PHASE 1 ----------
        phase1_header = Text(
            "Fase 1 • Gaya dorong masih bekerja",
            font_size=30,
            weight=BOLD,
        ).next_to(title, DOWN, buff=0.35)

        left_panel = make_panel(6.15, 5.25, "Visual gaya & kecepatan")
        right_panel = make_panel(6.65, 5.25, "Penyelesaian")
        left_panel.move_to(LEFT * 3.35 + DOWN * 0.45)
        right_panel.move_to(RIGHT * 3.25 + DOWN * 0.45)

        self.play(Write(phase1_header), FadeIn(left_panel, right_panel))

        # Diagram in left panel, upper half
        floor = Line(
            left_panel[0].get_left() + RIGHT * 0.55 + UP * 0.25,
            left_panel[0].get_right() + LEFT * 0.55 + UP * 0.25,
            stroke_width=3,
            color=GREY_A,
        )
        block = RoundedRectangle(
            width=1.2,
            height=0.75,
            corner_radius=0.08,
            fill_color=BLUE_D,
            fill_opacity=1,
            stroke_color=BLUE_B,
        ).move_to(floor.get_center() + UP * 0.39)

        push = Arrow(
            block.get_right() + RIGHT * 0.05,
            block.get_right() + RIGHT * 1.45,
            buff=0,
            color=GREEN_B,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.18,
        )
        drag = Arrow(
            block.get_left() + LEFT * 0.05,
            block.get_left() + LEFT * 1.2,
            buff=0,
            color=RED_B,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.2,
        )
        push_label = MathTex(r"F=10\,\mathrm N", font_size=28, color=GREEN_B)
        push_label.next_to(push, UP, buff=0.08)
        drag_label = MathTex(r"F_d=Cv", font_size=28, color=RED_B)
        drag_label.next_to(drag, UP, buff=0.08)

        v_arrow = Arrow(
            block.get_bottom() + DOWN * 0.15,
            block.get_bottom() + DOWN * 0.15 + RIGHT * 1.35,
            buff=0,
            color=YELLOW,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.18,
        )
        v_label = MathTex(r"v", font_size=28, color=YELLOW).next_to(v_arrow, DOWN, buff=0.04)

        self.play(Create(floor), FadeIn(block))
        self.play(GrowArrow(push), GrowArrow(drag), FadeIn(push_label, drag_label))
        self.play(GrowArrow(v_arrow), FadeIn(v_label))

        # Compact graph in lower half of left panel
        axes1 = Axes(
            x_range=[0, 5.6, 1],
            y_range=[0, 5.5, 1],
            x_length=4.65,
            y_length=2.15,
            axis_config={"include_ticks": True, "font_size": 18},
            tips=False,
        ).move_to(left_panel[0].get_center() + DOWN * 1.35)
        xlab1 = MathTex("t", font_size=22).next_to(axes1.x_axis.get_end(), RIGHT, buff=0.06)
        ylab1 = MathTex("v", font_size=22).next_to(axes1.y_axis.get_end(), UP, buff=0.06)
        curve1 = axes1.plot(
            lambda t: v_terminal * (1 - math.exp(-t / tau)),
            x_range=[0, 5.35],
            color=BLUE_B,
        )
        terminal_line = DashedLine(
            axes1.c2p(0, v_terminal),
            axes1.c2p(5.45, v_terminal),
            color=GREY_B,
            dash_length=0.07,
        )
        term_label = MathTex(r"5.00", font_size=18, color=GREY_A).next_to(
            axes1.c2p(0, v_terminal), LEFT, buff=0.08
        )
        dot1 = Dot(axes1.c2p(t1, vmax), radius=0.055, color=YELLOW)
        marker1 = DashedLine(
            axes1.c2p(t1, 0),
            axes1.c2p(t1, vmax),
            color=YELLOW,
            dash_length=0.06,
        )
        p1_label = MathTex(
            rf"(t_1,\,4.91)", font_size=20, color=YELLOW
        ).next_to(dot1, LEFT + DOWN, buff=0.12)

        self.play(Create(axes1), FadeIn(xlab1, ylab1))
        self.play(Create(terminal_line), FadeIn(term_label), Create(curve1))
        self.play(Create(marker1), FadeIn(dot1, p1_label))

        # Equations right panel. Separate lines, no crowding.
        eqs1 = VGroup(
            MathTex(r"m\frac{dv}{dt}=F-Cv", font_size=31),
            MathTex(r"\frac{dv}{F-Cv}=\frac{dt}{m}", font_size=31),
            MathTex(
                r"v(t)=\frac{F}{C}\left(1-e^{-Ct/m}\right)",
                font_size=31,
            ),
            MathTex(
                r"4.91=5\left(1-e^{-0.8t_1}\right)",
                font_size=31,
            ),
            MathTex(r"e^{-0.8t_1}=0.018", font_size=31),
            MathTex(
                r"t_1=\frac{-\ln(0.018)}{0.8}=5.02\,\mathrm s",
                font_size=31,
                color=YELLOW,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.31)
        fit_width(eqs1, 5.75)
        eqs1.move_to(right_panel[0].get_center() + DOWN * 0.15)

        for eq in eqs1:
            self.play(Write(eq), run_time=0.55)
        self.wait(1.3)

        # ---------- TRANSITION TO PHASE 2 ----------
        self.play(
            FadeOut(
                phase1_header,
                floor,
                block,
                push,
                drag,
                push_label,
                drag_label,
                v_arrow,
                v_label,
                axes1,
                xlab1,
                ylab1,
                curve1,
                terminal_line,
                term_label,
                dot1,
                marker1,
                p1_label,
                eqs1,
            )
        )

        phase2_header = Text(
            "Fase 2 • Gaya dorong dihentikan",
            font_size=30,
            weight=BOLD,
        ).next_to(title, DOWN, buff=0.35)
        self.play(Write(phase2_header))

        # Phase 2 diagram
        floor2 = Line(
            left_panel[0].get_left() + RIGHT * 0.55 + UP * 0.25,
            left_panel[0].get_right() + LEFT * 0.55 + UP * 0.25,
            stroke_width=3,
            color=GREY_A,
        )
        block2 = RoundedRectangle(
            width=1.2,
            height=0.75,
            corner_radius=0.08,
            fill_color=BLUE_D,
            fill_opacity=1,
            stroke_color=BLUE_B,
        ).move_to(floor2.get_center() + UP * 0.39)

        drag2 = Arrow(
            block2.get_left() + LEFT * 0.05,
            block2.get_left() + LEFT * 1.35,
            buff=0,
            color=RED_B,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.2,
        )
        drag2_label = MathTex(r"F_d=Cv", font_size=28, color=RED_B).next_to(
            drag2, UP, buff=0.08
        )
        no_push = Text("F = 0", font_size=25, color=GREY_A).next_to(
            block2, RIGHT, buff=0.55
        )
        v2_arrow = Arrow(
            block2.get_bottom() + DOWN * 0.15,
            block2.get_bottom() + DOWN * 0.15 + RIGHT * 1.25,
            buff=0,
            color=YELLOW,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.18,
        )
        v2_label = MathTex(r"v", font_size=28, color=YELLOW).next_to(
            v2_arrow, DOWN, buff=0.04
        )

        self.play(Create(floor2), FadeIn(block2, no_push))
        self.play(GrowArrow(drag2), FadeIn(drag2_label))
        self.play(GrowArrow(v2_arrow), FadeIn(v2_label))

        axes2 = Axes(
            x_range=[0, 1.5, 0.25],
            y_range=[0, 5.2, 1],
            x_length=4.65,
            y_length=2.15,
            axis_config={"include_ticks": True, "font_size": 18},
            tips=False,
        ).move_to(left_panel[0].get_center() + DOWN * 1.35)
        xlab2 = MathTex(r"t'", font_size=22).next_to(axes2.x_axis.get_end(), RIGHT, buff=0.06)
        ylab2 = MathTex("v", font_size=22).next_to(axes2.y_axis.get_end(), UP, buff=0.06)

        curve2 = axes2.plot(
            lambda t: vmax * math.exp(-t / tau),
            x_range=[0, 1.42],
            color=BLUE_B,
        )
        half_v = vmax / 2
        half_line = DashedLine(
            axes2.c2p(0, half_v),
            axes2.c2p(1.4, half_v),
            color=GREY_B,
            dash_length=0.06,
        )
        half_label = MathTex(
            r"\frac12v_{\max}", font_size=18, color=GREY_A
        ).next_to(axes2.c2p(0, half_v), LEFT, buff=0.08)
        dot2 = Dot(axes2.c2p(t2, half_v), radius=0.055, color=YELLOW)
        marker2 = DashedLine(
            axes2.c2p(t2, 0),
            axes2.c2p(t2, half_v),
            color=YELLOW,
            dash_length=0.06,
        )
        p2_label = MathTex(
            rf"(t_2,\,2.455)", font_size=20, color=YELLOW
        ).next_to(dot2, RIGHT + UP, buff=0.12)

        self.play(Create(axes2), FadeIn(xlab2, ylab2))
        self.play(Create(curve2), Create(half_line), FadeIn(half_label))
        self.play(Create(marker2), FadeIn(dot2, p2_label))

        eqs2 = VGroup(
            MathTex(r"m\frac{dv}{dt}=-Cv", font_size=31),
            MathTex(r"v(t')=v_{\max}e^{-Ct'/m}", font_size=31),
            MathTex(
                r"\frac12v_{\max}=v_{\max}e^{-0.8t_2}",
                font_size=31,
            ),
            MathTex(r"\frac12=e^{-0.8t_2}", font_size=31),
            MathTex(
                r"t_2=\frac{\ln 2}{0.8}=0.866\,\mathrm s",
                font_size=31,
                color=YELLOW,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        fit_width(eqs2, 5.75)
        eqs2.move_to(right_panel[0].get_center() + DOWN * 0.1)

        for eq in eqs2:
            self.play(Write(eq), run_time=0.58)
        self.wait(1.2)

        # ---------- FINAL ----------
        self.play(
            FadeOut(
                phase2_header,
                left_panel,
                right_panel,
                floor2,
                block2,
                drag2,
                drag2_label,
                no_push,
                v2_arrow,
                v2_label,
                axes2,
                xlab2,
                ylab2,
                curve2,
                half_line,
                half_label,
                dot2,
                marker2,
                p2_label,
                eqs2,
            )
        )

        final_panel = RoundedRectangle(
            width=10.6,
            height=4.2,
            corner_radius=0.18,
            stroke_color=GREY_B,
            fill_color="#171a22",
            fill_opacity=0.98,
        ).shift(DOWN * 0.25)

        final_title = Text("Total durasi", font_size=31, weight=BOLD)
        final_title.next_to(final_panel.get_top(), DOWN, buff=0.28)

        line1 = MathTex(
            r"t_{\text{total}}=t_1+t_2",
            font_size=39,
        )
        line2 = MathTex(
            rf"t_{{\text{{total}}}}=5.02+0.866",
            font_size=39,
        )
        line3 = MathTex(
            rf"\boxed{{t_{{\text{{total}}}}\approx {total:.2f}\,\mathrm{{s}}}}",
            font_size=46,
            color=YELLOW,
        )
        summary = VGroup(line1, line2, line3).arrange(DOWN, buff=0.42)
        summary.move_to(final_panel.get_center() + DOWN * 0.15)

        note = Text(
            "Kunci: waktu saat didorong dan waktu setelah gaya dilepas harus dijumlahkan.",
            font_size=23,
            color=GREY_A,
        ).next_to(final_panel, DOWN, buff=0.28)
        fit_width(note, 10.5)

        self.play(FadeIn(final_panel), Write(final_title))
        self.play(Write(line1))
        self.play(Write(line2))
        self.play(Write(line3))
        self.play(FadeIn(note))
        self.wait(2.5)
