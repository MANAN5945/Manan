import graphviz
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QTextEdit, QLabel, QMainWindow, QScrollArea,
                            QSizePolicy, QFileDialog, QMessageBox, QGroupBox)
from PyQt5.QtGui import QPixmap, QFont, QColor, QIcon
from PyQt5.QtCore import Qt, QByteArray, QSize
import heapq
from collections import defaultdict

class HuffmanCoding:
    """Huffman Coding implementation for text compression and decompression."""
    
    def __init__(self):
        """Initialize Huffman tree and code dictionaries."""
        self.huffman_tree = None
        self.codes = {}       # Character to binary code mapping
        self.reverse_codes = {}  # Binary code to character mapping

    class Node:
        """Node class for Huffman Tree nodes."""
        def __init__(self, char, freq):
            self.char = char  # Character (None for internal nodes)
            self.freq = freq  # Frequency of character/subtree
            self.left = None  # Left child
            self.right = None # Right child

        def __lt__(self, other):
            """Comparison method for priority queue."""
            return self.freq < other.freq

    def build_tree(self, text):
        """Build Huffman tree from input text."""
        # Calculate character frequencies
        frequency = defaultdict(int)
        for char in text:
            frequency[char] += 1

        # Create priority queue of leaf nodes
        priority_queue = [self.Node(char, freq) for char, freq in frequency.items()]
        heapq.heapify(priority_queue)

        # Build tree by merging nodes until one remains
        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            merged = self.Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(priority_queue, merged)

        # The last node is the root of the Huffman tree
        self.huffman_tree = priority_queue[0] if priority_queue else None
        self.codes = {}
        self.reverse_codes = {}
        self.generate_codes(self.huffman_tree, "")

    def generate_codes(self, node, current_code):
        """Recursively generate binary codes for characters."""
        if node is not None:
            if node.char is not None:  # Leaf node with character
                self.codes[node.char] = current_code
                self.reverse_codes[current_code] = node.char
            # Traverse left and right children
            self.generate_codes(node.left, current_code + "0")
            self.generate_codes(node.right, current_code + "1")

    def encode(self, text):
        """Encode text using generated Huffman codes."""
        return "".join(self.codes[char] for char in text) if self.codes else ""

    def decode(self, encoded_text):
        """Decode binary string using Huffman codes."""
        decoded_text = []
        current_code = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded_text.append(self.reverse_codes[current_code])
                current_code = ""
        return "".join(decoded_text)

    def visualize_tree(self):
        """Generate visual representation of Huffman tree using Graphviz."""
        if not self.huffman_tree:
            return None

        dot = graphviz.Digraph(comment="Huffman Tree")
        
        def add_node(node, parent_name=None):
            """Recursively add nodes and edges to Graphviz graph."""
            if node:
                node_id = str(id(node))  # Unique identifier for node
                # Label format: character/frequency for leaves, internal nodes show frequency
                label = f"{node.char}\n{node.freq}" if node.char else f"Internal\n{node.freq}"
                dot.node(node_id, label)
                if parent_name is not None:
                    dot.edge(parent_name, node_id)
                add_node(node.left, node_id)
                add_node(node.right, node_id)

        add_node(self.huffman_tree)
        return dot.pipe(format="png")  # Return PNG image data


