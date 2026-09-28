from manim import *
import numpy as np


class DragForceSolution(Scene):
    def clear_scene(self, wait=0.2):
        if self.mobjects:
            self.play(FadeOut(*self.mobjects), run_time=0.7)
        self.wait(wait)

    def section_title(self, text):
        title = Text(text, font_size=38, weight=BOLD)
        title.to_edge(UP, buff=0.35)
        return title

    def make_panel(self, width, height, center):
        panel = RoundedRectangle(
            corner_radius=0.18,
            width=width,
            height=height,
            stroke_width=1.5,
            fill_opacity=0.04,
        )
        panel.move_to(center)
        return panel

    def construct(self):
        # Constants
        m = 2.5
        F = 10.0
        C = 2.0
        vmax = 4.91
        vinf = F / C
        k = C / m
        t1 = -(m / C) * np.log(1 - C * vmax / F)
        t2 = (m / C) * np.log(2)
        total = t1 + t2

        # ------------------------------------------------------------
        # 1) Read the problem without solving it yet
        # ------------------------------------------------------------
        title = Text("Balok dengan hambatan linear", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.4)

        left_panel = self.make_panel(5.9, 4.7, LEFT * 3.35 + DOWN * 0.25)
        right_panel = self.make_panel(6.2, 4.7, RIGHT * 3.1 + DOWN * 0.25)

        data_head = Text("Data yang diberikan", font_size=27, weight=BOLD)
        data_head.move_to(left_panel.get_top() + DOWN * 0.45)

        data = VGroup(
            MathTex(r"m=2.5\ \mathrm{kg}"),
            MathTex(r"F=10\ \mathrm{N}"),
            MathTex(r"C=2\ \mathrm{N\,s/m}"),
            MathTex(r"v_{\max}=4.91\ \mathrm{m/s}"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        data.scale(0.9)
        data.next_to(data_head, DOWN, buff=0.45)

        goal_head = Text("Apa yang sebenarnya dicari?", font_size=27, weight=BOLD)
        goal_head.move_to(right_panel.get_top() + DOWN * 0.45)

        goal1 = MathTex(r"T_{\mathrm{total}}=t_1+t_2").scale(1.05)
        goal2 = Text(
            "t₁: waktu selama masih didorong",
            font_size=24,
        )
        goal3 = Text(
            "t₂: waktu setelah gaya dorong dilepas",
            font_size=24,
        )
        goal4 = MathTex(r"v:\ v_{\max}\longrightarrow \frac12 v_{\max}").scale(0.9)

        goals = VGroup(goal1, goal2, goal3, goal4).arrange(
            DOWN, aligned_edge=LEFT, buff=0.38
        )
        goals.next_to(goal_head, DOWN, buff=0.42)

        self.play(Write(title))
        self.play(Create(left_panel), Create(right_panel))
        self.play(Write(data_head))
        for item in data:
            self.play(Write(item), run_time=0.7)
            self.wait(0.25)
        self.play(Write(goal_head))
        for item in goals:
            self.play(Write(item), run_time=0.75)
            self.wait(0.3)

        note = Text(
            "Pisahkan gerak menjadi dua fase sebelum memasukkan angka.",
            font_size=25,
            slant=ITALIC,
        )
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note))
        self.wait(2.0)

        self.clear_scene()

        # ------------------------------------------------------------
        # 2) Phase 1: still pushed
        # ------------------------------------------------------------
        title = self.section_title("Fase 1 — balok masih didorong")

        left_panel = self.make_panel(5.6, 5.4, LEFT * 3.6 + DOWN * 0.25)
        right_panel = self.make_panel(7.0, 5.4, RIGHT * 3.0 + DOWN * 0.25)

        phase_label = Text("Diagram gaya", font_size=26, weight=BOLD)
        phase_label.move_to(left_panel.get_top() + DOWN * 0.45)

        block = RoundedRectangle(
            width=2.0, height=1.1, corner_radius=0.12, fill_opacity=0.12
        )
        block.move_to(left_panel.get_center() + DOWN * 0.25)
        block_text = MathTex("m").move_to(block)

        force_arrow = Arrow(
            block.get_right(), block.get_right() + RIGHT * 1.65, buff=0.05
        )
        drag_arrow = Arrow(
            block.get_left(), block.get_left() + LEFT * 1.65, buff=0.05
        )
        velocity_arrow = Arrow(
            block.get_top() + UP * 0.6 + LEFT * 0.7,
            block.get_top() + UP * 0.6 + RIGHT * 0.9,
            buff=0.0,
        )

        force_text = MathTex("F").next_to(force_arrow, UP, buff=0.12)
        drag_text = MathTex(r"F_d=Cv").next_to(drag_arrow, UP, buff=0.12)
        velocity_text = MathTex("v").next_to(velocity_arrow, UP, buff=0.08)

        physical_note = Text(
            "Hambatan selalu melawan arah gerak.",
            font_size=22,
        )
        physical_note.next_to(block, DOWN, buff=0.75)

        eq_head = Text("Hukum II Newton", font_size=26, weight=BOLD)
        eq_head.move_to(right_panel.get_top() + DOWN * 0.45)

        equations = VGroup(
            MathTex(r"\sum F_x=m\frac{dv}{dt}"),
            MathTex(r"F-Cv=m\frac{dv}{dt}"),
            MathTex(r"\frac{dv}{F-Cv}=\frac{dt}{m}"),
            MathTex(r"v(0)=0"),
            MathTex(r"v(t)=\frac{F}{C}\left(1-e^{-Ct/m}\right)"),
        )
        equations.arrange(DOWN, aligned_edge=LEFT, buff=0.33)
        equations.scale(0.82)
        equations.next_to(eq_head, DOWN, buff=0.38)

        self.play(Write(title), Create(left_panel), Create(right_panel))
        self.play(Write(phase_label), Write(eq_head))
        self.play(Create(block), Write(block_text))
        self.play(GrowArrow(force_arrow), Write(force_text))
        self.play(GrowArrow(drag_arrow), Write(drag_text))
        self.play(GrowArrow(velocity_arrow), Write(velocity_text))
        self.play(FadeIn(physical_note))
        self.wait(1.3)

        for i, eq in enumerate(equations):
            self.play(Write(eq), run_time=0.9)
            self.wait(0.55 if i < 4 else 1.2)

        self.clear_scene()

        # ------------------------------------------------------------
        # 3) Understand phase 1 before solving t1
        # ------------------------------------------------------------
        title = self.section_title("Mengapa mencapai 4.91 m/s membutuhkan waktu cukup lama?")

        axes = Axes(
            x_range=[0, 5.5, 1],
            y_range=[0, 5.5, 1],
            x_length=7.7,
            y_length=4.8,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 22},
        )
        axes.shift(LEFT * 2.3 + DOWN * 0.4)
        x_label = axes.get_x_axis_label(MathTex("t\ (s)").scale(0.8))
        y_label = axes.get_y_axis_label(MathTex("v\ (m/s)").scale(0.8))

        curve = axes.plot(
            lambda t: vinf * (1 - np.exp(-k * t)),
            x_range=[0, 5.3],
        )

        terminal_line = DashedLine(
            axes.c2p(0, vinf),
            axes.c2p(5.3, vinf),
            stroke_width=2,
        )
        target_line = DashedLine(
            axes.c2p(0, vmax),
            axes.c2p(t1, vmax),
            stroke_width=2,
        )
        time_line = DashedLine(
            axes.c2p(t1, 0),
            axes.c2p(t1, vmax),
            stroke_width=2,
        )
        target_dot = Dot(axes.c2p(t1, vmax), radius=0.07)

        info_panel = self.make_panel(4.6, 4.6, RIGHT * 4.15 + DOWN * 0.35)
        info_head = Text("Makna grafik", font_size=25, weight=BOLD)
        info_head.move_to(info_panel.get_top() + DOWN * 0.45)

        info = VGroup(
            MathTex(r"v_{\infty}=\frac{F}{C}=5.00\ \mathrm{m/s}"),
            MathTex(r"v_{\max}=4.91\ \mathrm{m/s}"),
            MathTex(r"\frac{v_{\max}}{v_{\infty}}=98.2\%"),
            Text("Kecepatan mendekati batas", font_size=22),
            Text("secara eksponensial.", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        info.scale(0.9)
        info.next_to(info_head, DOWN, buff=0.38)

        self.play(Write(title))
        self.play(Create(axes), FadeIn(x_label, y_label), Create(info_panel))
        self.play(Create(curve), run_time=1.6)
        self.play(Create(terminal_line), run_time=0.7)
        self.play(Write(info_head))
        for item in info:
            self.play(Write(item), run_time=0.65)
        self.play(Create(target_line), Create(time_line), FadeIn(target_dot))
        self.wait(2.2)

        self.clear_scene()

        # ------------------------------------------------------------
        # 4) Solve t1 symbolically first
        # ------------------------------------------------------------
        title = self.section_title("Menentukan waktu fase 1")

        panel = self.make_panel(11.8, 5.5, DOWN * 0.25)
        head = Text(
            "Gunakan v(t₁) = vₘₐₓ, lalu isolasi t₁",
            font_size=26,
            weight=BOLD,
        )
        head.move_to(panel.get_top() + DOWN * 0.45)

        eqs = VGroup(
            MathTex(r"v_{\max}=\frac{F}{C}\left(1-e^{-Ct_1/m}\right)"),
            MathTex(r"\frac{Cv_{\max}}{F}=1-e^{-Ct_1/m}"),
            MathTex(r"e^{-Ct_1/m}=1-\frac{Cv_{\max}}{F}"),
            MathTex(r"t_1=-\frac{m}{C}\ln\left(1-\frac{Cv_{\max}}{F}\right)"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        eqs.scale(0.84)
        eqs.next_to(head, DOWN, buff=0.4)

        self.play(Write(title), Create(panel), Write(head))
        for eq in eqs:
            self.play(Write(eq), run_time=0.9)
            self.wait(0.65)

        numeric = MathTex(
            r"t_1=-\frac{2.5}{2}\ln\left(1-\frac{(2)(4.91)}{10}\right)"
            r"\approx 5.02\ \mathrm{s}"
        ).scale(0.82)
        numeric.next_to(eqs, DOWN, buff=0.55)

        self.play(Write(numeric), run_time=1.2)
        self.wait(2.0)

        self.clear_scene()

        # ------------------------------------------------------------
        # 5) Phase 2: push removed
        # ------------------------------------------------------------
        title = self.section_title("Fase 2 — gaya dorong sudah dilepas")

        left_panel = self.make_panel(5.6, 5.4, LEFT * 3.6 + DOWN * 0.25)
        right_panel = self.make_panel(7.0, 5.4, RIGHT * 3.0 + DOWN * 0.25)

        phase_label = Text("Diagram gaya", font_size=26, weight=BOLD)
        phase_label.move_to(left_panel.get_top() + DOWN * 0.45)

        block = RoundedRectangle(
            width=2.0, height=1.1, corner_radius=0.12, fill_opacity=0.12
        )
        block.move_to(left_panel.get_center() + DOWN * 0.15)
        block_text = MathTex("m").move_to(block)

        drag_arrow = Arrow(
            block.get_left(), block.get_left() + LEFT * 1.75, buff=0.05
        )
        drag_text = MathTex(r"F_d=Cv").next_to(drag_arrow, UP, buff=0.12)
        velocity_arrow = Arrow(
            block.get_top() + UP * 0.6 + LEFT * 0.7,
            block.get_top() + UP * 0.6 + RIGHT * 0.9,
            buff=0.0,
        )
        velocity_text = MathTex("v").next_to(velocity_arrow, UP, buff=0.08)

        no_push = Text("Tidak ada lagi gaya F.", font_size=23)
        no_push.next_to(block, DOWN, buff=0.78)

        eq_head = Text("Persamaan gerak", font_size=26, weight=BOLD)
        eq_head.move_to(right_panel.get_top() + DOWN * 0.45)

        equations = VGroup(
            MathTex(r"m\frac{dv}{d\tau}=-Cv"),
            MathTex(r"\frac{dv}{v}=-\frac{C}{m}\,d\tau"),
            MathTex(r"v(0)=v_{\max}"),
            MathTex(r"v(\tau)=v_{\max}e^{-C\tau/m}"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        equations.scale(0.86)
        equations.next_to(eq_head, DOWN, buff=0.45)

        tau_note = Text(
            "τ dihitung mulai saat dorongan dihentikan.",
            font_size=21,
        )
        tau_note.next_to(equations, DOWN, buff=0.48)

        self.play(Write(title), Create(left_panel), Create(right_panel))
        self.play(Write(phase_label), Write(eq_head))
        self.play(Create(block), Write(block_text))
        self.play(GrowArrow(drag_arrow), Write(drag_text))
        self.play(GrowArrow(velocity_arrow), Write(velocity_text))
        self.play(FadeIn(no_push))
        self.wait(1.2)

        for eq in equations:
            self.play(Write(eq), run_time=0.9)
            self.wait(0.6)
        self.play(FadeIn(tau_note))
        self.wait(1.6)

        self.clear_scene()

        # ------------------------------------------------------------
        # 6) Solve t2
        # ------------------------------------------------------------
        title = self.section_title("Menentukan waktu fase 2")

        panel = self.make_panel(11.6, 5.4, DOWN * 0.25)
        head = Text(
            "Target: kecepatan turun menjadi setengah vₘₐₓ",
            font_size=26,
            weight=BOLD,
        )
        head.move_to(panel.get_top() + DOWN * 0.45)

        eqs = VGroup(
            MathTex(r"\frac12 v_{\max}=v_{\max}e^{-Ct_2/m}"),
            MathTex(r"\frac12=e^{-Ct_2/m}"),
            MathTex(r"\ln\left(\frac12\right)=-\frac{Ct_2}{m}"),
            MathTex(r"t_2=\frac{m}{C}\ln 2"),
            MathTex(r"t_2=\frac{2.5}{2}\ln 2\approx 0.866\ \mathrm{s}"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        eqs.scale(0.82)
        eqs.next_to(head, DOWN, buff=0.38)

        self.play(Write(title), Create(panel), Write(head))
        for eq in eqs:
            self.play(Write(eq), run_time=0.9)
            self.wait(0.6)
        self.wait(1.8)

        self.clear_scene()

        # ------------------------------------------------------------
        # 7) Put both phases on one time axis
        # ------------------------------------------------------------
        title = self.section_title("Gabungkan kedua fase")

        axes = Axes(
            x_range=[0, 6.6, 1],
            y_range=[0, 5.5, 1],
            x_length=9.2,
            y_length=4.5,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 21},
        )
        axes.shift(LEFT * 1.45 + DOWN * 0.45)

        x_label = axes.get_x_axis_label(MathTex("t\ (s)").scale(0.8))
        y_label = axes.get_y_axis_label(MathTex("v\ (m/s)").scale(0.8))

        phase1_curve = axes.plot(
            lambda t: vinf * (1 - np.exp(-k * t)),
            x_range=[0, t1],
        )
        phase2_curve = axes.plot(
            lambda t: vmax * np.exp(-k * (t - t1)),
            x_range=[t1, total],
        )

        switch_line = DashedLine(
            axes.c2p(t1, 0), axes.c2p(t1, vmax), stroke_width=2
        )
        finish_v = vmax / 2
        finish_line = DashedLine(
            axes.c2p(total, 0), axes.c2p(total, finish_v), stroke_width=2
        )

        switch_dot = Dot(axes.c2p(t1, vmax), radius=0.07)
        finish_dot = Dot(axes.c2p(total, finish_v), radius=0.07)

        info_panel = self.make_panel(3.55, 4.7, RIGHT * 5.25 + DOWN * 0.35)
        info = VGroup(
            Text("Ringkasan waktu", font_size=24, weight=BOLD),
            MathTex(r"t_1\approx 5.02\ \mathrm{s}"),
            MathTex(r"t_2\approx 0.866\ \mathrm{s}"),
            Line(LEFT * 1.25, RIGHT * 1.25, stroke_width=1),
            MathTex(r"T=t_1+t_2"),
            MathTex(r"T\approx 5.89\ \mathrm{s}"),
        ).arrange(DOWN, buff=0.35)
        info.scale(0.88)
        info.move_to(info_panel)

        self.play(Write(title))
        self.play(Create(axes), FadeIn(x_label, y_label), Create(info_panel))
        self.play(Create(phase1_curve), run_time=1.8)
        self.play(Create(switch_line), FadeIn(switch_dot))
        self.wait(0.8)
        self.play(Create(phase2_curve), run_time=1.2)
        self.play(Create(finish_line), FadeIn(finish_dot))
        self.wait(0.8)
        for item in info:
            self.play(Write(item) if not isinstance(item, Line) else Create(item), run_time=0.7)
            self.wait(0.3)

        self.wait(2.0)

        self.clear_scene()

        # ------------------------------------------------------------
        # 8) Final answer only after the process
        # ------------------------------------------------------------
        title = Text("Hasil akhir", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.55)

        result = MathTex(
            r"T_{\mathrm{total}}"
            r"=5.02+0.866"
            r"\approx 5.89\ \mathrm{s}"
        ).scale(1.15)

        box = SurroundingRectangle(result, buff=0.28, stroke_width=2)

        takeaway = VGroup(
            Text("Inti proses:", font_size=27, weight=BOLD),
            Text("1. Pisahkan dua fase gaya.", font_size=24),
            Text("2. Turunkan ODE dari Hukum II Newton.", font_size=24),
            Text("3. Selesaikan simbolik terlebih dahulu.", font_size=24),
            Text("4. Baru substitusi angka dan jumlahkan waktu.", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        takeaway.next_to(result, DOWN, buff=0.75)

        self.play(Write(title))
        self.play(Write(result), Create(box), run_time=1.4)
        self.wait(1.0)
        for item in takeaway:
            self.play(FadeIn(item), run_time=0.55)
            self.wait(0.25)
        self.wait(2.5)
