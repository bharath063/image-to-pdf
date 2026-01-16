import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QLabel, QMessageBox, QStyledItemDelegate, QDialog, QScrollArea,
    QStackedWidget
)
from PyQt6.QtGui import QIcon, QPixmap, QFont, QPainter, QPen, QColor, QDragEnterEvent, QDropEvent
from PyQt6.QtCore import Qt, QSize, QUrl
from PIL import Image
import os


THUMB_SIZE = 180


class DragHandleDelegate(QStyledItemDelegate):
    """Custom delegate to paint a drag handle on each item"""
    
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        
        # Draw drag handle (three horizontal lines) on the left
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Position for the drag handle
        x = option.rect.left() + 15
        y = option.rect.center().y()
        
        # Draw three horizontal lines
        pen = QPen(QColor(150, 150, 150), 2, Qt.PenStyle.SolidLine)
        painter.setPen(pen)
        
        for i in range(3):
            y_offset = y - 8 + (i * 8)
            painter.drawLine(x, y_offset, x + 20, y_offset)
        
        painter.restore()


class PreviewDialog(QDialog):
    """Dialog to preview the PDF pages"""
    
    def __init__(self, image_paths, parent=None):
        super().__init__(parent)
        self.image_paths = image_paths
        self.current_page = 0
        self.setWindowTitle("PDF Preview")
        self.setMinimumSize(800, 900)
        
        layout = QVBoxLayout(self)
        
        # Header with page counter
        header = QHBoxLayout()
        self.page_label = QLabel()
        self.page_label.setFont(QFont("System", 14, QFont.Weight.Bold))
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(self.page_label)
        layout.addLayout(header)
        
        # Scroll area for the image
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #2b2b2b; }")
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: white; padding: 20px;")
        scroll.setWidget(self.image_label)
        
        layout.addWidget(scroll)
        
        # Navigation buttons
        nav = QHBoxLayout()
        
        self.prev_btn = QPushButton("← Previous")
        self.prev_btn.clicked.connect(self.show_previous)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                font-size: 13px;
                background-color: #3a3a3a;
                border: 1px solid #555;
                border-radius: 4px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #666;
            }
        """)
        
        self.next_btn = QPushButton("Next →")
        self.next_btn.clicked.connect(self.show_next)
        self.next_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                font-size: 13px;
                background-color: #3a3a3a;
                border: 1px solid #555;
                border-radius: 4px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #666;
            }
        """)
        
        close_btn = QPushButton("Close Preview")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                font-size: 13px;
                background-color: #0066cc;
                border: none;
                border-radius: 4px;
                color: #ffffff;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0052a3;
            }
        """)
        
        nav.addWidget(self.prev_btn)
        nav.addStretch()
        nav.addWidget(close_btn)
        nav.addStretch()
        nav.addWidget(self.next_btn)
        
        layout.addLayout(nav)
        
        # Show first page
        self.update_page()
    
    def update_page(self):
        """Update the displayed page"""
        if not self.image_paths:
            return
        
        # Update page counter
        self.page_label.setText(f"Page {self.current_page + 1} of {len(self.image_paths)}")
        
        # Load and display image
        pixmap = QPixmap(self.image_paths[self.current_page])
        # Scale to fit while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(
            700, 900,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
        
        # Update button states
        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled(self.current_page < len(self.image_paths) - 1)
    
    def show_previous(self):
        """Show previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()
    
    def show_next(self):
        """Show next page"""
        if self.current_page < len(self.image_paths) - 1:
            self.current_page += 1
            self.update_page()


class EmptyStateWidget(QWidget):
    """Beautiful empty state when no images are loaded"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setAcceptDrops(True)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # Large icon/emoji
        icon_label = QLabel("📄")
        icon_label.setFont(QFont("System", 80))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Main title
        title = QLabel("No Images Yet")
        title.setFont(QFont("System", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #ffffff;")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("Drag & drop images here\nor click the button below")
        instructions.setFont(QFont("System", 14))
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setStyleSheet("color: #999; line-height: 1.6;")
        layout.addWidget(instructions)
        
        # Spacing
        layout.addSpacing(10)
        
        # Add Images button
        add_btn = QPushButton("➕ Add Images")
        add_btn.setFont(QFont("System", 14, QFont.Weight.Bold))
        add_btn.setFixedSize(180, 50)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self.parent_app.add_images)
        add_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                font-size: 15px;
                background-color: #0066cc;
                border: none;
                border-radius: 8px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #0052a3;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)
        
        # Center the button
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(add_btn)
        btn_container.addStretch()
        layout.addLayout(btn_container)
        
        # Supported formats
        formats = QLabel("Supported: JPG, PNG, BMP, WEBP, TIFF")
        formats.setFont(QFont("System", 11))
        formats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        formats.setStyleSheet("color: #666; margin-top: 20px;")
        layout.addWidget(formats)
        
        # Styling for the whole widget
        self.setStyleSheet("""
            EmptyStateWidget {
                background-color: #2b2b2b;
                border: 2px dashed #555;
                border-radius: 12px;
            }
        """)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                EmptyStateWidget {
                    background-color: #1a3a5a;
                    border: 2px dashed #0066cc;
                    border-radius: 12px;
                }
            """)
    
    def dragLeaveEvent(self, event):
        """Handle drag leave"""
        self.setStyleSheet("""
            EmptyStateWidget {
                background-color: #2b2b2b;
                border: 2px dashed #555;
                border-radius: 12px;
            }
        """)
    
    def dropEvent(self, event: QDropEvent):
        """Handle file drop"""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff')
        
        for file_path in files:
            if file_path.lower().endswith(image_extensions):
                self.parent_app.add_image_file(file_path)
        
        self.setStyleSheet("""
            EmptyStateWidget {
                background-color: #2b2b2b;
                border: 2px dashed #555;
                border-radius: 12px;
            }
        """)
        event.acceptProposedAction()


