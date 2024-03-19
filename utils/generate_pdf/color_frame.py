from reportlab.lib.colors import toColor
from reportlab.platypus import Frame

class ColorFrame(Frame):
    """ Extends the reportlab Frame with a background color. """

    def __init__(self, *args, **kwargs):
        self.background = kwargs.pop('background')
        print(self.background)
        super().__init__(*args, **kwargs)

    def drawBackground(self, canv):
        color = toColor(self.background)
        print('>>>', color)
        canv.saveState()
        canv.setFillColor(color)
        canv.rect(
            self._x1, self._y1,
            self._x2 - self._x1,
            self._y2 - self._y1,
            stroke=0, fill=1
        )
        canv.restoreState()

    def addFromList(self, drawlist, canv):
        if self.background:
            self.drawBackground(canv)
        Frame.addFromList(self, drawlist, canv)
