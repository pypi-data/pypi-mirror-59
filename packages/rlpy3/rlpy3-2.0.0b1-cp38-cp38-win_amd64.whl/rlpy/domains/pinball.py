"""Pinball domain for reinforcement learning
"""
from .domain import Domain
import numpy as np
from itertools import tee
import itertools
from pathlib import Path

try:
    from tkinter import Tk, Canvas
except ImportError:
    import warnings

    warnings.warn("TkInter is not found for Pinball.")
from rlpy.tools import __rlpy_location__

__copyright__ = "Copyright 2013, RLPy http://acl.mit.edu/RLPy"
__credits__ = [
    "Alborz Geramifard",
    "Robert H. Klein",
    "Christoph Dann",
    "William Dabney",
    "Jonathan P. How",
]
__license__ = "BSD 3-Clause"
__author__ = [
    "Pierre-Luc Bacon",  # author of the original version
    "Austin Hays",
]  # adapted for RLPy and TKinter


class Pinball(Domain):

    """
    The goal of this domain is to maneuver a small ball on a plate into a hole.
    The plate may contain obstacles which should be avoided.

    **STATE:**
        The state is given by a 4-dimensional vector, consisting of position and
        velocity of the ball.

    **ACTIONS:**
        There are 5 actions, standing for slanting the  plat in x or y direction
        or a horizontal position
        of the plate.

    **REWARD:**
        Slanting the plate costs -4 reward in addition to -1 reward for each timestep.
        When the ball reaches the hole, the agent receives 10000 units of reward.

    **REFERENCE:**

    .. seealso::
        G.D. Konidaris and A.G. Barto:
        *Skill Discovery in Continuous Reinforcement Learning domains using Skill Chaining.*
        Advances in Neural Information Processing Systems 22, pages 1015-1023, December 2009.
    """

    #: default location of config files shipped with rlpy
    DEFAULT_CONFIG_DIR = Path(__rlpy_location__).joinpath("domains/PinballConfigs")

    @classmethod
    def default_cfg(cls, name="pinball_simple_single.json"):
        return cls.DEFAULT_CONFIG_DIR.joinpath(name)

    def __init__(
        self,
        noise=0.1,
        episode_cap=1000,
        config_file=DEFAULT_CONFIG_DIR.joinpath("pinball_simple_single.json"),
    ):
        """
        :param config_file: Location of the configuration file.
        :param episode_cap: Maximum length of an episode
        :param noise: With probability noise, a uniformly random action is executed
        """
        self.NOISE = noise
        self.screen = None
        self.actions = [
            PinballModel.ACC_X,
            PinballModel.DEC_Y,
            PinballModel.DEC_X,
            PinballModel.ACC_Y,
            PinballModel.ACC_NONE,
        ]
        super().__init__(
            actions_num=len(self.actions),
            statespace_limits=np.array(
                [[0.0, 1.0], [0.0, 1.0], [-2.0, 2.0], [-2.0, 2.0]]
            ),
            continuous_dims=[4],
            episode_cap=episode_cap,
        )
        self.environment = PinballModel(config_file, random_state=self.random_state)

    def show_domain(self, _a=None):
        if self.screen is None:
            master = Tk()
            master.title("RLPy Pinball")
            self.screen = Canvas(master, width=500.0, height=500.0)
            self.screen.configure(background="LightGray")
            self.screen.pack()
            self.environment_view = PinballView(
                self.screen, 500.0, 500.0, self.environment
            )
        self.environment_view.blit()
        self.screen.pack()
        self.screen.update()

    def step(self, a):
        s = self.state
        [
            self.environment.ball.position[0],
            self.environment.ball.position[1],
            self.environment.ball.xdot,
            self.environment.ball.ydot,
        ] = s
        if self.random_state.random_sample() < self.NOISE:
            # Random Move
            a = self.random_state.choice(self.possible_actions())
        reward = self.environment.take_action(a)
        self.environment._check_bounds()
        state = np.array(self.environment.get_state())
        self.state = state.copy()
        return reward, state, self.is_terminal(), self.possible_actions()

    def s0(self):
        (
            self.environment.ball.position[0],
            self.environment.ball.position[1],
        ) = self.environment.start_pos
        self.environment.ball.xdot, self.environment.ball.ydot = 0.0, 0.0
        self.state = np.array(
            [
                self.environment.ball.position[0],
                self.environment.ball.position[1],
                self.environment.ball.xdot,
                self.environment.ball.ydot,
            ]
        )
        return self.state, self.is_terminal(), self.possible_actions()

    def possible_actions(self, s=0):
        return np.array(self.actions)

    def is_terminal(self):
        return self.environment.episode_ended()


