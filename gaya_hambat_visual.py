from manim import *
import numpy as np

# Colorful math-animation palette inspired by 3Blue1Brown's visual language.
BG = "#0B0F14"
BLUE = "#58C4DD"       # velocity / curves
YELLOW = "#F4D35E"     # applied force / derivative
GREEN = "#6BCB77"      # integral / result
PINK = "#FF6B9A"       # drag force
PURPLE = "#C792EA"     # algebra transformations
WHITE = "#E8EDF2"
MUTED = "#AAB4C0"
PANEL = "#263342"

config.background_color = BG


class DragForceSlow(Scene):
    def section_title(self, text, color=WHITE):
        title = Text(text, font_size=35, color=color, weight=BOLD)
        title.to_edge(UP, buff=0.28)
        return title

    def panel(self, width, height, center, color=PANEL):
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

    def clear_scene(self, wait=0.4):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.2)
        self.wait(wait)

    def construct(self):
        self.camera.background_color = BG

        m = 2.5
        F = 10.0
        C = 2.0
        vmax = 4.91
        vinf = F / C
        k = C / m
        t1 = -(m / C) * np.log(1 - C * vmax / F)
        t2 = (m / C) * np.log(2)
        total = t1 + t2

        # ============================================================
        # INTRO: READ BEFORE SOLVING
        # ============================================================
        title = Text("Balok dengan Hambatan Udara Linear", font_size=42, color=WHITE)
        subtitle = MathTex(r"F_d=Cv", color=PINK).scale(1.25)
        intro = VGroup(title, subtitle).arrange(DOWN, buff=0.35)

        self.play(Write(title), run_time=1.8)
        self.play(Write(subtitle), run_time=1.4)
        self.wait(2.0)

        data = VGroup(
            MathTex(r"m=2.5\ \mathrm{kg}", color=WHITE),
            MathTex(r"F=10\ \mathrm N", color=YELLOW),
            MathTex(r"C=2\ \mathrm{N\,s/m}", color=PINK),
            MathTex(r"v_{\max}=4.91\ \mathrm{m/s}", color=BLUE),
        ).arrange(RIGHT, buff=0.65).scale(0.72)
        data.to_edge(DOWN, buff=0.65)

        self.play(FadeIn(data, shift=UP*0.15), run_time=1.5)
        self.wait(2.2)

        phase_note = Text(
            "Kunci: gerak terdiri dari dua fase yang persamaannya berbeda.",
            font_size=25, color=MUTED
        )
        phase_note.next_to(intro, DOWN, buff=0.75)
        self.play(FadeIn(phase_note), run_time=1.3)
        self.wait(2.8)
        self.clear_scene()

        # ============================================================
        # PHASE 1: FORCES + WHY dv/dt APPEARS
        # ============================================================
        title = self.section_title("Fase 1 — balok masih didorong", BLUE)
        self.play(Write(title), run_time=1.5)

        left = self.panel(5.5, 5.2, LEFT*3.7 + DOWN*0.2, BLUE)
        right = self.panel(6.8, 5.2, RIGHT*3.1 + DOWN*0.2, YELLOW)
        self.play(Create(left), Create(right), run_time=1.4)

        block = RoundedRectangle(
            width=2.0, height=1.1, corner_radius=0.12,
            stroke_color=WHITE, fill_color=BLUE, fill_opacity=0.12
        ).move_to(left.get_center()+DOWN*0.1)
        block_text = MathTex("m", color=WHITE).move_to(block)

        push = Arrow(block.get_right(), block.get_right()+RIGHT*1.55, color=YELLOW, buff=0.04)
        drag = Arrow(block.get_left(), block.get_left()+LEFT*1.55, color=PINK, buff=0.04)
        vel = Arrow(
            block.get_top()+UP*0.72+LEFT*0.65,
            block.get_top()+UP*0.72+RIGHT*0.9,
            color=BLUE, buff=0
        )

        self.play(Create(block), Write(block_text), run_time=1.0)
        self.play(GrowArrow(push), Write(MathTex("F", color=YELLOW).next_to(push, UP, buff=0.1)), run_time=1.2)
        self.wait(0.8)
        self.play(GrowArrow(drag), Write(MathTex(r"Cv", color=PINK).next_to(drag, UP, buff=0.1)), run_time=1.2)
        self.wait(0.8)
        self.play(GrowArrow(vel), Write(MathTex("v", color=BLUE).next_to(vel, UP, buff=0.1)), run_time=1.2)
        self.wait(1.4)

        right_head = Text("Mengubah gaya menjadi persamaan gerak", font_size=23, color=YELLOW, weight=BOLD)
        right_head.move_to(right.get_top()+DOWN*0.42)
        self.play(Write(right_head), run_time=1.2)

        n2 = MathTex(r"\sum F_x=ma", color=WHITE).scale(0.92)
        n2.move_to(right.get_center()+UP*1.25)
        self.play(Write(n2), run_time=1.5)
        self.wait(1.2)

        accel = MathTex(r"a=\frac{dv}{dt}", color=YELLOW).scale(0.92)
        accel.next_to(n2, DOWN, buff=0.45)
        self.play(Write(accel), run_time=1.5)
        self.wait(1.4)

        meaning = Text(
            "dv/dt = seberapa cepat kecepatan berubah terhadap waktu",
            font_size=20, color=MUTED
        )
        meaning.next_to(accel, DOWN, buff=0.33)
        self.play(FadeIn(meaning), run_time=1.2)
        self.wait(1.8)

        ode = MathTex(
            r"F-Cv=m\frac{dv}{dt}",
            color=WHITE
        ).scale(1.0)
        ode.move_to(right.get_center()+DOWN*1.25)
        ode.set_color_by_tex("F", YELLOW)
        ode.set_color_by_tex("Cv", PINK)
        ode.set_color_by_tex(r"\frac{dv}{dt}", BLUE)

        self.play(Write(ode), run_time=1.8)
        self.wait(2.8)
        self.clear_scene()

        # ============================================================
        # PHASE 1: SEPARATE VARIABLES SLOWLY
        # ============================================================
        title = self.section_title("Fase 1 — pisahkan variabel sebelum mengintegralkan", PURPLE)
        self.play(Write(title), run_time=1.5)

        panel = self.panel(11.5, 5.25, DOWN*0.25, PURPLE)
        self.play(Create(panel), run_time=1.1)

        steps = [
            MathTex(r"F-Cv=m\frac{dv}{dt}", color=WHITE),
            MathTex(r"\frac{1}{F-Cv}\frac{dv}{dt}=\frac{1}{m}", color=WHITE),
            MathTex(r"\frac{dv}{F-Cv}=\frac{dt}{m}", color=WHITE),
        ]
        ys = [1.25, 0.25, -0.75]

        for eq, y in zip(steps, ys):
            eq.scale(0.95).move_to(UP*y)
            self.play(Write(eq), run_time=1.8)
            self.wait(1.3)

        explain_sep = VGroup(
            Text("Kiri hanya memuat v.", font_size=23, color=BLUE),
            Text("Kanan hanya memuat t.", font_size=23, color=YELLOW),
        ).arrange(RIGHT, buff=1.1)
        explain_sep.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(explain_sep), run_time=1.2)
        self.wait(2.4)
        self.clear_scene()

        # ============================================================
        # PHASE 1: INTEGRAL WITH BOUNDS
        # ============================================================
        title = self.section_title("Fase 1 — integral kedua ruas, pelan-pelan", GREEN)
        self.play(Write(title), run_time=1.5)

        panel = self.panel(12.0, 5.35, DOWN*0.25, GREEN)
        self.play(Create(panel), run_time=1.1)

        line1 = MathTex(
            r"\frac{dv}{F-Cv}=\frac{dt}{m}", color=WHITE
        ).scale(0.88).move_to(UP*1.45)
        self.play(Write(line1), run_time=1.5)
        self.wait(1.2)

        bounds_note = Text(
            "Saat t = 0, v = 0.  Saat t = t, kecepatannya v.",
            font_size=22, color=MUTED
        ).next_to(line1, DOWN, buff=0.28)
        self.play(FadeIn(bounds_note), run_time=1.2)
        self.wait(1.5)

        integral = MathTex(
            r"\int_{0}^{v}\frac{dv'}{F-Cv'}"
            r"="
            r"\int_{0}^{t}\frac{dt'}{m}",
            color=WHITE
        ).scale(0.92).move_to(UP*0.15)
        integral.set_color_by_tex(r"\int_{0}^{v}", BLUE)
        integral.set_color_by_tex(r"\int_{0}^{t}", YELLOW)
        self.play(Write(integral), run_time=2.2)
        self.wait(2.0)

        anti_left = MathTex(
            r"\int\frac{dv'}{F-Cv'}"
            r"=-\frac{1}{C}\ln(F-Cv')",
            color=GREEN
        ).scale(0.82).move_to(DOWN*0.85)
        self.play(Write(anti_left), run_time=2.0)
        self.wait(1.8)

        evaluated = MathTex(
            r"\left[-\frac1C\ln(F-Cv')\right]_{0}^{v}"
            r"="
            r"\left[\frac{t'}{m}\right]_{0}^{t}",
            color=WHITE
        ).scale(0.82).move_to(DOWN*1.75)
        self.play(Write(evaluated), run_time=2.2)
        self.wait(2.5)
        self.clear_scene()

        # ============================================================
        # PHASE 1: SIMPLIFY THE INTEGRAL RESULT
        # ============================================================
        title = self.section_title("Fase 1 — dari hasil integral ke fungsi v(t)", BLUE)
        self.play(Write(title), run_time=1.5)

        panel = self.panel(11.8, 5.35, DOWN*0.25, BLUE)
        self.play(Create(panel), run_time=1.1)

        simplify = VGroup(
            MathTex(
                r"-\frac1C\ln(F-Cv)+\frac1C\ln F=\frac{t}{m}",
                color=WHITE
            ),
            MathTex(
                r"\frac1C\ln\left(\frac{F}{F-Cv}\right)=\frac{t}{m}",
                color=PURPLE
            ),
            MathTex(
                r"\ln\left(\frac{F}{F-Cv}\right)=\frac{Ct}{m}",
                color=PURPLE
            ),
            MathTex(
                r"\frac{F}{F-Cv}=e^{Ct/m}",
                color=WHITE
            ),
            MathTex(
                r"F-Cv=Fe^{-Ct/m}",
                color=WHITE
            ),
            MathTex(
                r"\boxed{v(t)=\frac{F}{C}\left(1-e^{-Ct/m}\right)}",
                color=BLUE
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        simplify.scale(0.72)
        simplify.move_to(DOWN*0.15)

        for i, eq in enumerate(simplify):
            self.play(Write(eq), run_time=1.7)
            self.wait(1.1 if i < 5 else 2.2)

        self.clear_scene()

        # ============================================================
        # PHASE 1: PHYSICAL GRAPH + FIND t1
        # ============================================================
        title = self.section_title("Fase 1 — sekarang baru masukkan v_max", BLUE)
        self.play(Write(title), run_time=1.5)

        axes = Axes(
            x_range=[0, 5.6, 1],
            y_range=[0, 5.5, 1],
            x_length=7.2,
            y_length=4.8,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 21, "color": WHITE},
        ).move_to(LEFT*3.1 + DOWN*0.35)
        curve = axes.plot(
            lambda t: vinf*(1-np.exp(-k*t)),
            x_range=[0,5.35],
            color=BLUE, stroke_width=5
        )
        terminal = DashedLine(axes.c2p(0,vinf), axes.c2p(5.3,vinf), color=GREEN)
        vmaxline = DashedLine(axes.c2p(0,vmax), axes.c2p(t1,vmax), color=YELLOW)
        tline = DashedLine(axes.c2p(t1,0), axes.c2p(t1,vmax), color=YELLOW)

        self.play(Create(axes), Create(curve), run_time=2.0)
        self.play(Create(terminal), run_time=1.0)

        side = self.panel(5.1, 5.0, RIGHT*4.1 + DOWN*0.25, BLUE)
        self.play(Create(side), run_time=1.0)

        terminal_eq = MathTex(
            r"v_\infty=\frac{F}{C}=5.00\ \mathrm{m/s}",
            color=GREEN
        ).scale(0.78).move_to(side.get_center()+UP*1.55)
        target_eq = MathTex(
            r"v_{\max}=4.91\ \mathrm{m/s}",
            color=YELLOW
        ).scale(0.78).next_to(terminal_eq, DOWN, buff=0.34)
        near = Text(
            "4.91 m/s sangat dekat dengan 5.00 m/s.",
            font_size=21, color=MUTED
        ).next_to(target_eq, DOWN, buff=0.32)

        self.play(Write(terminal_eq), run_time=1.4)
        self.play(Write(target_eq), run_time=1.4)
        self.play(FadeIn(near), run_time=1.0)
        self.wait(1.5)

        self.play(Create(vmaxline), Create(tline), run_time=1.4)

        t1_eqs = VGroup(
            MathTex(
                r"4.91=5\left(1-e^{-0.8t_1}\right)",
                color=WHITE
            ),
            MathTex(
                r"e^{-0.8t_1}=0.018",
                color=PURPLE
            ),
            MathTex(
                r"t_1=-\frac{\ln(0.018)}{0.8}",
                color=PURPLE
            ),
            MathTex(
                r"\boxed{t_1\approx5.02\ \mathrm{s}}",
                color=YELLOW
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).scale(0.70)
        t1_eqs.move_to(side.get_center()+DOWN*0.65)

        for eq in t1_eqs:
            self.play(Write(eq), run_time=1.6)
            self.wait(1.0)
        self.wait(2.0)
        self.clear_scene()

        # ============================================================
        # PHASE 2: FORCE REMOVED + DERIVATIVE
        # ============================================================
        title = self.section_title("Fase 2 — gaya dorong dihentikan", PURPLE)
        self.play(Write(title), run_time=1.5)

        left = self.panel(5.5, 5.2, LEFT*3.7 + DOWN*0.2, PURPLE)
        right = self.panel(6.8, 5.2, RIGHT*3.1 + DOWN*0.2, PINK)
        self.play(Create(left), Create(right), run_time=1.4)

        block = RoundedRectangle(
            width=2.0, height=1.1, corner_radius=0.12,
            stroke_color=WHITE, fill_color=BLUE, fill_opacity=0.12
        ).move_to(left.get_center()+DOWN*0.1)
        drag = Arrow(block.get_left(), block.get_left()+LEFT*1.6, color=PINK, buff=0.04)
        vel = Arrow(
            block.get_top()+UP*0.72+LEFT*0.65,
            block.get_top()+UP*0.72+RIGHT*0.9,
            color=BLUE, buff=0
        )
        self.play(Create(block), GrowArrow(drag), GrowArrow(vel), run_time=1.3)
        self.play(
            Write(MathTex(r"Cv", color=PINK).next_to(drag, UP, buff=0.1)),
            Write(MathTex("v", color=BLUE).next_to(vel, UP, buff=0.1)),
            run_time=1.0
        )

        note = Text("Sekarang tidak ada gaya F ke kanan.", font_size=22, color=MUTED)
        note.next_to(block, DOWN, buff=0.7)
        self.play(FadeIn(note), run_time=1.0)
        self.wait(1.5)

        ode2 = VGroup(
            MathTex(r"\sum F_x=ma", color=WHITE),
            MathTex(r"-Cv=m\frac{dv}{d\tau}", color=WHITE),
            MathTex(r"\frac{dv}{v}=-\frac{C}{m}\,d\tau", color=PURPLE),
        ).arrange(DOWN, buff=0.45).scale(0.88)
        ode2.move_to(right.get_center()+UP*0.45)

        for eq in ode2:
            self.play(Write(eq), run_time=1.7)
            self.wait(1.1)

        tau = Text("τ = waktu sejak gaya dorong dilepas", font_size=21, color=MUTED)
        tau.move_to(right.get_bottom()+UP*0.55)
        self.play(FadeIn(tau), run_time=1.1)
        self.wait(2.3)
        self.clear_scene()

        # ============================================================
        # PHASE 2: INTEGRAL WITH BOUNDS
        # ============================================================
        title = self.section_title("Fase 2 — integralkan dari v_max ke v", GREEN)
        self.play(Write(title), run_time=1.5)

        panel = self.panel(11.8, 5.35, DOWN*0.25, GREEN)
        self.play(Create(panel), run_time=1.0)

        phase2_steps = VGroup(
            MathTex(
                r"\int_{v_{\max}}^{v}\frac{dv'}{v'}"
                r"="
                r"-\frac{C}{m}\int_{0}^{\tau}d\tau'",
                color=WHITE
            ),
            MathTex(
                r"\left[\ln v'\right]_{v_{\max}}^{v}"
                r"="
                r"-\frac{C}{m}\tau",
                color=GREEN
            ),
            MathTex(
                r"\ln v-\ln v_{\max}=-\frac{C\tau}{m}",
                color=PURPLE
            ),
            MathTex(
                r"\ln\left(\frac{v}{v_{\max}}\right)=-\frac{C\tau}{m}",
                color=PURPLE
            ),
            MathTex(
                r"\boxed{v(\tau)=v_{\max}e^{-C\tau/m}}",
                color=BLUE
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).scale(0.75)
        phase2_steps.move_to(DOWN*0.12)

        for eq in phase2_steps:
            self.play(Write(eq), run_time=1.8)
            self.wait(1.2)
        self.wait(2.3)
        self.clear_scene()

        # ============================================================
        # HALF SPEED
        # ============================================================
        title = self.section_title("Fase 2 — kapan kecepatannya menjadi setengah?", YELLOW)
        self.play(Write(title), run_time=1.5)

        panel = self.panel(10.8, 5.0, DOWN*0.2, YELLOW)
        self.play(Create(panel), run_time=1.0)

        half_steps = VGroup(
            MathTex(
                r"\frac12v_{\max}=v_{\max}e^{-Ct_2/m}",
                color=WHITE
            ),
            MathTex(
                r"\frac12=e^{-Ct_2/m}",
                color=PURPLE
            ),
            MathTex(
                r"\ln\left(\frac12\right)=-\frac{Ct_2}{m}",
                color=PURPLE
            ),
            MathTex(
                r"t_2=\frac{m}{C}\ln2",
                color=GREEN
            ),
            MathTex(
                r"t_2=\frac{2.5}{2}\ln2\approx0.866\ \mathrm{s}",
                color=YELLOW
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.27).scale(0.78)
        half_steps.move_to(DOWN*0.1)

        for eq in half_steps:
            self.play(Write(eq), run_time=1.7)
            self.wait(1.15)
        self.wait(2.5)
        self.clear_scene()

        # ============================================================
        # FINAL GRAPH: BOTH PHASES
        # ============================================================
        title = self.section_title("Gabungkan kedua fase", WHITE)
        self.play(Write(title), run_time=1.5)

        axes = Axes(
            x_range=[0, 6.6, 1],
            y_range=[0, 5.5, 1],
            x_length=8.7,
            y_length=4.7,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 21, "color": WHITE},
        ).move_to(LEFT*1.8 + DOWN*0.35)

        phase1 = axes.plot(
            lambda t: vinf*(1-np.exp(-k*t)),
            x_range=[0,t1],
            color=BLUE, stroke_width=5
        )
        phase2 = axes.plot(
            lambda t: vmax*np.exp(-k*(t-t1)),
            x_range=[t1,total],
            color=PURPLE, stroke_width=5
        )

        switch_line = DashedLine(axes.c2p(t1,0), axes.c2p(t1,vmax), color=YELLOW)
        half_line = DashedLine(axes.c2p(total,0), axes.c2p(total,vmax/2), color=GREEN)

        self.play(Create(axes), run_time=1.5)
        self.play(Create(phase1), run_time=2.0)
        self.play(Create(switch_line), run_time=1.0)
        self.wait(1.0)
        self.play(Create(phase2), run_time=1.7)
        self.play(Create(half_line), run_time=1.0)

        side = self.panel(4.1, 4.7, RIGHT*5.0 + DOWN*0.25, WHITE)
        self.play(Create(side), run_time=1.0)

        summary = VGroup(
            Text("Durasi", font_size=25, color=WHITE, weight=BOLD),
            MathTex(r"t_1\approx5.02\ \mathrm{s}", color=BLUE),
            MathTex(r"t_2\approx0.866\ \mathrm{s}", color=PURPLE),
            Line(LEFT*1.15, RIGHT*1.15, color=MUTED, stroke_width=1),
            MathTex(r"T=t_1+t_2", color=WHITE),
            MathTex(r"\boxed{T\approx5.89\ \mathrm{s}}", color=GREEN),
        ).arrange(DOWN, buff=0.32).scale(0.82)
        summary.move_to(side)

        for item in summary:
            if isinstance(item, Line):
                self.play(Create(item), run_time=0.7)
            else:
                self.play(Write(item), run_time=1.2)
            self.wait(0.55)

        self.wait(3.0)
