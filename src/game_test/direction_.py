import unittest
from src.game.direction import Direction, Turn


class Direction_(unittest.TestCase):
    def test_is_aligned(self):
        self.assertTrue(Direction.up.is_aligned(Direction.up))
        self.assertTrue(Direction.up.is_aligned(Direction.down))
        self.assertTrue(Direction.right.is_aligned(Direction.right))
        self.assertTrue(Direction.right.is_aligned(Direction.left))
        self.assertTrue(Direction.down.is_aligned(Direction.down))
        self.assertTrue(Direction.down.is_aligned(Direction.up))
        self.assertTrue(Direction.left.is_aligned(Direction.left))
        self.assertTrue(Direction.left.is_aligned(Direction.right))

    def test_is_perpendicular(self):
        self.assertTrue(Direction.up.is_perpendicular(Direction.left))
        self.assertTrue(Direction.up.is_perpendicular(Direction.right))
        self.assertTrue(Direction.right.is_perpendicular(Direction.up))
        self.assertTrue(Direction.right.is_perpendicular(Direction.down))
        self.assertTrue(Direction.down.is_perpendicular(Direction.left))
        self.assertTrue(Direction.down.is_perpendicular(Direction.right))
        self.assertTrue(Direction.left.is_perpendicular(Direction.up))
        self.assertTrue(Direction.left.is_perpendicular(Direction.down))

    def test_turn_right(self):
        self.assertEqual(Direction.up.turn(Turn.right), Direction.right)
        self.assertEqual(Direction.right.turn(Turn.right), Direction.down)
        self.assertEqual(Direction.down.turn(Turn.right), Direction.left)
        self.assertEqual(Direction.left.turn(Turn.right), Direction.up)

    def test_turn_left(self):
        self.assertEqual(Direction.down.turn(Turn.left), Direction.right)
        self.assertEqual(Direction.left.turn(Turn.left), Direction.down)
        self.assertEqual(Direction.up.turn(Turn.left), Direction.left)
        self.assertEqual(Direction.right.turn(Turn.left), Direction.up)

    def test_turn_ahead(self):
        self.assertEqual(Direction.down.turn(Turn.ahead), Direction.down)
        self.assertEqual(Direction.left.turn(Turn.ahead), Direction.left)
        self.assertEqual(Direction.up.turn(Turn.ahead), Direction.up)
        self.assertEqual(Direction.right.turn(Turn.ahead), Direction.right)