class BallModel:

    """ This class maintains the state of the ball
    in the pinball domain. It takes care of moving
    it according to the current velocity and drag coefficient.

    """

    DRAG = 0.995

    def __init__(self, start_position, radius):
        """
        :param start_position: The initial position
        :type start_position: float
        :param radius: The ball radius
        :type radius: float
        """
        self.position = start_position
        self.radius = radius
        self.xdot = 0.0
        self.ydot = 0.0

    def add_impulse(self, delta_xdot, delta_ydot):
        """ Change the momentum of the ball
        :param delta_xdot: The change in velocity in the x direction
        :type delta_xdot: float
        :param delta_ydot: The change in velocity in the y direction
        :type delta_ydot: float
        """
        self.xdot += delta_xdot / 5
        self.ydot += delta_ydot / 5
        self.xdot = self._clip(self.xdot)
        self.ydot = self._clip(self.ydot)

    def add_drag(self):
        """ Add a fixed amount of drag to the current velocity """
        self.xdot *= self.DRAG
        self.ydot *= self.DRAG

    def step(self):
        """ Move the ball by one increment """
        self.position[0] += self.xdot * self.radius / 20.0
        self.position[1] += self.ydot * self.radius / 20.0

    def _clip(self, val, low=-2, high=2):
        """ Clip a value in a given range """
        if val > high:
            val = high
        if val < low:
            val = low
        return val


class PinballObstacle:

    """ This class represents a single polygon obstacle in the
    pinball domain and detects when a :class:`BallModel` hits it.

    When a collision is detected, it also provides a way to
    compute the appropriate effect to apply on the ball.
    """

    def __init__(self, points):
        """
        :param points: A list of points defining the polygon
        :type points: list of lists
        """
        self.points = np.array(points)
        self.min_x = min(self.points, key=lambda pt: pt[0])[0]
        self.max_x = max(self.points, key=lambda pt: pt[0])[0]
        self.min_y = min(self.points, key=lambda pt: pt[1])[1]
        self.max_y = max(self.points, key=lambda pt: pt[1])[1]

        self._double_collision = False
        self._intercept = None

    def collision(self, ball):
        """ Determines if the ball hits this obstacle

    :param ball: An instance of :class:`BallModel`
    :type ball: :class:`BallModel`
        """
        self._double_collision = False

        if ball.position[0] - ball.radius > self.max_x:
            return False
        if ball.position[0] + ball.radius < self.min_x:
            return False
        if ball.position[1] - ball.radius > self.max_y:
            return False
        if ball.position[1] + ball.radius < self.min_y:
            return False

        a, b = tee(np.vstack([np.array(self.points), self.points[0]]))
        next(b, None)
        intercept_found = False
        for pt_pair in zip(a, b):
            if self._intercept_edge(pt_pair, ball):
                if intercept_found:
                    # Ball has hit a corner
                    self._intercept = self._select_edge(pt_pair, self._intercept, ball)
                    self._double_collision = True
                else:
                    self._intercept = pt_pair
                    intercept_found = True

        return intercept_found

    def collision_effect(self, ball):
        """ Based of the collision detection result triggered
    in :func:`PinballObstacle.collision`, compute the
        change in velocity.

    :param ball: An instance of :class:`BallModel`
    :type ball: :class:`BallModel`

        """
        if self._double_collision:
            return [-ball.xdot, -ball.ydot]

        # Normalize direction
        obstacle_vector = self._intercept[1] - self._intercept[0]
        if obstacle_vector[0] < 0:
            obstacle_vector = self._intercept[0] - self._intercept[1]

        velocity_vector = np.array([ball.xdot, ball.ydot])
        theta = self._angle(velocity_vector, obstacle_vector) - np.pi
        if theta < 0:
            theta += 2 * np.pi

        intercept_theta = self._angle([-1, 0], obstacle_vector)
        theta += intercept_theta

        if theta > 2 * np.pi:
            theta -= 2 * np.pi

        velocity = np.linalg.norm([ball.xdot, ball.ydot])

        return [velocity * np.cos(theta), velocity * np.sin(theta)]

    def _select_edge(self, intersect1, intersect2, ball):
        """ If the ball hits a corner, select one of two edges.

    :param intersect1: A pair of points defining an edge of the polygon
    :type intersect1: list of lists
    :param intersect2: A pair of points defining an edge of the polygon
    :type intersect2: list of lists
    :returns: The edge with the smallest angle with the velocity vector
    :rtype: list of lists

        """
        velocity = np.array([ball.xdot, ball.ydot])
        obstacle_vector1 = intersect1[1] - intersect1[0]
        obstacle_vector2 = intersect2[1] - intersect2[0]

        angle1 = self._angle(velocity, obstacle_vector1)
        if angle1 > np.pi:
            angle1 -= np.pi

        angle2 = self._angle(velocity, obstacle_vector2)
        if angle1 > np.pi:
            angle2 -= np.pi

        if np.abs(angle1 - np.pi / 2) < np.abs(angle2 - np.pi / 2):
            return intersect1
        return intersect2

    def _angle(self, v1, v2):
        """ Compute the angle difference between two vectors

    :param v1: The x,y coordinates of the vector
    :type: v1: list
    :param v2: The x,y coordinates of the vector
    :type: v2: list
    :rtype: float

    """
        angle_diff = np.arctan2(v1[0], v1[1]) - np.arctan2(v2[0], v2[1])
        if angle_diff < 0:
            angle_diff += 2 * np.pi
        return angle_diff

    def _intercept_edge(self, pt_pair, ball):
        """ Compute the projection on and edge and find out

    if it intercept with the ball.
    :param pt_pair: The pair of points defining an edge
    :type pt_pair: list of lists
    :param ball: An instance of :class:`BallModel`
    :type ball: :class:`BallModel`
    :returns: True if the ball has hit an edge of the polygon
    :rtype: bool

        """
        # Find the projection on an edge
        obstacle_edge = pt_pair[1] - pt_pair[0]
        difference = np.array(ball.position) - pt_pair[0]

        scalar_proj = difference.dot(obstacle_edge) / obstacle_edge.dot(obstacle_edge)
        if scalar_proj > 1.0:
            scalar_proj = 1.0
        elif scalar_proj < 0.0:
            scalar_proj = 0.0

        # Compute the distance to the closest point
        closest_pt = pt_pair[0] + obstacle_edge * scalar_proj
        obstacle_to_ball = ball.position - closest_pt
        distance = obstacle_to_ball.dot(obstacle_to_ball)

        if distance <= ball.radius * ball.radius:
            # A collision only if the ball is not already moving away
            velocity = np.array([ball.xdot, ball.ydot])
            ball_to_obstacle = closest_pt - ball.position

            angle = self._angle(ball_to_obstacle, velocity)
            if angle > np.pi:
                angle = 2 * np.pi - angle

            if angle > np.pi / 1.99:
                return False

            return True
        else:
            return False