class ImageItem(QListWidgetItem):
    def __init__(self, path):
        super().__init__()
        self.path = path

        pixmap = QPixmap(path)
        pixmap = pixmap.scaled(
            140, 140,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.setIcon(QIcon(pixmap))
        self.setText(f"   {os.path.basename(path)}")  # Add spacing for drag handle
        self.setSizeHint(QSize(500, 160))
        self.setData(Qt.ItemDataRole.UserRole, path)



class ImageToPDFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image to PDF Converter")
        self.setMinimumSize(900, 600)

        layout = QVBoxLayout(self)

        title = QLabel("Image to PDF")
        title.setFont(QFont("System", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Drag to reorder pages • Select and remove if needed")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: gray;")
        layout.addWidget(subtitle)
        
        # Create stacked widget to switch between empty state and list view
        self.stacked_widget = QStackedWidget()
        
        # Empty state widget
        self.empty_state = EmptyStateWidget(self)
        self.stacked_widget.addWidget(self.empty_state)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.ViewMode.ListMode)
        self.list_widget.setIconSize(QSize(140, 140))
        self.list_widget.setSpacing(12)
        self.list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.list_widget.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.list_widget.setSelectionMode(
            QListWidget.SelectionMode.ExtendedSelection
        )
        self.list_widget.setVerticalScrollMode(
            QListWidget.ScrollMode.ScrollPerPixel
        )
        
        # Add custom delegate for drag handles
        self.list_widget.setItemDelegate(DragHandleDelegate())
        self.stacked_widget.addWidget(self.list_widget)
        
        # Show empty state initially
        self.stacked_widget.setCurrentWidget(self.empty_state)

        layout.addWidget(self.stacked_widget)

        btns = QHBoxLayout()

        self.add_btn = QPushButton("➕ Add Images")
        self.add_btn.clicked.connect(self.add_images)
        self.add_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                font-size: 13px;
                background-color: #3a3a3a;
                border: 1px solid #555;
                border-radius: 4px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)

        self.remove_btn = QPushButton("🗑 Remove Selected")
        self.remove_btn.clicked.connect(self.remove_selected)
        self.remove_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                font-size: 13px;
                background-color: #3a3a3a;
                border: 1px solid #555;
                border-radius: 4px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)

        self.preview_btn = QPushButton("👁 Preview PDF")
        self.preview_btn.clicked.connect(self.preview_pdf)
        self.preview_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                font-size: 13px;
                background-color: #3a3a3a;
                border: 1px solid #555;
                border-radius: 4px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)

        self.generate_btn = QPushButton("📄 Generate PDF")
        self.generate_btn.clicked.connect(self.generate_pdf)
        self.generate_btn.setDefault(True)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 24px;
                font-size: 13px;
                background-color: #0066cc;
                border: none;
                border-radius: 4px;
                color: #ffffff;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0052a3;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)

        btns.addWidget(self.add_btn)
        btns.addWidget(self.remove_btn)
        btns.addWidget(self.preview_btn)
        btns.addStretch()
        btns.addWidget(self.generate_btn)

        layout.addLayout(btns)

    def update_view(self):
        """Switch between empty state and list view based on content"""
        if self.list_widget.count() == 0:
            self.stacked_widget.setCurrentWidget(self.empty_state)
        else:
            self.stacked_widget.setCurrentWidget(self.list_widget)
    
    def add_image_file(self, path):
        """Add a single image file to the list"""
        existing = {
            self.list_widget.item(i).data(Qt.ItemDataRole.UserRole)
            for i in range(self.list_widget.count())
        }
        
        if path not in existing:
            self.list_widget.addItem(ImageItem(path))
            self.update_view()
    
    def add_images(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Add Images",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp *.tiff)"
        )

        for path in files:
            self.add_image_file(path)

    def remove_selected(self):
        for item in self.list_widget.selectedItems():
            self.list_widget.takeItem(self.list_widget.row(item))
        self.update_view()

    def preview_pdf(self):
        """Show PDF preview window"""
        if self.list_widget.count() == 0:
            QMessageBox.warning(self, "No Images", "Add images first to preview.")
            return
        
        # Collect all image paths in order
        image_paths = []
        for i in range(self.list_widget.count()):
            path = self.list_widget.item(i).data(Qt.ItemDataRole.UserRole)
            image_paths.append(path)
        
        # Show preview dialog
        preview_dialog = PreviewDialog(image_paths, self)
        preview_dialog.exec()

    def generate_pdf(self):
        if self.list_widget.count() == 0:
            QMessageBox.warning(self, "No Images", "Add images first.")
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if not output_path:
            return

        try:
            images = []
            for i in range(self.list_widget.count()):
                path = self.list_widget.item(i).data(Qt.ItemDataRole.UserRole)
                img = Image.open(path).convert("RGB")
                images.append(img)

            images[0].save(
                output_path,
                save_all=True,
                append_images=images[1:]
            )

            QMessageBox.information(
                self, "Done", f"PDF created successfully:\n{output_path}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # consistent dark/light look
    window = ImageToPDFApp()
    window.show()
    sys.exit(app.exec())