class App(QMainWindow):
    """Main GUI application for Huffman Coding visualization."""
    
    def __init__(self):
        super().__init__()
        self.resize(1200, 800)
        self.current_image_data = None  # Stores current tree visualization PNG data
        
        # Central Widget Setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create UI components
        self.create_input_panel()
        self.create_visualization_panel()
        self.apply_styles()
        
        # Connect buttons to their functions
        self.btn_build.clicked.connect(self.generate)
        self.btn_clear.clicked.connect(self.reset)
        self.btn_save_text.clicked.connect(self.save_text)
        self.btn_save_image.clicked.connect(self.save_image)
        self.btn_load.clicked.connect(self.load_file)

    def create_input_panel(self):
        """Create left panel with input controls and results display."""
        input_panel = QVBoxLayout()
        input_panel.setSpacing(15)
        
        # Header
        header = QLabel("Huffman Coding")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        
        # Input text area
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter text to encode...")
        self.input_text.setAcceptRichText(False)
        
        # Button container with 5 action buttons
        btn_container = QHBoxLayout()
        self.btn_load = QPushButton("Load File")
        self.btn_build = QPushButton("Build Tree")
        self.btn_clear = QPushButton("Clear All")
        self.btn_save_text = QPushButton("Save Text")
        self.btn_save_image = QPushButton("Save Image")
        
        # Configure button appearance
        for btn in [self.btn_load, self.btn_build, self.btn_clear, 
                   self.btn_save_text, self.btn_save_image]:
            btn.setMinimumHeight(35)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        btn_container.addWidget(self.btn_load)
        btn_container.addWidget(self.btn_build)
        btn_container.addWidget(self.btn_clear)
        btn_container.addWidget(self.btn_save_text)
        btn_container.addWidget(self.btn_save_image)
        
        # Output display area
        self.output_display = QTextEdit()
        self.output_display.setPlaceholderText("Output")
        self.output_display.setReadOnly(True)
        
        input_panel.addWidget(header)
        input_panel.addWidget(self.input_text)
        input_panel.addLayout(btn_container)
        input_panel.addWidget(self.output_display)
        
        self.main_layout.addLayout(input_panel, 35)  # 35% width allocation

    def create_visualization_panel(self):
        """Create right panel for tree visualization and statistics."""
        vis_panel = QVBoxLayout()
        vis_panel.setSpacing(15)
        
        # Tree visualization label (holds the generated image)
        self.tree_label = QLabel()
        self.tree_label.setAlignment(Qt.AlignCenter)
        self.tree_label.setStyleSheet("background: white; border: 2px solid #ddd;")
        
        # Compression statistics group box
        stats_group = QGroupBox("Compression Statistics")
        stats_layout = QVBoxLayout()
        
        self.lbl_original = QLabel("Original Size: -")
        self.lbl_compressed = QLabel("Compressed Size: -")
        self.lbl_ratio = QLabel("Compression Ratio: -")
        
        for label in [self.lbl_original, self.lbl_compressed, self.lbl_ratio]:
            label.setFont(QFont("Segoe UI", 10))
            stats_layout.addWidget(label)
        
        stats_group.setLayout(stats_layout)
        
        vis_panel.addWidget(self.tree_label, 70)  # 70% height for visualization
        vis_panel.addWidget(stats_group, 30)      # 30% for statistics
        self.main_layout.addLayout(vis_panel, 65) # 65% width allocation

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QTextEdit, QLabel {
                border: 2px solid #d1d5db;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QPushButton {
                background-color: #4f46e5;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
            QPushButton:pressed {
                background-color: #3730a3;
            }
            QGroupBox {
                border: 2px solid #d1d5db;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
                font: bold 14px 'Segoe UI';
                color: #1f2937;
            }
        """)
    def generate(self):
        """Main processing function: build tree, encode text, and update UI."""
        text = self.input_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Input Error", "Please enter some text!")
            return
            
        try:
            huffman = HuffmanCoding()
            huffman.build_tree(text)
            
            # Calculate compression statistics
            original_size = len(text.encode('utf-8')) * 8  # in bits
            encoded_text = huffman.encode(text)
            compressed_size = len(encoded_text)  # in bits
            
            ratio = (1 - compressed_size/original_size) * 100 if original_size else 0
            
            # Update statistics labels
            self.lbl_original.setText(f"Original Size: {original_size//8} bytes")
            self.lbl_compressed.setText(f"Compressed Size: {(compressed_size + 7)//8} bytes")
            self.lbl_ratio.setText(f"Compression Ratio: {ratio:.2f}%")
            
            # Display results
            output = f"Encoded Text:\n{encoded_text}\n\nHuffman Codes:\n"
            output += "\n".join([f"'{k}': {v}" for k, v in huffman.codes.items()])
            self.output_display.setPlainText(output)
            
            # Update tree visualization
            self.update_tree_visualization(huffman)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def update_tree_visualization(self, huffman):
        """Update the tree visualization image from Huffman tree data."""
        image_data = huffman.visualize_tree()
        self.current_image_data = image_data
        
        if image_data:
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            
            # Scale image to fit available space while maintaining aspect ratio
            max_width = self.tree_label.width() - 20
            max_height = self.tree_label.height() - 20
            scaled_pixmap = pixmap.scaled(max_width, max_height, 
                                        Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.tree_label.setPixmap(scaled_pixmap)
            self.tree_label.setAlignment(Qt.AlignCenter)

    def reset(self):
        """Reset all UI elements to initial state."""
        self.input_text.clear()
        self.output_display.clear()
        self.tree_label.clear()
        self.current_image_data = None
        self.lbl_original.setText("Original Size: -")
        self.lbl_compressed.setText("Compressed Size: -")
        self.lbl_ratio.setText("Compression Ratio: -")

    def save_text(self):
        """Save current results (encoded text and codes) to a file."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Results", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'w') as f:
                    f.write(self.output_display.toPlainText())
                QMessageBox.information(self, "Success", "Text saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save text: {str(e)}")

    def save_image(self):
        """Save current tree visualization to PNG file."""
        if not self.current_image_data:
            QMessageBox.warning(self, "Error", "No tree generated to save!")
            return
            
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Tree Image", "huffman_tree.png", 
            "PNG Files (*.png);;All Files (*)", options=options)
        
        if file_name:
            try:
                if not file_name.lower().endswith('.png'):
                    file_name += '.png'
                
                with open(file_name, 'wb') as f:
                    f.write(self.current_image_data)
                QMessageBox.information(self, "Success", "Image saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save image: {str(e)}")

    def load_file(self):
        """Load text from a file into the input area."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Text File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    self.input_text.setText(f.read())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")

    def resizeEvent(self, event):
        """Handle window resize events to update tree visualization scaling."""
        if self.current_image_data:
            self.update_tree_visualization(HuffmanCoding())
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    window = App()
    window.show()
    app.exec_()