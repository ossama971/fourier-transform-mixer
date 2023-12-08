from PyQt6.QtGui import QPixmap, QImage, QPainter


def grayscale_image(original_pixmap):
    # Convert the QPixmap to a QImage
    original_image = original_pixmap.toImage()

    # Convert the QImage to grayscale
    grayscale_image = QImage(original_image.size(), QImage.Format.Format_Grayscale8)
    painter = QPainter(grayscale_image)
    painter.drawImage(0, 0, original_image)
    painter.end()

    # Convert the QImage back to a QPixmap
    grayscale_pixmap = QPixmap.fromImage(grayscale_image)

    return grayscale_pixmap
