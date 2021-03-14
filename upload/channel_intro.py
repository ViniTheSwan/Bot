import sys
from neural_network import NeuralNetwork
from grant_network import NetworkMobject
from manimlib import *

class myNetworkMobject(NetworkMobject):
    CONFIG = {
        "edge_propogation_color": BLUE,
        "edge_propogation_time": 0.6,
    }

class Intro(Scene):
    def construct(self):
        n1 = myNetworkMobject(NeuralNetwork((10,10,10)),)

        self.play(FadeIn(n1))
        self.play(*n1.get_edge_propogation_animations(0))
        self.play(*n1.get_edge_propogation_animations(1))
        self.wait()

        self.play(ScaleInPlace(n1, 0.5))

class Landscape(ThreeDScene):
    def construct(self):
        pass
class GraphScene(FunctionGraph):
    def construct(self):
        pass


class BitcoinGraph(Scene):
    def construct(self):
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
            include_tip = True,
        )
        f = a.get_graph(self.func)
        self.add(a)
        self.play(Write(f))
        #self.play(FadeIn(a))
        #a.get_graph(self.func)
    def func(self, x):
        return x**2