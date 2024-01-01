from source.graphics import Circle, GraphWin, Point

win = GraphWin("My Circle", 100, 100)
c = Circle(Point(50, 50), 10)
c.draw(win)
win.getMouse()  # Pause to view result
win.close()  # Close window when done