class PinballModel:

    """ This class is a self-contained model of the pinball
    domain for reinforcement learning.

    It can be used either over RL-Glue through the :class:`PinballRLGlue`
    adapter or interactively with :class:`PinballView`.

    """

    ACC_X = 0
    ACC_Y = 1
    DEC_X = 2
    DEC_Y = 3
    ACC_NONE = 4

    STEP_PENALTY = -1
    THRUST_PENALTY = -5
    END_EPISODE = 10000

    def __init__(self, config_file, random_state):
        """ Read a configuration file for Pinball and draw the domain to screen
        """

        self.random_state = random_state
        self.action_effects = {
            self.ACC_X: (1, 0),
            self.ACC_Y: (0, 1),
            self.DEC_X: (-1, 0),
            self.DEC_Y: (0, -1),
            self.ACC_NONE: (0, 0),
        }
        import json

        # Set up the environment according to the configuration
        with config_file.open() as f:
            config = json.load(f)
        try:
            self.obstacles = list(map(PinballObstacle, config["obstacles"]))
            self.target_pos = config["target_pos"]
            self.target_rad = config["target_rad"]
            start_pos = config["start_pos"]
            ball_rad = config["ball_rad"]
        except KeyError as e:
            raise KeyError(f"Pinball config doesn't have a key: {e}")

        self.start_pos = start_pos[0]
        start_idx = self.random_state.randint(len(start_pos))
        self.ball = BallModel(list(start_pos[start_idx]), ball_rad)

    def get_state(self):
        """ Access the current 4-dimensional state vector

        :returns: a list containing the x position, y position, xdot, ydot
        :rtype: list

        """
        return [
            self.ball.position[0],
            self.ball.position[1],
            self.ball.xdot,
            self.ball.ydot,
        ]

    def take_action(self, action):
        """ Take a step in the environment

        :param action: The action to apply over the ball
        :type action: int

        """
        if isinstance(action, np.ndarray):
            action = action.item()
        for i in range(20):
            if i == 0:
                self.ball.add_impulse(*self.action_effects[action])

            self.ball.step()

            # Detect collisions
            ncollision = 0
            dxdy = np.array([0, 0])

            for obs in self.obstacles:
                if obs.collision(self.ball):
                    dxdy = dxdy + obs.collision_effect(self.ball)
                    ncollision += 1

            if ncollision == 1:
                self.ball.xdot = dxdy[0]
                self.ball.ydot = dxdy[1]
                if i == 19:
                    self.ball.step()
            elif ncollision > 1:
                self.ball.xdot = -self.ball.xdot
                self.ball.ydot = -self.ball.ydot

            if self.episode_ended():
                return self.END_EPISODE

        self.ball.add_drag()
        self._check_bounds()

        if action == self.ACC_NONE:
            return self.STEP_PENALTY

        return self.THRUST_PENALTY

    def episode_ended(self):
        """ Find out if the ball reached the target

        :returns: True if the ball reached the target position
        :rtype: bool

        """
        return (
            np.linalg.norm(np.array(self.ball.position) - np.array(self.target_pos))
            < self.target_rad
        )

    def _check_bounds(self):
        """ Make sure that the ball stays within the environment """
        if self.ball.position[0] > 1.0:
            self.ball.position[0] = 0.95
        if self.ball.position[0] < 0.0:
            self.ball.position[0] = 0.05
        if self.ball.position[1] > 1.0:
            self.ball.position[1] = 0.95
        if self.ball.position[1] < 0.0:
            self.ball.position[1] = 0.05


