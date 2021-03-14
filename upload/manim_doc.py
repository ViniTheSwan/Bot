from manim import *

#to run a new scene

#command line
#manim first_animation.py SquareToCircle -p -ql
#SquareToCircle is the Scene
#-p means play Video right away
#-ql means quality low

#create new scene every Scene inherits form Scene
class NewScene(Scene):
    def construct(self):
        ## graphical Objects
        circle = Circle(color =RED)
        square =  Square(color= BLUE)
        triangle =  Triangle(color = PINK)
        a = Axes(
            x_min=-3,
            x_max=3,
            x_axis_width=15,
            x_tick_frequency=1,
            x_leftmost_tick=None,
            x_axis_label=None,

            y_min=-3,
            y_max=3,
            y_axis_height=15,
            y_tick_frequency=1,
            y_bottom_tick=None,
            y_labeled_nums=None,
            y_axis_label=None,

            axes_color=WHITE,
            graph_origin=1 * DOWN + 1 * LEFT,
            exclude_zero_label=True,
            num_graph_anchor_points=25,
            default_graph_colors=[BLUE, GREEN, YELLOW],
            default_derivative_color=GREEN,
            default_input_color=YELLOW,
            default_riemann_start_color=BLUE,
            default_riemann_end_color=GREEN,
            function_color=WHITE,
            area_opacity=0.8,
            num_rects=50,
            include_tip=True,
            axis_config={"include_tip": False},
            x_axis_config={"x_min": -40},
            y_axis_config={}
        )
        n = NumberLine()
        f = FunctionGraph(lambda x:x**2, x_min = 3,x_max = 3,color = BLUE)
        f = ParametricFunction(self.func, t_min = - 3, t_max = 3, color=BLUE)

        # graphical actions

        #Grouping
        VGroup(circle, triangle,square) # groups multiple objects, color shifting rotation is applied to all elements
        Group()    # groups for objects not base on bezier curves

        #Effects
        Write()
        ShowCreation()
        FadeIn()
        FadeOut()

        ## Latex equations Objects
        eq1 = TextMobject(r"$\frac{dJ}{d\theta} = \textbf{W}\vec{x} $")

        #object transformation
        eq1.shift(UP)
        eq1.shift()

        #Scene methods
        self.play()
        self.add()
