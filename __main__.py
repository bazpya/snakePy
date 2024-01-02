from source.graphics import Circle, GraphWin, Point

window = GraphWin("snakePy", 500, 500)
circle1 = Circle(Point(50, 50), 10)
circle2 = Circle(Point(80, 80), 20)
circle1.draw(window)
circle2.draw(window)
window.getMouse()
window.close()