class PinballView:

    """ This class displays a :class:`PinballModel`

    This class is used in conjunction with the :func:`run_pinballview`
    function, acting as a *controller*.

    """

    def __init__(self, screen, width, height, model):
        """
           Changed from original PyGame implementation to work
           with Tkinter visualization.
        """
        self.screen = screen
        self.width = 500.0
        self.height = 500.0
        self.model = model

        self.x, self.y = self._to_pixels(self.model.ball.position)
        self.rad = int(self.model.ball.radius * self.width)

        self.DARK_GRAY = [64, 64, 64]
        self.DARK_BLUE = [0, 0, 128]
        self.LIGHT_GRAY = [232, 232, 232]
        self.BALL_COLOR = [0, 0, 255]
        self.TARGET_COLOR = [255, 0, 0]

        for obs in model.obstacles:
            coords_list = list(map(self._to_pixels, obs.points))
            chain = itertools.chain(*coords_list)
            coords = list(chain)
            self.screen.create_polygon(coords, fill="blue")
        self.screen.pack()

        self.target_x, self.target_y = self._to_pixels(self.model.target_pos)
        self.target_rad = int(self.model.target_rad * self.width)
        _ = self.drawcircle(
            self.screen, self.target_x, self.target_y, self.target_rad, "red"
        )
        self.ball_id = self.drawcircle(self.screen, self.x, self.y, self.rad, "black")
        self.screen.pack()

    def drawcircle(self, canv, x, y, rad, color):
        return canv.create_oval(x - rad, y - rad, x + rad, y + rad, width=0, fill=color)

    def _to_pixels(self, pt):
        """ Converts from real units in the 0-1 range to pixel units

        :param pt: a point in real units
        :type pt: list
        :returns: the input point in pixel units
        :rtype: list

        """
        return [int(pt[0] * self.width), int(pt[1] * self.height)]

    def blit(self):
        """ Blit the ball onto the background surface """
        self.screen.coords(
            self.ball_id,
            self.x - self.rad,
            self.y - self.rad,
            self.x + self.rad,
            self.y + self.rad,
        )
        self.x, self.y = self._to_pixels(self.model.ball.position)
        self.screen.pack()


def run_pinballview(width, height, configuration):
    """
    Changed from original Pierre-Luc Bacon implementation to reflect
    the visualization changes in the PinballView Class.
    """

    width, height = float(width), float(height)
    master = Tk()
    master.title("RLPy Pinball")
    screen = Canvas(master, width=500.0, height=500.0)
    screen.configure(background="LightGray")
    screen.pack()

    environment = PinballModel(configuration)
    environment_view = PinballView(screen, width, height, environment)

    actions = [
        PinballModel.ACC_X,
        PinballModel.DEC_Y,
        PinballModel.DEC_X,
        PinballModel.ACC_Y,
        PinballModel.ACC_NONE,
    ]
    done = False
    while not done:
        user_action = np.random.choice(actions)
        environment_view.blit()
        if environment.episode_ended():
            done = True
        if environment.take_action(user_action) == environment.END_EPISODE:
            done = True

        environment_view.blit()
        screen.update()
