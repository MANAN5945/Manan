from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTextEdit, QPushButton, QLabel, QScrollArea, QListWidget,
                             QListWidgetItem, QGroupBox, QMessageBox)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor, QTextCursor
from PyQt5.QtCore import Qt, QSize

class RLE:
    def __init__(self):
        self.encoding_steps = []  # Stores each step of the encoding process
        self.original_size = 0    # Original text character count
        self.compressed_size = 0  # Compressed text character count

    def encode(self, text):
        """Encodes input text using RLE and tracks compression steps"""
        if not text:
            return ""
        
        self.encoding_steps = []
        self.original_size = len(text)  # Store original length

        encoded = []  # List to hold encoded parts
        current_char = text[0]
        count = 1

        # Iterate through characters to find consecutive runs
        for char in text[1:]:
            if char == current_char:
                count += 1
            else:
                # Add encoded part and record step
                encoded_part = f"{count}{current_char}"
                encoded.append(encoded_part)
                self.encoding_steps.append(f"'{current_char * count}' → '{encoded_part}'")
                current_char = char
                count = 1
        
        # Add the last character group
        encoded_part = f"{count}{current_char}"
        encoded.append(encoded_part)
        self.encoding_steps.append(f"'{current_char * count}' → '{encoded_part}'")
        
        compressed = "".join(encoded)
        self.compressed_size = len(compressed)  # Store compressed length
        return compressed

    def decode(self, encoded_text):
        """Decodes valid RLE encoded text back to original"""
        decoded = []
        i = 0
        
        try:
            while i < len(encoded_text):
                # Extract count digits
                count_str = ""
                while i < len(encoded_text) and encoded_text[i].isdigit():
                    count_str += encoded_text[i]
                    i += 1

                if i >= len(encoded_text):
                    break

                # Get character and repeat count
                char = encoded_text[i]
                count = int(count_str) if count_str else 1
                decoded.append(char * count)
                i += 1
        except:
            raise ValueError("Invalid RLE format")
        
        return "".join(decoded)

