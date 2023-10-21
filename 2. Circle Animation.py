import math
import sys
from PyQt5.QtCore import QPropertyAnimation, QObject, QEvent, QPoint
from PyQt5.QtGui import QShortcutEvent
from PyQt5.QtWidgets import QFrame, QApplication


def degree_to_rad(degree: int) -> float:
    return (math.pi / 180) * degree


class YourWindow(QFrame):
    def __init__(self, app_obj: QApplication):
        super().__init__()
        self.resize(int(app_obj.desktop().height() * 0.4), int(app_obj.desktop().height() * 0.4))
        self.setWindowTitle("CircleAnimation")
        self.grabShortcut("Up")

        self.y_abs = int(self.height() // 2)  # Максимальная y координата по модулю
        self.x_abs = int(self.width() // 2)   # Максимальная x координата по модулю
        self.rotating_object_size = (int(self.width() * 0.05), int(self.height() * 0.05))
        self.rotating_object_pos = (int(self.x_abs * 2), int(self.y_abs - (self.rotating_object_size[1] // 2)))

        self.resize(self.x_abs * 2 + self.rotating_object_size[0], self.y_abs * 2 + self.rotating_object_size[1])
        self.rotating_object = QFrame(self)
        self.rotating_object.setStyleSheet("background-color: red")
        self.rotating_object.resize(*self.rotating_object_size)
        self.rotating_object.move(*self.rotating_object_pos)
        self.rotating_object.update()
        self.create_circle_animation(180, 2, self.rotating_object)

        self.installEventFilter(self)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if event.type() == event.Shortcut:
            event: QShortcutEvent
            self.animation_obj.start()
            print(event.key().toString())
        return super().eventFilter(obj, event)

    def projection_of_coordinates_on_pixels(self, x_cos, y_sin) -> tuple:
        return int(self.x_abs * x_cos), int(self.y_abs * 2 - (self.y_abs * y_sin))

    def create_circle_animation(self, degree: int, animation_sec: float, target: QFrame) -> QPropertyAnimation:
        animation_sec = int(animation_sec * 1000)
        self.animation_obj = QPropertyAnimation(target, b'pos')
        self.animation_obj.setDuration(animation_sec)
        self.animation_obj.setStartValue(target.pos())
        end_value = self.projection_of_coordinates_on_pixels(
            math.cos(degree_to_rad(degree))+1,
            math.sin(degree_to_rad(degree))+1)
        self.animation_obj.setEndValue(QPoint(*end_value))
        for degree_step in range(1, abs(degree) + 1):
            x_degree = degree_step
            y_degree = degree_step
            if degree < 0:
                x_degree, y_degree = -x_degree, -y_degree
            x_cord = math.cos(degree_to_rad(x_degree)) + 1
            y_cord = math.sin(degree_to_rad(y_degree)) + 1
            pos_projection = self.projection_of_coordinates_on_pixels(x_cord, y_cord)
            pos_projection = QPoint(*pos_projection)
            self.animation_obj.setKeyValueAt(x_degree / degree, pos_projection)
            print(f"cos | sin : {x_cord - 1} | {round(y_cord, 8) - 1} \n"
                  f"Degree: {x_degree}, {y_degree} \n"
                  f"Cords: {x_cord}, {y_cord} \n"
                  f"Pos projection: {pos_projection} \n"
                  f"Delta time: {x_degree / degree}")

        return self.animation_obj


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_instance = YourWindow(app)
    window_instance.show()
    sys.exit(app.exec_())

