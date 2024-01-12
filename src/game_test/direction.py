import unittest
from src.game.direction import Direction


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
