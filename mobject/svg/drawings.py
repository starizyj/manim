from __future__ import absolute_import

from constants import *

from mobject.mobject import Mobject
from mobject.svg.svg_mobject import SVGMobject
from mobject.svg.brace import Brace
from mobject.svg.tex_mobject import TexMobject
from mobject.svg.tex_mobject import TextMobject
from mobject.types.vectorized_mobject import VGroup
from mobject.types.vectorized_mobject import VMobject
from mobject.types.vectorized_mobject import VectorizedPoint

from animation.animation import Animation
from animation.composition import AnimationGroup
from animation.composition import LaggedStart
from animation.rotation import Rotating
from animation.transform import ApplyMethod
from animation.creation import FadeIn
from animation.creation import GrowFromCenter

from mobject.geometry import Arc
from mobject.geometry import Circle
from mobject.geometry import Line
from mobject.geometry import Polygon
from mobject.geometry import Rectangle
from mobject.geometry import Square
from mobject.shape_matchers import SurroundingRectangle
from topics.three_dimensions import Cube
from utils.config_ops import digest_config
from utils.config_ops import digest_locals
from utils.space_ops import R3_to_complex
from utils.space_ops import angle_of_vector
from utils.space_ops import complex_to_R3
from utils.space_ops import rotate_vector

class Lightbulb(SVGMobject):
    CONFIG = {
        "file_name" : "lightbulb",
        "height" : 1,
        "stroke_color" : YELLOW,
        "stroke_width" : 3,
        "fill_color" : YELLOW,
        "fill_opacity" : 0,
    }

