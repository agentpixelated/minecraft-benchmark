from manim import *
import numpy as np

# Visual language inspired by the educational principles of 3Blue1Brown:
# dark field, semantic colors, minimal chrome, transformations instead of slides.
BG = "#1C1C1C"
WHITE = "#FFFFFF"
GREY = "#BBBBBB"
BLUE = "#58C4DD"      # velocity, v
YELLOW = "#FFFF00"    # applied force, F
RED = "#FC6255"       # drag force, Cv
GREEN = "#83C167"     # exponential / Euler operation / final result
PURPLE = "#9A72AC"    # logarithm / algebraic transformation
TEAL = "#5CD0B3"
ORANGE = "#FF862F"

config.background_color = BG


class LinearDragDeepDive(Scene):
    def M(self, *tex_strings, color=WHITE, **kwargs):
        return MathTex(*tex_strings, color=color, **kwargs)

    def color_math(self, mob):
        # Colors are isolated at construction time in M().
        return mob

    def title(self, text, color=WHITE):
        t = Text(text, font_size=34, color=WHITE, weight=BOLD)
        t.to_edge(UP, buff=0.28)
        return t

    def wipe(self, keep=None):
        keep = set(keep or [])
        mobs = [m for m in self.mobjects if m not in keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=1.1)
        self.wait(0.35)

    def construct(self):
        m, F, C, vmax = 2.5, 10.0, 2.0, 4.91
        vinf = F/C
        k = C/m
        t1 = -(m/C)*np.log(1 - C*vmax/F)
        t2 = (m/C)*np.log(2)
        total = t1+t2

        # ==========================================================
        # 0. WHAT THE PHYSICS IS SAYING
        # ==========================================================
        big = Text("Sebelum menghitung: apa yang sedang terjadi?", font_size=39, color=WHITE)
        self.play(Write(big), run_time=1.8)
        self.wait(1.8)
        self.play(big.animate.scale(0.72).to_edge(UP, buff=0.28), run_time=1.2)

        floor = Line(LEFT*5.2, RIGHT*5.2, color=GREY, stroke_width=2).shift(DOWN*1.45)
        block = RoundedRectangle(width=2.0, height=1.05, corner_radius=0.12,
                                 stroke_color=WHITE, fill_color="#172033", fill_opacity=1)
        block.move_to(DOWN*0.9)

        vtracker = ValueTracker(0.4)

        vel_arrow = always_redraw(lambda:
            Arrow(block.get_top()+UP*0.55+LEFT*0.8,
                  block.get_top()+UP*0.55+LEFT*0.8+RIGHT*(0.45+0.23*vtracker.get_value()),
                  color=BLUE, stroke_width=7, buff=0)
        )
        drag_arrow = always_redraw(lambda:
            Arrow(block.get_left(),
                  block.get_left()+LEFT*(0.35+0.23*vtracker.get_value()),
                  color=RED, stroke_width=7, buff=0)
        )
        push_arrow = Arrow(block.get_right(), block.get_right()+RIGHT*2.0,
                           color=YELLOW, stroke_width=7, buff=0)

        push_label = self.M(r"F=10\,\mathrm N", color=YELLOW).scale(0.82).next_to(push_arrow, UP, buff=0.12)
        vel_label = always_redraw(lambda:
            self.M(rf"v={vtracker.get_value():.1f}\,\mathrm{{m/s}}", color=BLUE)
            .scale(0.72).next_to(vel_arrow, UP, buff=0.08)
        )
        drag_label = always_redraw(lambda:
            self.M(r"F_d=Cv", color=RED).scale(0.76).next_to(drag_arrow, UP, buff=0.08)
        )

        self.play(Create(floor), Create(block), run_time=1.2)
        self.play(GrowArrow(push_arrow), Write(push_label), run_time=1.2)
        self.play(GrowArrow(vel_arrow), GrowArrow(drag_arrow), FadeIn(vel_label), FadeIn(drag_label), run_time=1.3)
        self.wait(1.2)

        sentence = Text(
            "Makin cepat balok bergerak, makin besar gaya hambatnya.",
            font_size=25, color=GREY
        ).to_edge(DOWN, buff=0.42)
        self.play(FadeIn(sentence), run_time=1.1)

        self.play(vtracker.animate.set_value(2.0), run_time=2.1)
        self.wait(0.8)
        self.play(vtracker.animate.set_value(4.0), run_time=2.1)
        self.wait(0.8)
        self.play(vtracker.animate.set_value(4.91), run_time=2.2)
        self.wait(1.5)

        balance = self.M(r"F-Cv", color=WHITE).scale(1.0)
        balance.set_color_by_tex("F", YELLOW)
        balance.set_color_by_tex("C", RED)
        balance.set_color_by_tex("v", BLUE)
        balance.next_to(block, DOWN, buff=0.55)
        self.play(Transform(sentence, balance), run_time=1.3)
        self.wait(2.0)
        self.wipe()

        # ==========================================================
        # 1. FORCE -> DIFFERENTIAL EQUATION
        # ==========================================================
        title = self.title("1. Dari diagram gaya ke persamaan diferensial", BLUE)
        self.play(Write(title), run_time=1.4)

        left_block = RoundedRectangle(width=1.9, height=1.0, corner_radius=0.12,
                                      stroke_color=WHITE, fill_color="#172033", fill_opacity=1)
        left_block.move_to(LEFT*3.8+DOWN*0.35)
        F_arrow = Arrow(left_block.get_right(), left_block.get_right()+RIGHT*1.9, color=YELLOW, buff=0)
        D_arrow = Arrow(left_block.get_left(), left_block.get_left()+LEFT*1.45, color=RED, buff=0)
        self.play(Create(left_block), GrowArrow(F_arrow), GrowArrow(D_arrow), run_time=1.4)
        self.play(
            Write(self.M("F", color=YELLOW).next_to(F_arrow, UP, buff=0.08)),
            Write(self.M("Cv", color=RED).next_to(D_arrow, UP, buff=0.08)),
            run_time=1.0
        )

        eq1 = self.M(r"\sum F_x = ma", color=WHITE).scale(1.0).move_to(RIGHT*2.7+UP*1.35)
        eq2 = self.M(r"F-Cv = ma", color=WHITE).scale(1.0).move_to(eq1)
        eq3 = self.M(r"a=\frac{dv}{dt}", color=WHITE).scale(0.92).move_to(RIGHT*2.7+UP*0.25)
        eq4 = self.M(r"F-Cv=m\frac{dv}{dt}", color=WHITE).scale(1.05).move_to(RIGHT*2.7+DOWN*1.0)

        for eq in [eq1,eq2,eq3,eq4]:
            self.color_math(eq)

        self.play(Write(eq1), run_time=1.4)
        self.wait(1.0)
        self.play(TransformMatchingTex(eq1, eq2), run_time=1.4)
        self.wait(1.0)
        self.play(Write(eq3), run_time=1.4)
        self.wait(1.5)

        deriv_note = VGroup(
            Text("dv", font_size=25, color=BLUE),
            Text("perubahan kecil pada kecepatan", font_size=21, color=GREY),
            Text("dt", font_size=25, color=TEAL),
            Text("perubahan kecil pada waktu", font_size=21, color=GREY),
        ).arrange(DOWN, buff=0.10).move_to(RIGHT*2.7+DOWN*0.55)
        self.play(FadeIn(deriv_note), run_time=1.2)
        self.wait(2.2)
        self.play(FadeOut(deriv_note), run_time=0.8)
        self.play(Write(eq4), run_time=1.6)
        self.wait(2.4)
        self.wipe()

        # ==========================================================
        # 2. SEPARATE VARIABLES
        # ==========================================================
        title = self.title("2. Pisahkan v dan t dengan operasi yang sama", PURPLE)
        self.play(Write(title), run_time=1.3)

        eq = self.M(r"F-Cv=m\frac{dv}{dt}", color=WHITE).scale(1.22).move_to(UP*1.45)
        self.color_math(eq)
        self.play(Write(eq), run_time=1.5)
        self.wait(1.2)

        divide_left = self.M(r"\div(F-Cv)", color=RED).scale(0.82).move_to(LEFT*3.7+UP*0.2)
        divide_right = divide_left.copy().move_to(RIGHT*3.7+UP*0.2)
        caption = Text("bagi KEDUA ruas dengan (F − Cv)", font_size=23, color=GREY).move_to(UP*0.25)
        self.play(FadeIn(caption), FadeIn(divide_left), FadeIn(divide_right), run_time=1.0)
        self.wait(1.0)

        eq_div = self.M(
            r"1=\frac{m}{F-Cv}\frac{dv}{dt}",
            color=WHITE
        ).scale(1.15).move_to(DOWN*0.65)
        self.color_math(eq_div)
        self.play(
            TransformMatchingTex(eq.copy(), eq_div),
            FadeOut(divide_left), FadeOut(divide_right), FadeOut(caption),
            run_time=1.7
        )
        self.wait(1.5)

        factor_left = self.M(r"\times\frac{dt}{m}", color=TEAL).scale(0.88).move_to(LEFT*3.7+DOWN*1.7)
        factor_right = factor_left.copy().move_to(RIGHT*3.7+DOWN*1.7)
        caption2 = Text("kalikan KEDUA ruas dengan dt/m", font_size=23, color=GREY).move_to(DOWN*1.55)
        self.play(FadeIn(caption2), FadeIn(factor_left), FadeIn(factor_right), run_time=1.0)
        self.wait(1.0)

        separated = self.M(
            r"\frac{dv}{F-Cv}=\frac{dt}{m}",
            color=WHITE
        ).scale(1.28).move_to(DOWN*0.55)
        self.color_math(separated)
        self.play(
            ReplacementTransform(eq_div, separated),
            FadeOut(factor_left), FadeOut(factor_right), FadeOut(caption2),
            FadeOut(eq),
            run_time=1.8
        )
        self.wait(1.2)

        left_tag = VGroup(
            Underline(separated, color=BLUE, buff=0.12),
            Text("semua yang memuat v di kiri", font_size=22, color=BLUE)
        )
        left_tag[1].next_to(separated, DOWN, buff=0.35)
        time_tag = Text("semua yang memuat t di kanan", font_size=22, color=TEAL)
        time_tag.next_to(left_tag[1], DOWN, buff=0.18)
        self.play(Create(left_tag[0]), FadeIn(left_tag[1]), FadeIn(time_tag), run_time=1.2)
        self.wait(2.6)
        self.wipe()

        # ==========================================================
        # 3. INTEGRATE LEFT SIDE CAREFULLY
        # ==========================================================
        title = self.title("3. Integral ruas kiri: jangan lompat langkah", GREEN)
        self.play(Write(title), run_time=1.4)

        integ_left = self.M(r"\int_0^v \frac{dv'}{F-Cv'}", color=WHITE).scale(1.25).move_to(UP*2.0)
        self.color_math(integ_left)
        self.play(Write(integ_left), run_time=1.7)
        self.wait(1.2)

        sub1 = self.M(r"u=F-Cv'", color=PURPLE).scale(1.0).move_to(UP*0.95)
        sub2 = self.M(r"du=-C\,dv'", color=PURPLE).scale(1.0).move_to(UP*0.05)
        sub3 = self.M(r"dv'=-\frac{du}{C}", color=PURPLE).scale(1.0).move_to(DOWN*0.85)
        self.color_math(sub1); self.color_math(sub2); self.color_math(sub3)
        for q in [sub1, sub2, sub3]:
            self.play(Write(q), run_time=1.4)
            self.wait(0.9)

        bounds = VGroup(
            self.M(r"v'=0\Rightarrow u=F", color=WHITE),
            self.M(r"v'=v\Rightarrow u=F-Cv", color=WHITE),
        ).arrange(RIGHT, buff=1.0).scale(0.78).to_edge(DOWN, buff=0.48)
        for q in bounds: self.color_math(q)
        self.play(FadeIn(bounds), run_time=1.1)
        self.wait(2.1)
        self.wipe()

        title = self.title("4. Substitusi u mengubah integral menjadi logaritma", GREEN)
        self.play(Write(title), run_time=1.4)

        chain = [
            self.M(r"\int_0^v \frac{dv'}{F-Cv'}", color=WHITE),
            self.M(r"=-\frac1C\int_F^{F-Cv}\frac{du}{u}", color=WHITE),
            self.M(r"=-\frac1C\left[\ln u\right]_F^{F-Cv}", color=WHITE),
            self.M(r"=-\frac1C\left(\ln(F-Cv)-\ln F\right)", color=WHITE),
            self.M(r"=\frac1C\ln\left(\frac{F}{F-Cv}\right)", color=WHITE),
        ]
        positions=[1.8,0.9,0.0,-0.9,-1.8]
        for q,y in zip(chain,positions):
            self.color_math(q)
            q.scale(0.86).move_to(UP*y)
            self.play(Write(q), run_time=1.55)
            self.wait(0.9)
        self.wait(2.0)
        self.wipe()

        # ==========================================================
        # 5. RIGHT INTEGRAL + EQUATE
        # ==========================================================
        title=self.title("5. Integral ruas kanan lebih sederhana", TEAL)
        self.play(Write(title), run_time=1.3)

        r1=self.M(r"\int_0^t\frac{dt'}{m}", color=WHITE).scale(1.25).move_to(UP*1.35)
        r2=self.M(r"=\frac1m\left[t'\right]_0^t", color=WHITE).scale(1.05).move_to(UP*0.15)
        r3=self.M(r"=\frac{t}{m}", color=TEAL).scale(1.25).move_to(DOWN*1.05)
        self.color_math(r1); self.color_math(r2); self.color_math(r3)
        for q in [r1,r2,r3]:
            self.play(Write(q), run_time=1.5)
            self.wait(1.0)
        self.wait(1.7)
        self.wipe()

        title=self.title("6. Kedua hasil integral harus sama", WHITE)
        self.play(Write(title), run_time=1.3)

        both=self.M(
            r"\frac1C\ln\left(\frac{F}{F-Cv}\right)=\frac{t}{m}",
            color=WHITE
        ).scale(1.15).move_to(UP*1.1)
        self.color_math(both)
        self.play(Write(both), run_time=1.7)
        self.wait(1.4)

        multiply_c=self.M(
            r"\ln\left(\frac{F}{F-Cv}\right)=\frac{Ct}{m}",
            color=WHITE
        ).scale(1.15).move_to(DOWN*0.45)
        self.color_math(multiply_c)

        c_left=self.M("C", color=RED).scale(1.05).move_to(LEFT*4.2+UP*0.2)
        c_right=self.M("C", color=RED).scale(1.05).move_to(RIGHT*4.2+UP*0.2)
        same=Text("kalikan kedua ruas dengan C", font_size=22, color=GREY).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(same), FadeIn(c_left), FadeIn(c_right), run_time=1.0)
        self.play(c_left.animate.move_to(both.get_left()+LEFT*0.45),
                  c_right.animate.move_to(both.get_right()+RIGHT*0.45),
                  run_time=1.4)
        self.play(TransformMatchingTex(both.copy(), multiply_c),
                  FadeOut(c_left), FadeOut(c_right), FadeOut(same), run_time=1.7)
        self.wait(2.2)
        self.wipe()

        # ==========================================================
        # 7. THE EULER / EXPONENTIAL STEP IN FULL DETAIL
        # ==========================================================
        title=self.title("7. Terapkan fungsi eksponensial pada KEDUA ruas", GREEN)
        self.play(Write(title), run_time=1.4)

        base=self.M(
            r"\ln\left(\frac{F}{F-Cv}\right)",
            "=",
            r"\frac{Ct}{m}",
            color=WHITE
        ).scale(1.18).move_to(UP*1.75)
        self.color_math(base)
        base[0].set_color(PURPLE)
        base[2].set_color(TEAL)
        self.play(Write(base), run_time=1.7)
        self.wait(1.2)

        left_box=SurroundingRectangle(base[0], color=PURPLE, buff=0.15)
        right_box=SurroundingRectangle(base[2], color=TEAL, buff=0.15)
        self.play(Create(left_box), Create(right_box), run_time=1.0)

        warning=VGroup(
            Text("Bukan mengalikan dengan angka e.", font_size=24, color=GREY),
            Text("Fungsi x ↦ eˣ diterapkan ke masing-masing ruas.", font_size=24, color=GREEN),
        ).arrange(DOWN, buff=0.15).move_to(UP*0.5)
        self.play(FadeIn(warning), run_time=1.2)
        self.wait(2.2)

        opL=self.M(r"x\mapsto e^x", color=GREEN).scale(1.2).move_to(LEFT*2.65+DOWN*0.65)
        opR=self.M(r"x\mapsto e^x", color=GREEN).scale(1.2).move_to(RIGHT*2.65+DOWN*0.65)
        op_caption=Text("operasi identik di kiri dan kanan", font_size=21, color=GREY).move_to(DOWN*1.45)
        self.play(FadeIn(opL), FadeIn(opR), FadeIn(op_caption), run_time=1.1)

        arrL=Arrow(opL.get_top(), left_box.get_bottom(), color=GREEN, stroke_width=5, buff=0.08)
        arrR=Arrow(opR.get_top(), right_box.get_bottom(), color=GREEN, stroke_width=5, buff=0.08)
        self.play(GrowArrow(arrL), GrowArrow(arrR), run_time=1.2)
        self.wait(1.5)

        exp_both=self.M(
            r"e^{\,\ln\left(\frac{F}{F-Cv}\right)}",
            "=",
            r"e^{\,Ct/m}",
            color=WHITE
        ).scale(1.08).move_to(DOWN*2.05)
        self.color_math(exp_both)
        exp_both[0].set_color(GREEN)
        exp_both[2].set_color(GREEN)
        self.play(Write(exp_both), run_time=2.0)
        self.wait(2.0)

        inverse_rule=self.M(r"e^{\ln z}=z", color=GREEN).scale(0.95).to_corner(DR).shift(LEFT*0.4+UP*0.2)
        self.play(Write(inverse_rule), run_time=1.4)
        self.play(Circumscribe(exp_both[0], color=GREEN, fade_out=True), run_time=1.6)
        self.wait(2.0)

        simplified=self.M(
            r"\frac{F}{F-Cv}",
            "=",
            r"e^{Ct/m}",
            color=WHITE
        ).scale(1.18).move_to(DOWN*1.9)
        self.color_math(simplified)
        simplified[0].set_color(YELLOW)
        simplified[2].set_color(GREEN)
        self.play(
            TransformMatchingTex(exp_both, simplified),
            FadeOut(opL), FadeOut(opR), FadeOut(arrL), FadeOut(arrR),
            FadeOut(left_box), FadeOut(right_box), FadeOut(warning),
            FadeOut(op_caption), FadeOut(inverse_rule), FadeOut(base),
            run_time=1.8
        )
        self.wait(2.5)
        self.wipe()

        # ==========================================================
        # 8. VISUALIZE exp and log AS INVERSES
        # ==========================================================
        title=self.title("8. Mengapa e^(ln z) kembali menjadi z?", GREEN)
        self.play(Write(title), run_time=1.4)

        z=self.M("z", color=BLUE).scale(1.35).move_to(LEFT*4.5)
        lnz=self.M(r"\ln z", color=PURPLE).scale(1.35).move_to(ORIGIN)
        back=self.M("z", color=BLUE).scale(1.35).move_to(RIGHT*4.5)

        arr1=Arrow(z.get_right(), lnz.get_left(), color=PURPLE, buff=0.25)
        arr2=Arrow(lnz.get_right(), back.get_left(), color=GREEN, buff=0.25)
        lab1=self.M(r"\ln(\cdot)", color=PURPLE).scale(0.78).next_to(arr1, UP, buff=0.15)
        lab2=self.M(r"e^{(\cdot)}", color=GREEN).scale(0.78).next_to(arr2, UP, buff=0.15)

        self.play(Write(z), run_time=0.8)
        self.play(GrowArrow(arr1), Write(lab1), run_time=1.2)
        self.play(Write(lnz), run_time=1.0)
        self.wait(1.1)
        self.play(GrowArrow(arr2), Write(lab2), run_time=1.2)
        self.play(Write(back), run_time=1.0)
        self.wait(1.5)

        inverse=Text("log natural dan eksponensial saling membatalkan", font_size=24, color=GREY)
        inverse.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(inverse), run_time=1.1)
        self.wait(2.5)
        self.wipe()

        # ==========================================================
        # 9. AFTER EXPONENTIATING: EACH ALGEBRA STEP
        # ==========================================================
        title=self.title("9. Operasi yang sama tetap dilakukan pada kedua ruas", GREEN)
        self.play(Write(title), run_time=1.3)

        e2=self.M(
            r"\frac{F}{F-Cv}=e^{Ct/m}",
            color=WHITE
        ).scale(1.18).move_to(UP*1.75)
        self.color_math(e2)
        self.play(Write(e2), run_time=1.6)
        self.wait(1.2)

        factorL=self.M(r"\times(F-Cv)", color=RED).scale(1.0).move_to(LEFT*3.6+UP*0.55)
        factorR=factorL.copy().move_to(RIGHT*3.6+UP*0.55)
        equal_ops=Text("operasi kiri = operasi kanan", font_size=22, color=GREY).move_to(UP*0.35)
        self.play(FadeIn(factorL), FadeIn(factorR), FadeIn(equal_ops), run_time=1.0)
        self.play(
            factorL.animate.move_to(LEFT*2.25+UP*1.0),
            factorR.animate.move_to(RIGHT*2.25+UP*1.0),
            run_time=1.3
        )
        self.wait(1.0)

        e3=self.M(
            r"F=(F-Cv)e^{Ct/m}",
            color=WHITE
        ).scale(1.12).move_to(DOWN*0.15)
        self.color_math(e3)
        self.play(
            Write(e3), FadeOut(factorL), FadeOut(factorR), FadeOut(equal_ops),
            run_time=1.6
        )
        self.wait(1.5)

        factor2L=self.M(r"\times e^{-Ct/m}", color=GREEN).scale(0.95).move_to(LEFT*3.6+DOWN*1.15)
        factor2R=factor2L.copy().move_to(RIGHT*3.6+DOWN*1.15)
        why2=Text("kalikan kedua ruas dengan e⁻ᶜᵗ⁄ᵐ", font_size=22, color=GREY).move_to(DOWN*1.25)
        self.play(FadeIn(factor2L), FadeIn(factor2R), FadeIn(why2), run_time=1.0)
        self.wait(1.1)

        e4=self.M(
            r"Fe^{-Ct/m}=F-Cv",
            color=WHITE
        ).scale(1.18).move_to(DOWN*2.0)
        self.color_math(e4)
        self.play(
            Write(e4), FadeOut(factor2L), FadeOut(factor2R), FadeOut(why2),
            run_time=1.7
        )
        self.wait(2.3)
        self.wipe()

        title=self.title("10. Isolasi v", BLUE)
        self.play(Write(title), run_time=1.2)

        iso=[
            self.M(r"Fe^{-Ct/m}=F-Cv",color=WHITE),
            self.M(r"Cv=F-Fe^{-Ct/m}",color=WHITE),
            self.M(r"Cv=F\left(1-e^{-Ct/m}\right)",color=WHITE),
            self.M(r"\boxed{v(t)=\frac FC\left(1-e^{-Ct/m}\right)}",color=WHITE),
        ]
        ys=[1.65,0.55,-0.55,-1.65]
        for q,y in zip(iso,ys):
            self.color_math(q)
            q.scale(0.98 if y>-1 else 1.05).move_to(UP*y)
            self.play(Write(q),run_time=1.6)
            self.wait(1.0)
        self.wait(2.4)
        self.wipe()

        # ==========================================================
        # 11. PHYSICAL MEANING OF THE EXPONENTIAL SOLUTION
        # ==========================================================
        title=self.title("11. Apa arti bentuk eksponensial ini secara fisik?", BLUE)
        self.play(Write(title),run_time=1.3)

        axes=Axes(
            x_range=[0,6,1],y_range=[0,5.5,1],
            x_length=8.0,y_length=4.8,tips=False,
            axis_config={"include_numbers":True,"font_size":21,"color":WHITE}
        ).shift(LEFT*1.8+DOWN*0.35)
        curve=axes.plot(lambda t:vinf*(1-np.exp(-k*t)),x_range=[0,5.7],color=BLUE,stroke_width=5)
        terminal=DashedLine(axes.c2p(0,vinf),axes.c2p(5.7,vinf),color=GREEN,stroke_width=3)
        self.play(Create(axes),Create(curve),run_time=2.0)
        self.play(Create(terminal),run_time=1.0)

        terminal_label=self.M(r"\frac FC=5.00\,\mathrm{m/s}",color=GREEN).scale(0.78)
        terminal_label.next_to(terminal,UP,buff=0.12).shift(RIGHT*1.9)
        self.play(Write(terminal_label),run_time=1.2)

        formula=self.M(r"v(t)=\frac FC\left(1-e^{-Ct/m}\right)",color=WHITE).scale(0.86)
        self.color_math(formula)
        formula.move_to(RIGHT*4.5+UP*1.35)
        self.play(Write(formula),run_time=1.5)

        decay=self.M(r"e^{-Ct/m}\longrightarrow0",color=GREEN).scale(0.86).next_to(formula,DOWN,buff=0.55)
        limit=self.M(r"v(t)\longrightarrow\frac FC",color=BLUE).scale(0.9).next_to(decay,DOWN,buff=0.38)
        self.play(Write(decay),run_time=1.4)
        self.wait(1.1)
        self.play(Write(limit),run_time=1.4)
        self.wait(2.3)
        self.wipe()

        # ==========================================================
        # 12. t1
        # ==========================================================
        title=self.title("12. Waktu sampai v_max = 4.91 m/s", YELLOW)
        self.play(Write(title),run_time=1.3)
        t1eqs=[
            self.M(r"4.91=5\left(1-e^{-0.8t_1}\right)",color=WHITE),
            self.M(r"0.982=1-e^{-0.8t_1}",color=WHITE),
            self.M(r"e^{-0.8t_1}=0.018",color=GREEN),
            self.M(r"-0.8t_1=\ln(0.018)",color=PURPLE),
            self.M(r"t_1=-\frac{\ln(0.018)}{0.8}",color=WHITE),
            self.M(r"\boxed{t_1\approx5.02\,\mathrm s}",color=YELLOW),
        ]
        ypos=[2.0,1.2,0.4,-0.4,-1.2,-2.0]
        for q,y in zip(t1eqs,ypos):
            self.color_math(q)
            q.scale(0.82).move_to(UP*y)
            self.play(Write(q),run_time=1.5)
            self.wait(0.9)
        self.wait(2.0)
        self.wipe()

        # ==========================================================
        # 13. PHASE 2
        # ==========================================================
        title=self.title("13. Fase 2: gaya dorong hilang", RED)
        self.play(Write(title),run_time=1.3)

        eqp2=self.M(r"-Cv=m\frac{dv}{d\tau}",color=WHITE).scale(1.1).move_to(UP*1.55)
        sep2=self.M(r"\frac{dv}{v}=-\frac Cm\,d\tau",color=WHITE).scale(1.05).move_to(UP*0.45)
        int2=self.M(
            r"\int_{v_{\max}}^v\frac{dv'}{v'}"
            r"=-\frac Cm\int_0^\tau d\tau'",
            color=WHITE
        ).scale(0.92).move_to(DOWN*0.65)
        result2=self.M(
            r"\ln\left(\frac{v}{v_{\max}}\right)=-\frac{C\tau}{m}",
            color=WHITE
        ).scale(0.98).move_to(DOWN*1.75)
        for q in [eqp2,sep2,int2,result2]: self.color_math(q)
        for q in [eqp2,sep2,int2,result2]:
            self.play(Write(q),run_time=1.6)
            self.wait(1.0)
        self.wait(1.8)
        self.wipe()

        # ==========================================================
        # 14. EULER STEP PHASE 2 TOO
        # ==========================================================
        title=self.title("14. Lagi: terapkan e^(·) pada kedua ruas", GREEN)
        self.play(Write(title),run_time=1.3)

        p2a=self.M(
            r"\ln\left(\frac{v}{v_{\max}}\right)=-\frac{C\tau}{m}",
            color=WHITE
        ).scale(1.05).move_to(UP*1.45)
        self.color_math(p2a)
        p2a.set_color(PURPLE)
        self.play(Write(p2a),run_time=1.4)

        ops=VGroup(
            self.M(r"e^{(\cdot)}",color=GREEN).scale(0.9).move_to(LEFT*2.6+UP*0.3),
            self.M(r"e^{(\cdot)}",color=GREEN).scale(0.9).move_to(RIGHT*2.6+UP*0.3),
        )
        self.play(FadeIn(ops),run_time=1.0)
        self.wait(1.0)

        p2b=self.M(
            r"e^{\,\ln(v/v_{\max})}=e^{-C\tau/m}",
            color=WHITE
        ).scale(1.0).move_to(DOWN*0.05)
        self.color_math(p2b)
        p2b.set_color(GREEN)
        self.play(Write(p2b),run_time=1.7)
        self.wait(1.3)

        p2c=self.M(
            r"\frac{v}{v_{\max}}=e^{-C\tau/m}",
            color=WHITE
        ).scale(1.05).move_to(DOWN*1.15)
        self.color_math(p2c)
        self.play(TransformMatchingTex(p2b.copy(),p2c),run_time=1.5)
        self.wait(1.2)

        p2d=self.M(
            r"\boxed{v(\tau)=v_{\max}e^{-C\tau/m}}",
            color=WHITE
        ).scale(1.05).move_to(DOWN*2.0)
        self.color_math(p2d)
        self.play(Write(p2d),run_time=1.5)
        self.wait(2.2)
        self.wipe()

        # ==========================================================
        # 15. HALF-SPEED TIME
        # ==========================================================
        title=self.title("15. Turun sampai setengah v_max", PURPLE)
        self.play(Write(title),run_time=1.3)

        half=[
            self.M(r"\frac12v_{\max}=v_{\max}e^{-Ct_2/m}",color=WHITE),
            self.M(r"\frac12=e^{-Ct_2/m}",color=WHITE),
            self.M(r"\ln\left(\frac12\right)=-\frac{Ct_2}{m}",color=WHITE),
            self.M(r"-\ln2=-\frac{Ct_2}{m}",color=WHITE),
            self.M(r"t_2=\frac mC\ln2",color=WHITE),
            self.M(r"\boxed{t_2\approx0.866\,\mathrm s}",color=PURPLE),
        ]
        ypos=[2.0,1.2,0.4,-0.4,-1.2,-2.0]
        for q,y in zip(half,ypos):
            self.color_math(q)
            q.scale(0.82).move_to(UP*y)
            self.play(Write(q),run_time=1.45)
            self.wait(0.9)
        self.wait(2.0)
        self.wipe()

        # ==========================================================
        # 16. FULL MOTION
        # ==========================================================
        title=self.title("16. Seluruh gerak dalam satu gambar", WHITE)
        self.play(Write(title),run_time=1.3)

        axes=Axes(
            x_range=[0,6.6,1],y_range=[0,5.5,1],
            x_length=9.1,y_length=4.8,tips=False,
            axis_config={"include_numbers":True,"font_size":21,"color":WHITE}
        ).shift(LEFT*1.55+DOWN*0.4)

        ph1=axes.plot(lambda t:vinf*(1-np.exp(-k*t)),x_range=[0,t1],color=BLUE,stroke_width=5)
        ph2=axes.plot(lambda t:vmax*np.exp(-k*(t-t1)),x_range=[t1,total],color=PURPLE,stroke_width=5)
        switch=DashedLine(axes.c2p(t1,0),axes.c2p(t1,vmax),color=YELLOW,stroke_width=3)
        end=DashedLine(axes.c2p(total,0),axes.c2p(total,vmax/2),color=GREEN,stroke_width=3)

        self.play(Create(axes),run_time=1.4)
        self.play(Create(ph1),run_time=2.0)
        self.play(Create(switch),run_time=1.0)
        self.wait(1.0)
        self.play(Create(ph2),run_time=1.8)
        self.play(Create(end),run_time=1.0)

        labels=VGroup(
            self.M(r"t_1\approx5.02\,s",color=YELLOW),
            self.M(r"t_2\approx0.866\,s",color=PURPLE),
            self.M(r"T=t_1+t_2\approx5.89\,s",color=GREEN),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.42).scale(0.78)
        labels.move_to(RIGHT*5.0+DOWN*0.25)
        for q in labels:
            self.play(Write(q),run_time=1.3)
            self.wait(0.7)

        self.wait(3.0)
