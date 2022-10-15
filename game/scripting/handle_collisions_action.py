from itertools import cycle
import constants
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point

class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.
    
    The responsibility of HandleCollisionsAction is to handle the situation when the cycle collides
    with the other Cycle segments collides, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False

    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        cycle_1 = cast.get_first_actor("Cycle_1")
        cycle_2 = cast.get_first_actor("Cycle_2")
        if not self._is_game_over:

            self._handle_segment_collision(cast)
            cycle_1.grow_tail(1)
            cycle_2.grow_tail(1)
            self._handle_game_over(cast)

    def _handle_segment_collision(self, cast):
        """Sets the game over flag if the cycle collides with another cycles segments.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        cycle_1 = cast.get_first_actor("Cycle_1")
        cycle_2 = cast.get_first_actor("Cycle_2")
        head_1 = cycle_1.get_segments()[0]
        head_2 = cycle_2.get_segments()[0]
        segments_1 = cycle_1.get_segments()[1:]
        segments_2 = cycle_2.get_segments()[1:]
        
        for segment in segments_2:
            if head_1.get_position().equals(segment.get_position()):
                self._winner = "Player 2"
                self._is_game_over = True
        
        for segment in segments_1:
            if head_2.get_position().equals(segment.get_position()):
                self._winner = "Player 1"
                self._is_game_over = True
        
    def _handle_game_over(self, cast):
        """Shows the 'game over' message and turns the Cycles white if the game is over.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:
            cycle_1 = cast.get_first_actor("Cycle_1")
            segments_1 = cycle_1.get_segments()
            cycle_2 = cast.get_first_actor("Cycle_2")
            segments_2 = cycle_2.get_segments()

            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 2)
            position = Point(x, y)

            message = Actor()
            message.set_text("Game Over! "+self._winner+" wins!")
            message.set_position(position)
            cast.add_actor("messages", message)

            for segment in segments_1:
                segment.set_color(constants.WHITE)
            for segment in segments_2:
                segment.set_color(constants.WHITE)