class BitcoinLogo(SVGMobject):
    CONFIG = {
        "file_name" : "Bitcoin_logo",
        "height" : 1,
        "fill_color" : "#f7931a",
        "inner_color" : WHITE,
        "fill_opacity" : 1,
        "stroke_width" : 0,
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self[0].set_fill(self.fill_color, self.fill_opacity)
        self[1].set_fill(self.inner_color, 1)

class Guitar(SVGMobject):
    CONFIG = {
        "file_name" : "guitar",
        "height" : 2.5,
        "fill_color" : DARK_GREY,
        "fill_opacity" : 1,
        "stroke_color" : WHITE,
        "stroke_width" : 0.5,
    }

class SunGlasses(SVGMobject):
    CONFIG = {
        "file_name" : "sunglasses",
        "glasses_width_to_eyes_width" : 1.1,
    }
    def __init__(self, pi_creature, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.set_stroke(WHITE, width = 0)
        self.set_fill(GREY, 1)
        self.scale_to_fit_width(
            self.glasses_width_to_eyes_width*pi_creature.eyes.get_width()
        )
        self.move_to(pi_creature.eyes, UP)

class Speedometer(VMobject):
    CONFIG = {
        "arc_angle" : 4*np.pi/3,
        "num_ticks" : 8,
        "tick_length" : 0.2,
        "needle_width" : 0.1,
        "needle_height" : 0.8,
        "needle_color" : YELLOW,
    }
    def generate_points(self):
        start_angle = np.pi/2 + self.arc_angle/2
        end_angle = np.pi/2 - self.arc_angle/2
        self.add(Arc(
            start_angle = start_angle,
            angle = -self.arc_angle
        ))
        tick_angle_range = np.linspace(start_angle, end_angle, self.num_ticks)
        for index, angle in enumerate(tick_angle_range):
            vect = rotate_vector(RIGHT, angle)
            tick = Line((1-self.tick_length)*vect, vect)
            label = TexMobject(str(10*index))
            label.scale_to_fit_height(self.tick_length)
            label.shift((1+self.tick_length)*vect)
            self.add(tick, label)

        needle = Polygon(
            LEFT, UP, RIGHT,
            stroke_width = 0,
            fill_opacity = 1,
            fill_color = self.needle_color
        )
        needle.stretch_to_fit_width(self.needle_width)
        needle.stretch_to_fit_height(self.needle_height)
        needle.rotate(start_angle - np.pi/2, about_point = ORIGIN)
        self.add(needle)
        self.needle = needle

        self.center_offset = self.get_center()

    def get_center(self):
        result = VMobject.get_center(self)
        if hasattr(self, "center_offset"):
            result -= self.center_offset
        return result

    def get_needle_tip(self):
        return self.needle.get_anchors()[1]

    def get_needle_angle(self):
        return angle_of_vector(
            self.get_needle_tip() - self.get_center()
        )

    def rotate_needle(self, angle):
        self.needle.rotate(angle, about_point = self.get_center())
        return self

    def move_needle_to_velocity(self, velocity):
        max_velocity = 10*(self.num_ticks-1)
        proportion = float(velocity) / max_velocity
        start_angle = np.pi/2 + self.arc_angle/2
        target_angle = start_angle - self.arc_angle * proportion
        self.rotate_needle(target_angle - self.get_needle_angle())
        return self

class AoPSLogo(SVGMobject):
    CONFIG = {
        "file_name" : "aops_logo",
        "height" : 1.5,
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.set_stroke(WHITE, width = 0)
        colors = [BLUE_E, "#008445", GREEN_B]
        index_lists = [
            (10, 11, 12, 13, 14, 21, 22, 23, 24, 27, 28, 29, 30),
            (0, 1, 2, 3, 4, 15, 16, 17, 26),
            (5, 6, 7, 8, 9, 18, 19, 20, 25)
        ]
        for color, index_list in zip(colors, index_lists):
            for i in index_list:
                self.submobjects[i].set_fill(color, opacity = 1)

        self.scale_to_fit_height(self.height)
        self.center()

class PartyHat(SVGMobject):
    CONFIG = {
        "file_name" : "party_hat",
        "height" : 1.5,
        "pi_creature" : None,
        "stroke_width" : 0,
        "fill_opacity" : 1,
        "propagate_style_to_family" : True,
        "frills_colors" : [MAROON_B, PURPLE],
        "cone_color" : GREEN,
        "dots_colors" : [YELLOW],
    }
    NUM_FRILLS = 7
    NUM_DOTS = 6
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.scale_to_fit_height(self.height)
        if self.pi_creature is not None:
            self.next_to(self.pi_creature.eyes, UP, buff = 0)

        self.frills = VGroup(*self[:self.NUM_FRILLS])
        self.cone = self[self.NUM_FRILLS]
        self.dots = VGroup(*self[self.NUM_FRILLS+1:])

        self.frills.set_color_by_gradient(*self.frills_colors)
        self.cone.set_color(self.cone_color)
        self.dots.set_color_by_gradient(*self.dots_colors)

class Laptop(VGroup):
    CONFIG = {
        "width" : 3,
        "body_dimensions" : [4, 3, 0.05],
        "screen_thickness" : 0.01,
        "keyboard_width_to_body_width" : 0.9,
        "keyboard_height_to_body_height" : 0.5,
        "screen_width_to_screen_plate_width" : 0.9,
        "key_color_kwargs" : {
            "stroke_width" : 0,
            "fill_color" : BLACK,
            "fill_opacity" : 1,
        },
        "body_color" : LIGHT_GREY,
        "shaded_body_color" : GREY,
        "open_angle" : np.pi/4,
    }
    def generate_points(self):
        body = Cube(side_length = 1)
        for dim, scale_factor in enumerate(self.body_dimensions):
            body.stretch(scale_factor, dim = dim)
        body.scale_to_fit_width(self.width)
        body.set_fill(self.shaded_body_color, opacity = 1)
        body.sort_submobjects(lambda p : p[2])
        body[-1].set_fill(self.body_color)
        keyboard = VGroup(*[
            VGroup(*[
                Square(**self.key_color_kwargs)
                for x in range(12-y%2)
            ]).arrange_submobjects(RIGHT, buff = SMALL_BUFF)
            for y in range(4)
        ]).arrange_submobjects(DOWN, buff = MED_SMALL_BUFF)
        keyboard.stretch_to_fit_width(
            self.keyboard_width_to_body_width*body.get_width(),
        )
        keyboard.stretch_to_fit_height(
            self.keyboard_height_to_body_height*body.get_height(),
        )
        keyboard.next_to(body, OUT, buff = 0.1*SMALL_BUFF)
        keyboard.shift(MED_SMALL_BUFF*UP)
        body.add(keyboard)

        screen_plate = body.copy()
        screen_plate.stretch(self.screen_thickness/self.body_dimensions[2], dim = 2)
        screen = Rectangle(
            stroke_width = 0,
            fill_color = BLACK,
            fill_opacity = 1,
        )
        screen.replace(screen_plate, stretch = True)
        screen.scale_in_place(self.screen_width_to_screen_plate_width)
        screen.next_to(screen_plate, OUT, buff = 0.1*SMALL_BUFF)
        screen_plate.add(screen)
        screen_plate.next_to(body, UP, buff = 0)
        screen_plate.rotate(
            self.open_angle, RIGHT, 
            about_point = screen_plate.get_bottom()
        )
        self.screen_plate = screen_plate
        self.screen = screen

        axis = Line(
            body.get_corner(UP+LEFT+OUT),
            body.get_corner(UP+RIGHT+OUT),
            color = BLACK,
            stroke_width = 2
        )
        self.axis = axis

        self.add(body, screen_plate, axis)
        self.rotate(5*np.pi/12, LEFT, about_point = ORIGIN)
        self.rotate(np.pi/6, DOWN, about_point = ORIGIN)

class PatreonLogo(SVGMobject):
    CONFIG = {
        "file_name" : "patreon_logo",
        "fill_color" : "#F96854",
        # "fill_color" : WHITE,
        "fill_opacity" : 1,
        "stroke_width" : 0,
        "width" : 4,
        "propagate_style_to_family" : True
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.scale_to_fit_width(self.width)
        self.center()

class VideoIcon(SVGMobject):
    CONFIG = {
        "file_name" : "video_icon",
        "width" : FRAME_WIDTH/12.,
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.center()
        self.scale_to_fit_width(self.width)
        self.set_stroke(color = WHITE, width = 0)
        self.set_fill(color = WHITE, opacity = 1)

class VideoSeries(VGroup):
    CONFIG = {
        "num_videos" : 11,
        "gradient_colors" : [BLUE_B, BLUE_D],
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        videos = [VideoIcon() for x in range(self.num_videos)]
        VGroup.__init__(self, *videos, **kwargs)
        self.arrange_submobjects()
        self.scale_to_fit_width(FRAME_WIDTH-MED_LARGE_BUFF)
        self.set_color_by_gradient(*self.gradient_colors)

class Headphones(SVGMobject):
    CONFIG = {
        "file_name" : "headphones",
        "height" : 2,
        "y_stretch_factor" : 0.5,
        "color" : GREY,
    }
    def __init__(self, pi_creature = None, **kwargs):
        digest_config(self, kwargs)
        SVGMobject.__init__(self, file_name = self.file_name, **kwargs)
        self.stretch(self.y_stretch_factor, 1)        
        self.scale_to_fit_height(self.height)
        self.set_stroke(width = 0)
        self.set_fill(color = self.color)
        if pi_creature is not None:
            eyes = pi_creature.eyes
            self.scale_to_fit_height(3*eyes.get_height())
            self.move_to(eyes, DOWN)
            self.shift(DOWN*eyes.get_height()/4)

class Clock(VGroup):
    CONFIG = {
        "propagate_style_to_family" : True,
    }
    def __init__(self, **kwargs):
        circle = Circle()
        ticks = []
        for x in range(12):
            alpha = x/12.
            point = complex_to_R3(
                np.exp(2*np.pi*alpha*complex(0, 1))
            )
            length = 0.2 if x%3 == 0 else 0.1
            ticks.append(
                Line(point, (1-length)*point)
            )
        self.hour_hand = Line(ORIGIN, 0.3*UP)
        self.minute_hand = Line(ORIGIN, 0.6*UP)
        # for hand in self.hour_hand, self.minute_hand:
        #     #Balance out where the center is
        #     hand.add(VectorizedPoint(-hand.get_end()))

        VGroup.__init__(
            self, circle, 
            self.hour_hand, self.minute_hand,
            *ticks
        )

class ClockPassesTime(Animation):
    CONFIG = {
        "run_time" : 5, 
        "hours_passed" : 12,
        "rate_func" : None,
    }
    def __init__(self, clock, **kwargs):
        digest_config(self, kwargs)
        assert(isinstance(clock, Clock))
        rot_kwargs = {
            "axis" : OUT,
            "about_point" : clock.get_center()
        }
        hour_radians = -self.hours_passed*2*np.pi/12
        self.hour_rotation = Rotating(
            clock.hour_hand, 
            radians = hour_radians,
            **rot_kwargs
        )
        self.minute_rotation = Rotating(
            clock.minute_hand, 
            radians = 12*hour_radians,
            **rot_kwargs
        )
        Animation.__init__(self, clock, **kwargs)

    def update_mobject(self, alpha):
        for rotation in self.hour_rotation, self.minute_rotation:
            rotation.update_mobject(alpha)

class Bubble(SVGMobject):
    CONFIG = {
        "direction" : LEFT,
        "center_point" : ORIGIN,
        "content_scale_factor" : 0.75,
        "height" : 5,
        "width"  : 8,
        "bubble_center_adjustment_factor" : 1./8,
        "file_name" : None,
        "propagate_style_to_family" : True,
        "fill_color" : BLACK,
        "fill_opacity" : 0.8,
        "stroke_color" : WHITE,
        "stroke_width" : 3,
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs, locals())
        if self.file_name is None:
            raise Exception("Must invoke Bubble subclass")
        try:
            SVGMobject.__init__(self, **kwargs)
        except IOError as err:
            self.file_name = os.path.join(FILE_DIR, self.file_name)
            SVGMobject.__init__(self, **kwargs)
        self.center()
        self.stretch_to_fit_height(self.height)
        self.stretch_to_fit_width(self.width)
        if self.direction[0] > 0:
            Mobject.flip(self)
        self.direction_was_specified = ("direction" in kwargs)
        self.content = Mobject()

    def get_tip(self):
        #TODO, find a better way
        return self.get_corner(DOWN+self.direction)-0.6*self.direction

    def get_bubble_center(self):
        factor = self.bubble_center_adjustment_factor
        return self.get_center() + factor*self.get_height()*UP

    def move_tip_to(self, point):
        VGroup(self, self.content).shift(point - self.get_tip())
        return self

    def flip(self):
        Mobject.flip(self)        
        self.direction = -np.array(self.direction)
        return self

    def pin_to(self, mobject):
        mob_center = mobject.get_center()
        want_to_filp = np.sign(mob_center[0]) != np.sign(self.direction[0])
        can_flip = not self.direction_was_specified
        if want_to_filp and can_flip:
            self.flip()
        boundary_point = mobject.get_critical_point(UP-self.direction)
        vector_from_center = 1.0*(boundary_point-mob_center)
        self.move_tip_to(mob_center+vector_from_center)
        return self

    def position_mobject_inside(self, mobject):
        scaled_width = self.content_scale_factor*self.get_width()
        if mobject.get_width() > scaled_width:
            mobject.scale_to_fit_width(scaled_width)
        mobject.shift(
            self.get_bubble_center() - mobject.get_center()
        )
        return mobject

    def add_content(self, mobject):
        self.position_mobject_inside(mobject)
        self.content = mobject
        return self.content

    def write(self, *text):
        self.add_content(TextMobject(*text))
        return self

    def resize_to_content(self):
        target_width = self.content.get_width()
        target_width += max(MED_LARGE_BUFF, 2)
        target_height = self.content.get_height()
        target_height += 2.5*LARGE_BUFF
        tip_point = self.get_tip()
        self.stretch_to_fit_width(target_width)
        self.stretch_to_fit_height(target_height)
        self.move_tip_to(tip_point)
        self.position_mobject_inside(self.content)

    def clear(self):
        self.add_content(VMobject())
        return self

class SpeechBubble(Bubble):
    CONFIG = {
        "file_name" : "Bubbles_speech.svg",
        "height" : 4
    }

class DoubleSpeechBubble(Bubble):
    CONFIG = {
        "file_name" : "Bubbles_double_speech.svg",
        "height" : 4
    }

class ThoughtBubble(Bubble):
    CONFIG = {
        "file_name" : "Bubbles_thought.svg",
    }

    def __init__(self, **kwargs):
        Bubble.__init__(self, **kwargs)
        self.submobjects.sort(
            lambda m1, m2 : int((m1.get_bottom()-m2.get_bottom())[1])
        )

    def make_green_screen(self):
        self.submobjects[-1].set_fill(GREEN_SCREEN, opacity = 1)
        return self

class Car(SVGMobject):
    CONFIG = {
        "file_name" : "Car", 
        "height" : 1,
        "color" : LIGHT_GREY,
        "light_colors" : [BLACK, BLACK],
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.scale_to_fit_height(self.height)
        self.set_stroke(color = WHITE, width = 0)
        self.set_fill(self.color, opacity = 1)

        from for_3b1b_videos.pi_creature import Randolph
        randy = Randolph(mode = "happy")
        randy.scale_to_fit_height(0.6*self.get_height())
        randy.stretch(0.8, 0)
        randy.look(RIGHT)
        randy.move_to(self)
        randy.shift(0.07*self.height*(RIGHT+UP))
        self.randy = self.pi_creature = randy
        self.add_to_back(randy)

        orientation_line = Line(self.get_left(), self.get_right())
        orientation_line.set_stroke(width = 0)
        self.add(orientation_line)
        self.orientation_line = orientation_line

        for light, color in zip(self.get_lights(), self.light_colors):
            light.set_fill(color, 1)
            light.is_subpath = False

        self.add_treds_to_tires()

    def move_to(self, point_or_mobject):
        vect = rotate_vector(
            UP+LEFT, self.orientation_line.get_angle()
        )
        self.next_to(point_or_mobject, vect, buff = 0)
        return self

    def get_front_line(self):
        return DashedLine(
            self.get_corner(UP+RIGHT), 
            self.get_corner(DOWN+RIGHT),
            color = DISTANCE_COLOR,
            dashed_segment_length = 0.05,
        )

    def add_treds_to_tires(self):
        for tire in self.get_tires():
            radius = tire.get_width()/2
            center = tire.get_center()
            tred = Line(
                0.9*radius*RIGHT, 1.4*radius*RIGHT,
                stroke_width = 2,
                color = BLACK
            )
            tred.rotate_in_place(np.pi/4)
            for theta in np.arange(0, 2*np.pi, np.pi/4):
                new_tred = tred.copy()
                new_tred.rotate(theta, about_point = ORIGIN)
                new_tred.shift(center)
                tire.add(new_tred)
        return self

    def get_tires(self):
        return VGroup(self[1][1], self[1][3])

    def get_lights(self):
        return VGroup(self.get_front_light(), self.get_rear_light())

    def get_front_light(self):
        return self[1][5]

    def get_rear_light(self):
        return self[1][8]


