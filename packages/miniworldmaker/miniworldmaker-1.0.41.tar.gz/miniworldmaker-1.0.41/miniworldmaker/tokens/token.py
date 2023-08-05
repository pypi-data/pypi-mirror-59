import math
from typing import Union

import pygame
from miniworldmaker.app import app
from miniworldmaker.appearances import costume
from miniworldmaker.board_positions import board_position
from miniworldmaker.physics import physics as ph


class Meta(type):
    def __call__(cls, *args, **kwargs):
        try:
            instance = super().__call__(*args, **kwargs)
        except TypeError:
            raise
            #raise TypeError("Wrong number of arguments for {0}-constructor. See method-signature: {0}{1}".format(cls.__name__,inspect.signature(cls.__init__)))
        if hasattr(instance, "set_physics_default_values"):
            instance.set_physics_default_values()
        if hasattr(instance, "setup_physics"):
            instance.setup_physics()
            instance._start_physics()
        if hasattr(instance, "on_setup"):
            instance.on_setup()
        if hasattr(instance, "setup"):
            instance.setup()
        return instance


class Token(pygame.sprite.DirtySprite, metaclass = Meta):
    """
    Token is the basic class for all kinds of players,
    pieces and obstacles on the playing field

      * Acting: Create a method act(self). The method is called every frame
      * Setup: Create a method on_setup(self). The method is called when a new token is created (after __init__())
      * Physics: Create a method setup_physics(self). When this method is added, the object will be handled as
        physics-object.
      * Collsision-detection: Create a method on_sensing_<class_name>(self, other).
        The method is called everytime the token is colliding with a token of <class_name>.
        (Note: Write <class_name> in lower_case)

        Args:
            position (tuple): Position on the board where the token should be created.

        Attributes:
            collision_type (str): Defines the type of collision. Can be either "rect", "circle" or "mask"
        """
    token_count = 0
    class_image = None
    class_id = 0
    subclasses = None

    def __init__(self, position=None):
        pygame.sprite.DirtySprite.__init__(self)
        self.setup_completed = False
        self.board = app.App.board
        self.costume = None
        # private
        self._size = (0, 0)  # Tuple with size
        if position is not None:
            self._position: board_position.BoardPosition = position # Set in add_to_board
        else:
            self._position = (0, 0)
        self._direction = 0
        self.last_position = (0, 0)
        self.last_direction = 90
        self.init = 1 # Was init called ?
        self.board_connector = None
        Token.token_count += 1
        self.speed = 1
        # public
        self.physics = ph.PhysicsProperty()
        self.token_id = Token.token_count + 1
        self.is_static = False
        # costume
        self.costume_count = 0
        self.costume = costume.Costume(self)
        self._rect = self.image.get_rect()
        self.costumes = [self.costume]
        self.collision_type = "mask"
        self.costume.is_upscaled = True
        self.board = app.App.board
        self._orientation = 0
        self._initial_direction = 0
        self._dirty = 1
        self.costume.reload_image()
        self.board.add_to_board(self, self.position)

    @classmethod
    def from_center(cls, center_position):
        """
        Creates a token with center at center_position

        Args:
            center_position: Center of token
        """
        obj = cls(position = (0,0)) # temp positition
        obj.center = center_position # pos set to center
        return obj

    @property
    def orientation(self):
        """
        The orientation "corrects" a wrongly orientation of a token image.
        If orientation is != 0, the token is rotated by orientation degrees, before any other operation.

        Examples:

            Sets orientation:

            >>>  class Bird(Actor):
            >>>
            >>>    def on_setup(self):
            >>>      self.add_image("images/fly.png")
            >>>      self.orientation = 180
            >>>      self.flip_x() #flips actor

            Instead of using token.orientation, you can also use token.costume.orientation:

            >>>  def on_setup(self):
            >>>    self.add_image("images/fly.png")
            >>>    self.costume.orientation = 180
            >>>    self.flip_x() #flips actor

        """
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value
        if self.costume.orientation != self._orientation:
            self.costume.orientation = self._orientation

    @classmethod
    def all_subclasses(cls):
        """
        Gets all subclasses from Token-Class
        """
        def rec_all_subs(cls) -> set:
            if cls.subclasses is None:
                return set(cls.__subclasses__()).union(
                    [s for c in cls.__subclasses__() for s in rec_all_subs(c)])
            else:
                return cls.subclasses
        return rec_all_subs(cls)

    @property
    def is_flipped(self):
        """
        If a token is flipped, it is mirrored via the y-axis.

        Returns:
            True, if token is flipped

        Examples:

            flip a token in Example flipthefish.py

            >>>  def on_sensing_not_on_board(self):
            >>>    self.move_back()
            >>>    self.flip_x()
        """
        return self._is_flipped

    @is_flipped.setter
    def is_flipped(self, value):
        self.costume._is_flipped = value
        if self.is_flipped is True:
            self.costume.is_flipped = True
        else:
            self.costume.is_flipped = False

    def __str__(self):
        if self.board:
            return "{0}-Object, ID: {1} at pos {2}".format(self.class_name, self.token_id, self.position)
        else:
            return "**: {0}; ID: {1}".format(self.class_name, self.token_id)

    @property
    def image(self) -> pygame.Surface:
        """
        The image of the token:

        Warning: You should not draw on the image or similar,
        as the image will be reloaded during animations or other
        operations and changes will not be applied.

        Returns:
            The image of the token

        """
        return self.costume.image

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value
        if hasattr(self, "board") and self.board:
            self.board.dirty = 1

    def set_dirty(self):
        self.dirty = 1

    @property
    def rect(self) -> pygame.Rect:
        """
        The surrounding Rectangle as pygame.Rect.
        Warning: If the token is rotated, the rect vertices are not the vertices of the token image.

        Returns:
            The rectangle describing the image

        """
        if self.dirty == 1:
            self._rect = self.board_connector.get_token_rect()
            return self._rect
        else:
            return self._rect

    def add_image(self, path: str) -> int:
        """
        Adds an image to the token.
        Best Practice: Image should me placed in ./images subfolder of your project, because these images
        will be loaded before running the main-loop.

        Loading images is very slow, so this shouldn't be done in runtime.

        Args:
            path: Path to the images.

        Returns:
            The image index

        Examples:

            Create several tokens with images (in example createrobotworld.py)

            >>>  class Robot(Actor):
            >>>
            >>>    def on_setup(self):
            >>>      self.add_image("images/robo_green.png")
            >>>
            >>>
            >>>  class Wall(Token):
            >>>    def on_setup(self):
            >>>      self.add_image("images/rock.png")
            >>>
            >>>
            >>>  class Gold(Token):
            >>>    def on_setup(self):
            >>>      self.add_image("images/stone_gold.png")


        """
        image = self.costume.add_image(path)
        if not self.__class__.class_image:
            self.__class__.class_image = path
        return image

    def add_costume(self, path: str) -> costume.Costume:
        """
        Adds a new costume to token.
        The costume can be switched with self.switch_costume(index)

        Args:
            path: Path to the first image of new costume

        Returns:
            The new costume.

        """
        new_costume = costume.Costume(self)
        new_costume.add_image(path)
        self.costumes.append(new_costume)
        return new_costume

    def switch_costume(self, index=-1) -> costume.Costume:
        """Switches the costume of token

        Args:
            index: The index of the new costume. If index=-1, the next costume will be selected

        Returns: The new costume

        """
        if index == -1:
            index = self.costumes.index(self.costume)
            if index < len(self.costumes) - 1:
                index += 1
            else:
                index = 0
        else:
            index = index
        self.costume = self.costumes[index]
        self.costume.reset()
        self.costume.dirty = 1
        self.costume.call_all_actions()
        self.dirty = 1
        return self.costume

    @property
    def direction(self) -> int:
        """ Sets direction the token is oriented

            0°:  East, x degrees clock-wise otherwise
            You can also set the direction by String ("forward", "up", "down", ...

            .. image:: ../_images/movement.jpg

        Examples:

            Moving in rpg-basic-example.py:

            >>> def on_key_down(self, keys):
            >>>    if "W" in keys:
            >>>      self.point_in_direction("up")
            >>>    elif "S" in keys:
            >>>      self.point_in_direction("down")
            >>>    elif "A" in keys:
            >>>      self.point_in_direction("left")
            >>>    elif "D" in keys:
            >>>      self.point_in_direction("right")
            >>>    self.move()


        """
        return (self._direction + 180) % 360 - 180

    @direction.setter
    def direction(self, value):
        self.last_direction = self.direction
        direction = self._value_to_direction(value)
        self._direction = direction
        if self.last_direction != self._direction:
            self.dirty = 1
            if self.costume:
                self.costume.call_action("rotate")
            if self.board:
                self.board.window.send_event_to_containers("token_changed_direction", self)

    @property
    def direction_at_unit_circle(self):
        """
        Gets the direction as value in unit circle (0° right, 90° top, 180° left...
        """
        return Token.dir_to_unit_circle(self._direction)

    @direction_at_unit_circle.setter
    def direction_at_unit_circle(self, value):
        """
        Sets the direction from unit circle
        Args:
            value: An angle in the unit circle, e.g. 0°: right, 90° top, ...
        """
        self.direction = Token.unit_circle_to_dir(value)

    @staticmethod
    def dir_to_unit_circle(direction):
        """
        Transforms the current direction into standard-unit-circle direction

        Args:
            value: The direction in scratch-style

        Returns:

        """
        return -(direction + 90) % 360 - 180

    @staticmethod
    def unit_circle_to_dir(direction):
        """
        Transforms the current direction from standard-unit-circle direction
        into scratch-style coordinates

        Args:
            value: The direction in math unit circle style.

        Returns:

        """
        return - (direction + 90) % 360 - 180

    def turn_left(self, degrees: int = 90) -> int:
        """Turns actor by *degrees* degrees left

        Args:
            degrees: degrees in left direction

        Returns:
            New direction

        """
        self.direction = self.direction - degrees
        return self.direction

    def turn_right(self, degrees: int = 90):
        """Turns token by *degrees* degrees right

        Args:
            degrees: degrees in left direction

        Returns:
            New direction

        """
        self.direction = self.direction + degrees
        return self.direction

    def point_in_direction(self, direction) -> int:
        """
        Token points in given direction

        Args:
            direction: Direction the actor should point to

        Returns:
            The new direction as integer

        """
        self.direction = self._value_to_direction(direction)
        return self.direction

    def delta_x(self, distance):
        return math.sin(math.radians(self.direction)) * distance

    def delta_y(self, distance):
        return - math.cos(math.radians(self.direction)) * distance

    def point_towards_position(self, destination) -> int:
        """
        Token points towards a given position

        Args:
            destination: The position to which the actor should pointing

        Returns:
            The new direction

        Examples:

            Point towards mouse_position:

            >>>  def act(self):
            >>>  mouse = self.board.get_mouse_position()
            >>>  if mouse:
            >>>    self.point_towards_position(mouse)
            >>>  self.move()
        """
        return self.board_connector.point_towards_position(destination)

    def point_towards_token(self, other) -> int:
        """
        Token points towards another token.

        Args:
            other: The other token

        Returns:
            The new direction

        """
        pos = other.rect.center
        return self.point_towards_position(pos)

    @property
    def size(self) -> tuple:
        """Size of the token

        """
        return self._size

    @size.setter
    def size(self, value: tuple):
        if self.board_connector:
            self.board_connector.set_size(value)
        else:
            self._size = value
        if self.physics:
            self.physics.reload_physics()
        self.costume.call_action("scale")

    @property
    def width(self):
        """
        The width of the token in pixels
        """
        return self.size[0]

    @property
    def height(self):
        """
        The height of the token in pixels
        """
        return self.size[1]

    @property
    def position(self) -> board_position.BoardPosition:
        """
        The position of the token as tuple (x, y)
        """
        return self._position

    @position.setter
    def position(self, value: Union[board_position.BoardPosition, tuple]):
        self.last_position = self.position
        self.last_direction = self.direction
        if type(value) == tuple:
            value = board_position.BoardPosition(value[0], value[1])
        self._position = value
        if self.last_position != self.position:
            self.dirty = 1
            if self.board:
                self.board.window.send_event_to_containers("token_moved", self)

    @property
    def x(self):
        """int: The x-value of an token
        """
        return self._position[0]

    @x.setter
    def x(self, value):
        self.position = (value, self.y)

    @property
    def y(self):
        """int: The x-value of an token
        """
        return self._position[1]

    @y.setter
    def y(self, value):
        self.position = (self.x, value)

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    @property
    def center_x(self):
        """x-value of token center-position"""
        return self.rect.centerx

    @property
    def topleft_x(self):
        """x-value of token topleft-position"""
        return self.rect.topleft[0]

    @property
    def topleft_y(self):
        """x-value of token topleft-position"""
        return self.rect.topleft[1]

    @property
    def topleft(self) -> board_position.BoardPosition:
        return board_position.BoardPosition(self.rect.topleft[0], self.rect.topleft[1])

    @topleft.setter
    def topleft(self, value):
        self.last_position = self.position
        shift = self.width / 2 , self.height / 2
        self.position = value[0] + shift[0], value[1] + shift[1]

    @property
    def center_y(self):
        """y-value of token center-position"""
        return self.rect.centery

    @property
    def center(self) -> board_position.BoardPosition:
        return board_position.BoardPosition(self.center_x, self.center_y)

    @center_x.setter
    def center_x(self, value):
        self.last_position = self.position
        rect = pygame.Rect.copy(self.rect)
        rect.centerx = value
        self.x = rect.topleft[0]

    @center_y.setter
    def center_y(self, value):
        self.last_position = self.position
        rect = pygame.Rect.copy(self.rect)
        rect.centery = value
        self.y = rect.topleft[1]

    @center.setter
    def center(self, value):
        self.last_position = self.position
        rect = pygame.Rect.copy(self.rect)
        rect.centerx = value[0]
        rect.centery = value[1]
        self.position = rect.center

    def move(self, distance: int = 0):
        """Moves actor *distance* steps.

        Args:
            distance: Number of steps to move.
            If distance = 0, the actor speed will be used.

        Returns:
            The actor

        Examples:

            >>> class Robot(Token):
            >>>    def act(self):
            >>>         if self.sensing_on_board():
            >>>             self.move()
        """
        if distance == 0:
            distance = self.speed
        destination = self.board_connector.get_destination(self.position, self.direction, distance)
        self.position = board_position.BoardPosition.from_tuple(destination)
        return self

    def move_back(self):
        """
        Moves the actor to the last position (before the last movement")
        The last position will always be safed, when a move is executed, so move_back can undo every move.

        Examples:

            move_back as blocking-mechanism (in rpg-basic-template.py):

            >>>  def on_sensing_wall(self, wall):
            >>>    self.move_back()

        """
        self.position = self.last_position
        self.direction = self.last_direction

    def _value_to_direction(self, value) -> int:
        """
        Transforms a string value ("top", "left", "right", "bottom)
        into a position

        Args:
            value: The String value ("top", "left", "right", or "bottom)

        Returns:
            The position as scratch-style deegrees

        """
        if value == "top" or value == "up":
            value = 0
        if value == "left":
            value = 270
        if value == "right":
            value = 90
        if value == "down":
            value = 180
        if value == "forward":
            value = self.direction
        if value == "back":
            value = 360 - self.direction
        value = value % 360
        return value

    def move_in_direction(self, direction: Union[int, str]):
        """Moves token *distance* steps into a *direction*.

        .. image:: ../_images/movement.jpg

        Args:
            direction: Direction as angle

        Returns:
            The token itself

        """
        direction = self._value_to_direction(direction)
        self.direction = direction
        self.move()
        return self

    def move_to(self, position: board_position.BoardPosition):
        """Moves token *distance* steps to a specific board_position

        Args:
            position: The position to which the actor should move

        Returns:
            The token itself

        """
        self.position = position
        return self

    def remove(self):
        """
        Removes this token from board

        Examples:

            Removes robots in thecrash.py :

            >>>    def act(self):
            >>>        self.move()
            >>>        other = self.sensing_token(distance = 0, token_type=Robot)
            >>>    if other:
            >>>        explosion = Explosion(position=self.position)
            >>>        self.remove()
            >>>        other.remove()
        """
        if self.physics:
            self.physics.remove()
            self.physics = None
        if hasattr(self,  "board") and self.board:
            self.board_connector.remove_from_board()
        for event_handler in app.App.board.registered_event_handlers_for_tokens[self.__class__].keys():
            app.App.board.tokens_with_eventhandler[event_handler].remove(self)
        self.kill()
        del (self)

    def _start_physics(self):
        """
        Starts the physics engine.

        """
        self.physics.token = self
        self.physics.setup_physics_model()
        self.physics.start_physics()

    def flip_x(self) -> int:
        """Flips the actor by 180° degrees

        Examples:

            flip a token in Example flipthefish.py

            >>>  def on_sensing_not_on_board(self):
            >>>    self.move_back()
            >>>    self.flip_x()
        """
        if not self.costume.is_flipped:
            self.costume.is_flipped = True
        else:
            self.costume.is_flipped = False
        self.turn_left(180)
        return self.direction

    def bounce_from_border(self, borders):
        """ Bounces the actor from a border.

        Args:
            borders: A list of borders as strings e.g. ["left", "right"]

        Returns: The actor

        """
        angle = self.direction
        if ("top" in borders and (
                (self.direction <= 0 and self.direction > -90 or self.direction <= 90 and self.direction >= 0))):
            self.point_in_direction(0)
            incidence = self.direction - angle
            self.turn_left(180 - incidence)
        elif ("bottom" in borders and (
                (self.direction < -90 and self.direction >= -180) or (self.direction > 90 and self.direction <= 180))):
            self.point_in_direction(180)
            incidence = self.direction - angle
            self.turn_left(180 - incidence)
        elif ("left" in borders and self.direction <= 0):
            self.point_in_direction(-90)
            incidence = self.direction - angle
            self.turn_left(180 - incidence)
        elif ("right" in borders and (self.direction >= 0)):
            self.point_in_direction(90)
            incidence = self.direction - angle
            self.turn_left(180 - incidence)
        else:
            pass
        return self

    def sensing_on_board(self, distance: int = 0) -> bool:
        """
        Senses if token is on board

        Args:
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns: True if token is on board

        """
        return self.board_connector.sensing_on_board(distance=distance)

    def sensing_tokens(self, token_type=None, distance: int = 0):
        """
        Senses if tokens are on tokens position
        Args:
            token_type: filter by token type. Enter a class_name of tokens to look for here
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns: All tokens found by Sensor

        """
        return self.board_connector.sensing_tokens(token_type, distance)

    def sensing_token(self, token_type=None, distance: int = 0):
        """
        Senses if tokens are on tokens position.
        Args:
            token_type: filter by token type. Enter a class_name of tokens to look for here
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns: First token found by Sensor

        Examples:
            Sensing a fireplace in rpg-basic-template.py:

            >>>  fireplace =  self.player.sensing_token(Fireplace)
            >>>    if fireplace:
            >>>      self.console.newline("Du zündest die Feuerstelle an.")
            >>>      self.fireplace.burn()

        """
        return self.board_connector.sensing_token(token_type, distance)

    def sensing_borders(self, distance: int = 0):
        """
        Senses borders
        Args:
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns: True if border was found.

        """
        return self.board_connector.sensing_borders(distance)

    def sensing_colors(self, colors, distance):
        """
        Senses colors in board-background at token-position

        Args:
            colors:
            distance: Specifies the distance in front of the actuator to which the sensor reacts.

        Returns: All tokens found by Sensor

        """
        colors = self.board_connector.sensing_colors(colors, distance)
        return colors