# Main application window class
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        # Window configuration
        self.setWindowTitle("RLE Compressor")
        self.resize(1200, 800)
        self.rle = RLE()  # RLE processor instance

        # Main widget and layout setup
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QHBoxLayout(main_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Create UI components
        self.create_input_panel()
        self.create_visualization_panel()
        self.create_output_panel()

        # Connect button signals to slots
        self.encode_btn.clicked.connect(self.encode_text)
        self.decode_btn.clicked.connect(self.decode_text)
        self.clear_btn.clicked.connect(self.clear_all)

        # Apply modern styling
        self.apply_styles()

    def create_input_panel(self):
        """Creates the left panel with input text area and buttons"""
        input_group = QGroupBox("Input Text")
        input_layout = QVBoxLayout()
        
        # Application title
        header = QLabel("Run-Length Encoding")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        
        # Text input area
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter text or RLE code...")
        self.input_text.setAcceptRichText(False)
        
        # Action buttons
        self.encode_btn = QPushButton("Encode")
        self.decode_btn = QPushButton("Decode")
        self.clear_btn = QPushButton("Clear All")
        
        # Assemble input panel
        input_layout.addWidget(header)
        input_layout.addWidget(self.input_text)
        input_layout.addWidget(self.encode_btn)
        input_layout.addWidget(self.decode_btn)
        input_layout.addWidget(self.clear_btn)
        input_group.setLayout(input_layout)
        
        self.main_layout.addWidget(input_group, 35)  # 35% width allocation

    def create_visualization_panel(self):
        """Creates the middle panel with compression steps and statistics"""
        vis_group = QGroupBox("Compression Process")
        vis_layout = QVBoxLayout()
        
        # List widget to show encoding steps
        self.steps_list = QListWidget()
        self.steps_list.setStyleSheet("font-family: Consolas;")
        
        # Statistics display group
        stats_group = QGroupBox("Statistics")
        stats_layout = QVBoxLayout()
        self.original_size_label = QLabel("Original Size: -")
        self.compressed_size_label = QLabel("Compressed Size: -")
        self.ratio_label = QLabel("Compression Ratio: -")
        
        # Configure statistic labels
        for label in [self.original_size_label, 
                     self.compressed_size_label,
                     self.ratio_label]:
            label.setFont(QFont("Segoe UI", 10))
            stats_layout.addWidget(label)
        
        stats_group.setLayout(stats_layout)
        
        # Assemble visualization panel
        vis_layout.addWidget(self.steps_list, 70)  # 70% height for steps
        vis_layout.addWidget(stats_group, 30)      # 30% for statistics
        vis_group.setLayout(vis_layout)
        
        self.main_layout.addWidget(vis_group, 40)  # 40% width allocation

    def create_output_panel(self):
        """Creates the right panel with output display"""
        output_group = QGroupBox("Output")
        output_layout = QVBoxLayout()
        
        # Read-only output display
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setStyleSheet("font-family: Consolas;")
        
        output_layout.addWidget(self.output_display)
        output_group.setLayout(output_layout)
        
        self.main_layout.addWidget(output_group, 25)  # 25% width allocation

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background: #f8f9fa;
            }
            QGroupBox {
                border: 2px solid #ced4da;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                font: bold 14px 'Segoe UI';
                color: #2b2d42;
            }
            QPushButton {
                background-color: #4a95f5;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                margin: 4px;
                font: 12px 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #3b7ccf;
            }
            QTextEdit, QListWidget {
                border: 2px solid #ced4da;
                border-radius: 6px;
                padding: 8px;
                font: 14px 'Consolas';
            }
            QListWidget::item {
                padding: 6px;
                border-bottom: 1px solid #eee;
            }
        """)

    def encode_text(self):
        """Handles text encoding when Encode button is clicked"""
        text = self.input_text.toPlainText().strip()
        
        if not text:
            self.show_error("Please enter text to encode!")
            return
            
        try:
            # Process encoding
            encoded = self.rle.encode(text)
            decoded = self.rle.decode(encoded)  # Verify encoding
            
            # Update step visualization
            self.steps_list.clear()
            self.steps_list.addItems(self.rle.encoding_steps)
            
            # Display results
            self.output_display.setPlainText(
                f"Encoded Result:\n{encoded}\n\n"
                f"Decoding Verification:\n{decoded}"
            )
            
            # Update statistics
            self.original_size_label.setText(f"Original Size: {self.rle.original_size} chars")
            self.compressed_size_label.setText(f"Compressed Size: {self.rle.compressed_size} chars")
            
            # Calculate compression ratio
            ratio = (1 - self.rle.compressed_size/self.rle.original_size) * 100
            self.ratio_label.setText(f"Compression Ratio: {ratio:.1f}%")
            
            # Warn if compression is inefficient
            if self.rle.compressed_size > self.rle.original_size:
                QMessageBox.warning(self, "Inefficient Compression", 
                    "RLE increased the size! Input contains too few repeated characters.")
            
        except Exception as e:
            self.show_error(f"Encoding error: {str(e)}")

    def decode_text(self):
        """Handles RLE decoding when Decode button is clicked"""
        text = self.input_text.toPlainText().strip()
        
        if not text:
            self.show_error("Please enter RLE code to decode!")
            return
            
        try:
            # Process decoding
            decoded = self.rle.decode(text)
            self.output_display.setPlainText(f"Decoded Result:\n{decoded}")
            
            # Clear encoding-specific displays
            self.steps_list.clear()
            self.original_size_label.setText("Original Size: -")
            self.compressed_size_label.setText("Compressed Size: -")
            self.ratio_label.setText("Compression Ratio: -")
            
        except Exception as e:
            self.show_error(f"Decoding error: {str(e)}")

    def clear_all(self):
        """Resets all UI elements to initial state"""
        self.input_text.clear()
        self.output_display.clear()
        self.steps_list.clear()
        self.original_size_label.setText("Original Size: -")
        self.compressed_size_label.setText("Compressed Size: -")
        self.ratio_label.setText("Compression Ratio: -")

    def show_error(self, message):
        """Displays error messages in a dialog"""
        QMessageBox.critical(self, "Error", message)

# Application entry point
if __name__ == "__main__":
    app = QApplication([])
    window = App()
    window.show()
    app.exec_()