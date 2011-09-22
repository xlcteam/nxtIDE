
class Clicker():
    def __init__(self):
        self.events = []

    def bind(self, rect, func):
        self.events.append((rect, func))

    def process(self, pos):
        for event in self.events:
            if self.in_rect(pos, event[0]):
                event[1]()
    
    def in_rect(self, pos, rect):
        if pos[0] >= rect[0][0] and pos[0] <= rect[0][0] + rect[1][0] and \
            pos[1] >= rect[0][1] and pos[1] <= rect[0][1] + rect[1][1]:
            return True
        else:
            return False

if __name__ == '__main__':
    def a():
        print "gotcha"

    clicker = Clicker()
    clicker.bind( ((0, 0,),(10, 10)) , a)
    clicker.process((10, 10))

#   def in_triangle(p, a, b, c):
#       xpBorder = b['x'] <= p['x']
#       ypBorder = b['y'] <= p['y']

#       return ((a['x'] <= p['x']) == xpBorder) and ((c['x'] <= p['x']) == xpBorder) or ((a['y'] <= p['y']) == ypBorder) and ((c['y'] <= p['y']) == ypBorder)


#   p = {'x': 1, 'y': 1}
#   a = {'x': 5, 'y': 5}
#   b = {'x': 5, 'y': 5}
#   c = {'x': 5, 'y': 5}
#   print in_triangle(p, a, b, c)

