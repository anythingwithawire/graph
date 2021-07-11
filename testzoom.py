from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene

        self.initUI()

        self.setScene(self.grScene)

        self.zoomInFactor = 1.25
        self.zoomClamp = False
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

    def initUI(self):
        # image quality
        self.setRenderHints(
            QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        #   Refresh
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # Close the scroll bar
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        # Determine the type of mouse press

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.rightMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)
        # Determine the type of mouse release

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)
        # Drag and drop function - Press to achieve

    def middleMouseButtonPress(self, event):
        # These sentences are not understood, and friends who understand can explain
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease,
                                   event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        #
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(),
                                event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton,
                                event.modifiers())
        super().mousePressEvent(fakeEvent)

        #  function - release implementation

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(),
                                event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton,
                                event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        # Cancel drag and drop
        self.setDragMode(QGraphicsView.NoDrag)

    def leftMouseButtonPress(self, event):
        return super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        return super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        return super().mousePressEvent(event)

    def rightMouseButtonRelease(self, event):
        return super().mouseReleaseEvent(event)

        # Roller zoom implementation

    def wheelEvent(self, event):
        # calculate our zoom Factor

        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        #  trigger
        if event.angleDelta().y() > 0:
            #  ratio 1.25
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
            # Zoom out trigger
        else:
            # Reduction ratio 0.8
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep
        # self.zoomRange[0] = 0 , self.zoomRange[1] =10
        # Limit the extreme of zooming, zoom out to self.zoom = -1 or zoom in to self.zoom=11
        # Cancel zoom ,
        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]:
            self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            # scaling implemented function
            self.scale(zoomFactor, zoomFactor)


