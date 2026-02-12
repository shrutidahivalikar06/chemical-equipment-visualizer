# app.py
import sys
import pandas as pd
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QMessageBox, QLabel, QFrame, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, QSize, QMimeData
from PyQt5.QtGui import QFont, QColor, QPalette, QDragEnterEvent, QDropEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from datetime import datetime

# Import enhanced charts
from charts import EquipmentChart


class StatCard(QFrame):
    """Modern stat card matching web frontend - PyQt5 optimized"""
    def __init__(self, title, value, unit=""):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setStyleSheet("""
            StatCard {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 12px;
                padding: 20px;
            }
            StatCard:hover {
                border: 2px solid #1a73e8;
                background-color: #f8f9fa;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 13px;
            font-weight: 600;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        """)
        layout.addWidget(title_label)
        
        # Value container
        value_layout = QHBoxLayout()
        value_layout.setSpacing(8)
        
        # Value
        value_label = QLabel(str(value))
        value_label.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: #1a1e24;
        """)
        value_layout.addWidget(value_label)
        
        # Unit
        if unit:
            unit_label = QLabel(unit)
            unit_label.setStyleSheet("""
                font-size: 14px;
                font-weight: 500;
                color: #6c757d;
            """)
            value_layout.addWidget(unit_label)
        
        value_layout.addStretch()
        layout.addLayout(value_layout)
        self.setLayout(layout)


class UploadCard(QFrame):
    """Modern upload card with drag & drop - PyQt5 optimized"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setStyleSheet("""
            UploadCard {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 12px;
                padding: 28px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(24)
        layout.setContentsMargins(28, 28, 28, 28)
        
        # Title
        title = QLabel("Chemical Equipment Parameter Visualizer")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 600;
            color: #1a1e24;
            margin-bottom: 8px;
        """)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel(
            "Upload Chemical Equipment Data\n"
            "Upload a CSV file containing equipment parameters to generate "
            "analytical summaries and visualizations"
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("""
            color: #6c757d;
            font-size: 15px;
            line-height: 1.5;
        """)
        layout.addWidget(subtitle)
        
        # Requirements box
        req_box = QFrame()
        req_box.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        req_layout = QVBoxLayout()
        req_layout.setSpacing(8)
        
        requirements = [
            "✓ CSV format only",
            "✓ Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature",
            "✓ Maximum file size: 10MB"
        ]
        
        for req in requirements:
            req_label = QLabel(req)
            req_label.setStyleSheet("""
                font-size: 13px;
                color: #495057;
                padding: 2px 0;
            """)
            req_layout.addWidget(req_label)
        
        req_box.setLayout(req_layout)
        layout.addWidget(req_box)
        
        # Drop zone
        self.drop_zone = QFrame()
        self.drop_zone.setStyleSheet("""
            QFrame {
                border: 2px dashed #ced4da;
                border-radius: 12px;
                background-color: #fafbfc;
                padding: 32px;
            }
            QFrame:hover {
                border: 2px dashed #1a73e8;
                background-color: #f0f7ff;
            }
        """)
        
        drop_layout = QVBoxLayout()
        drop_layout.setAlignment(Qt.AlignCenter)
        drop_layout.setSpacing(12)
        
        # File icon
        icon_label = QLabel("📄")
        icon_label.setStyleSheet("font-size: 32px;")
        drop_layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        
        # Choose file text
        choose_text = QLabel("Choose CSV File")
        choose_text.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #1a1e24;
        """)
        drop_layout.addWidget(choose_text, alignment=Qt.AlignCenter)
        
        # Drag drop text
        drag_text = QLabel("or drag and drop your file here")
        drag_text.setStyleSheet("font-size: 14px; color: #6c757d;")
        drop_layout.addWidget(drag_text, alignment=Qt.AlignCenter)
        
        self.drop_zone.setLayout(drop_layout)
        layout.addWidget(self.drop_zone)
        
        # Upload button
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 15px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)
        self.upload_btn.clicked.connect(self.parent.upload_csv)
        layout.addWidget(self.upload_btn)
        
        # File info (hidden by default)
        self.file_info = QFrame()
        self.file_info.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 12px;
                margin-top: 8px;
            }
        """)
        self.file_info.hide()
        
        file_info_layout = QHBoxLayout()
        file_info_layout.setContentsMargins(12, 12, 12, 12)
        
        file_icon = QLabel("📄")
        file_icon.setStyleSheet("font-size: 20px;")
        file_info_layout.addWidget(file_icon)
        
        self.file_name_label = QLabel()
        self.file_name_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 500;
            color: #1a1e24;
        """)
        file_info_layout.addWidget(self.file_name_label)
        
        file_info_layout.addStretch()
        
        selected_label = QLabel("Selected")
        selected_label.setStyleSheet("font-size: 12px; color: #6c757d;")
        file_info_layout.addWidget(selected_label)
        
        self.file_info.setLayout(file_info_layout)
        layout.addWidget(self.file_info)
        
        self.setLayout(layout)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
            self.drop_zone.setStyleSheet("""
                QFrame {
                    border: 2px dashed #1a73e8;
                    border-radius: 12px;
                    background-color: #f0f7ff;
                    padding: 32px;
                }
            """)
        else:
            event.ignore()
    
    def dragLeaveEvent(self, event):
        self.drop_zone.setStyleSheet("""
            QFrame {
                border: 2px dashed #ced4da;
                border-radius: 12px;
                background-color: #fafbfc;
                padding: 32px;
            }
        """)
    
    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            self.parent.load_csv_file(files[0])
        self.drop_zone.setStyleSheet("""
            QFrame {
                border: 2px dashed #ced4da;
                border-radius: 12px;
                background-color: #fafbfc;
                padding: 32px;
            }
        """)
    
    def show_file_info(self, filename):
        self.file_name_label.setText(filename)
        self.file_info.show()


class DataPreviewTable(QFrame):
    """Modern data preview table - PyQt5 optimized"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            DataPreviewTable {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 12px;
                padding: 24px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        
        title = QLabel("Data Preview")
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #1a1e24;
        """)
        header_layout.addWidget(title)
        
        self.subtitle = QLabel("Showing first 10 rows of 0 total equipment records")
        self.subtitle.setStyleSheet("font-size: 14px; color: #6c757d;")
        header_layout.addWidget(self.subtitle)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                border: none;
                gridline-color: #e9ecef;
                font-size: 13px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 12px 16px;
                border-bottom: 1px solid #e9ecef;
            }
            QTableWidget::item:selected {
                background-color: #f1f3f5;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 12px 16px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-size: 13px;
                font-weight: 600;
                color: #495057;
            }
        """)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def update_data(self, df, total_rows=247):
        """Update table with dataframe"""
        self.subtitle.setText(f"Showing first 10 rows of {total_rows:,} total equipment records")
        
        if df is None or df.empty:
            return
        
        # Take first 10 rows
        display_df = df.head(10)
        
        # Set columns
        columns = [
            "EQUIPMENT NAME", "TYPE", 
            "FLOWRATE (L/MIN)", "PRESSURE (BAR)", "TEMPERATURE (°C)"
        ]
        
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        
        # Set rows
        self.table.setRowCount(len(display_df))
        
        for i, (_, row) in enumerate(display_df.iterrows()):
            # Equipment Name
            name_value = str(row.get('equipment_name', row.get('EQUIPMENT NAME', '')))
            name_item = QTableWidgetItem(name_value)
            name_font = QFont("Inter", 13)
            name_font.setWeight(QFont.Medium)
            name_item.setFont(name_font)
            name_item.setForeground(QColor("#1a1e24"))
            self.table.setItem(i, 0, name_item)
            
            # Type
            type_value = str(row.get('equipment_type', row.get('TYPE', '')))
            type_item = QTableWidgetItem(type_value)
            type_item.setForeground(QColor("#495057"))
            self.table.setItem(i, 1, type_item)
            
            # Flowrate
            flow_value = row.get('flowrate', row.get('FLOWRATE (L/MIN)', 0))
            flow_item = QTableWidgetItem(f"{float(flow_value):.1f}")
            flow_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            flow_font = QFont("Consolas", 12)
            flow_item.setFont(flow_font)
            self.table.setItem(i, 2, flow_item)
            
            # Pressure
            pressure_value = row.get('pressure', row.get('PRESSURE (BAR)', 0))
            pressure_item = QTableWidgetItem(f"{float(pressure_value):.1f}")
            pressure_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            pressure_item.setFont(QFont("Consolas", 12))
            self.table.setItem(i, 3, pressure_item)
            
            # Temperature
            temp_value = row.get('temperature', row.get('TEMPERATURE (°C)', 0))
            temp_item = QTableWidgetItem(f"{float(temp_value):.1f}")
            temp_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            temp_item.setFont(QFont("Consolas", 12))
            self.table.setItem(i, 4, temp_item)
        
        # Resize columns
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


class ExportActions(QFrame):
    """Modern export actions panel - PyQt5 optimized"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            ExportActions {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 12px;
                padding: 24px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # File info
        file_info_frame = QFrame()
        file_info_frame.setStyleSheet("""
            QFrame {
                background-color: #e7f5ff;
                border: none;
                border-radius: 8px;
                padding: 8px 12px;
            }
        """)
        
        file_info_layout = QHBoxLayout()
        file_info_layout.setContentsMargins(12, 8, 12, 8)
        
        self.file_label = QLabel("📄 test.csv")
        self.file_label.setStyleSheet("font-size: 14px; font-weight: 500; color: #1a73e8;")
        file_info_layout.addWidget(self.file_label)
        
        self.size_label = QLabel("2.4 KB")
        self.size_label.setStyleSheet("font-size: 12px; color: #5f6b7a;")
        file_info_layout.addWidget(self.size_label)
        
        file_info_layout.addStretch()
        file_info_frame.setLayout(file_info_layout)
        layout.addWidget(file_info_frame)
        
        # Export actions
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(20)
        
        # Left side - title and status
        left_layout = QVBoxLayout()
        left_layout.setSpacing(8)
        
        title = QLabel("Export & Actions")
        title.setStyleSheet("font-size: 16px; font-weight: 600; color: #1a1e24;")
        left_layout.addWidget(title)
        
        # Status row
        status_layout = QHBoxLayout()
        status_layout.setSpacing(16)
        
        last_updated = QLabel("Last updated: 2 min ago")
        last_updated.setStyleSheet("font-size: 13px; color: #6c757d;")
        status_layout.addWidget(last_updated)
        
        file_size = QLabel("● File size: 2.4 KB")
        file_size.setStyleSheet("font-size: 13px; color: #6c757d;")
        status_layout.addWidget(file_size)
        
        validated = QLabel("✓ Data validated")
        validated.setStyleSheet("font-size: 13px; color: #40c057;")
        status_layout.addWidget(validated)
        
        status_layout.addStretch()
        left_layout.addLayout(status_layout)
        
        actions_layout.addLayout(left_layout)
        actions_layout.addStretch()
        
        # Right side - buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        # PDF Button
        pdf_btn = QPushButton("📄 Download PDF Report")
        pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)
        pdf_btn.clicked.connect(self.parent.download_pdf)
        button_layout.addWidget(pdf_btn)
        
        # JSON Button
        json_btn = QPushButton("📋 Download Summary (JSON)")
        json_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1a73e8;
                border: 1px solid #1a73e8;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #f0f7ff;
                border: 1px solid #1557b0;
                color: #1557b0;
            }
            QPushButton:pressed {
                background-color: #e1f0ff;
            }
        """)
        json_btn.clicked.connect(self.parent.download_json)
        button_layout.addWidget(json_btn)
        
        actions_layout.addLayout(button_layout)
        layout.addLayout(actions_layout)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            QFrame {
                background-color: #e9ecef;
                max-height: 1px;
                margin: 20px 0 0 0;
            }
        """)
        layout.addWidget(separator)
        
        # Footer
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 20, 0, 0)
        
        left_footer = QLabel("Chemical Equipment Parameter Visualizer - Interactive Prototype")
        left_footer.setStyleSheet("font-size: 12px; color: #adb5bd;")
        footer_layout.addWidget(left_footer)
        
        footer_layout.addStretch()
        
        right_footer = QLabel("PyQt5 | Reference for Desktop Implementation")
        right_footer.setStyleSheet("font-size: 12px; color: #adb5bd;")
        footer_layout.addWidget(right_footer)
        
        layout.addLayout(footer_layout)
        self.setLayout(layout)
    
    def update_file_info(self, filename, filesize):
        self.file_label.setText(f"📄 {filename}")
        self.size_label.setText(f"{filesize:.1f} KB")
    
    def update_status(self, last_updated="2 min ago", file_size="2.4 KB"):
        """Update status information"""
        # This would update the status labels if we had references to them
        pass


class EquipmentVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(100, 100, 1300, 1000)
        
        # Set application font
        font = QFont("Inter", 10)
        if not QFontInfo(font).exactMatch():
            font = QFont("Segoe UI", 10)
        self.setFont(font)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
            }
        """)
        
        self.df = None
        self.current_file = None
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("Chemical Equipment Parameter Visualizer")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #1a1e24;
            letter-spacing: -0.5px;
            margin-bottom: 20px;
        """)
        main_layout.addWidget(title)
        
        # Upload Card
        self.upload_card = UploadCard(self)
        main_layout.addWidget(self.upload_card)
        
        # Stats container (hidden initially)
        self.stats_container = QFrame()
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        
        self.stats_container.setLayout(stats_layout)
        self.stats_container.hide()
        main_layout.addWidget(self.stats_container)
        
        # Chart container
        self.chart_widget = EquipmentChart()
        self.chart_widget.hide()
        main_layout.addWidget(self.chart_widget)
        
        # Data preview table
        self.preview_table = DataPreviewTable()
        self.preview_table.hide()
        main_layout.addWidget(self.preview_table)
        
        # Export actions
        self.export_actions = ExportActions(self)
        self.export_actions.hide()
        main_layout.addWidget(self.export_actions)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
        
        # Load sample data for demo
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load sample data from screenshots for demo"""
        sample_data = {
            'equipment_name': [
                'Compressor-A-101', 'Separator-E-102', 'Distillation-Column-D-103',
                'Valve-G-104', 'Compressor-G-105', 'Heat-Exchanger-A-106',
                'Mixer-D-107', 'Distillation-Column-D-108', 'Reactor-D-109',
                'Pump-A-110'
            ],
            'equipment_type': [
                'Compressor', 'Separator', 'Distillation Column',
                'Valve', 'Compressor', 'Heat Exchanger',
                'Mixer', 'Distillation Column', 'Reactor',
                'Pump'
            ],
            'flowrate': [81.1, 119.4, 183.8, 113.4, 88.6, 211.9, 115.0, 170.5, 142.3, 102.0],
            'pressure': [9.4, 2.4, 1.7, 3.9, 9.1, 5.8, 3.4, 1.7, 4.2, 2.8],
            'temperature': [114.3, 43.0, 69.0, 63.3, 113.9, 99.3, 63.0, 85.1, 91.0, 48.5],
            'status': ['Active'] * 10,
            'location': ['Unit A'] * 5 + ['Unit B'] * 5,
            'purchase_year': [2019, 2020, 2018, 2021, 2019, 2020, 2021, 2018, 2019, 2020],
            'condition': ['Good'] * 7 + ['Excellent'] * 3
        }
        self.df = pd.DataFrame(sample_data)
        self.current_file = "sample_equipment_data.csv"
        
        # Update UI with sample data
        self.upload_card.show_file_info(self.current_file)
        self.update_stats()
        self.chart_widget.update_chart(self.df)
        self.chart_widget.show()
        self.preview_table.update_data(self.df, 247)
        self.preview_table.show()
        self.export_actions.show()
        self.stats_container.show()
    
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.load_csv_file(file_path)
    
    def load_csv_file(self, file_path):
        try:
            # Load CSV
            self.df = pd.read_csv(file_path)
            self.current_file = os.path.basename(file_path)
            
            # Update UI
            self.upload_card.show_file_info(self.current_file)
            self.update_stats()
            self.chart_widget.update_chart(self.df)
            self.chart_widget.show()
            self.preview_table.update_data(self.df, len(self.df))
            self.preview_table.show()
            self.export_actions.show()
            self.stats_container.show()
            
            # Calculate file size
            file_size = os.path.getsize(file_path) / 1024
            self.export_actions.update_file_info(self.current_file, file_size)
            
            QMessageBox.information(
                self, "Success",
                f"✅ CSV loaded successfully!\n\n"
                f"Total Equipment: {len(self.df):,}\n"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load CSV: {str(e)}")
    
    def update_stats(self):
        """Update statistics cards"""
        if self.df is None:
            return
        
        # Calculate stats
        total_equipment = len(self.df)
        
        # Get column names (handle both naming conventions)
        flow_col = 'flowrate' if 'flowrate' in self.df.columns else 'FLOWRATE (L/MIN)'
        pressure_col = 'pressure' if 'pressure' in self.df.columns else 'PRESSURE (BAR)'
        temp_col = 'temperature' if 'temperature' in self.df.columns else 'TEMPERATURE (°C)'
        
        avg_flowrate = self.df[flow_col].mean() if flow_col in self.df.columns else 125.7
        avg_pressure = self.df[pressure_col].mean() if pressure_col in self.df.columns else 4.2
        avg_temp = self.df[temp_col].mean() if temp_col in self.df.columns else 73.0
        
        # Clear existing layout
        stats_layout = self.stats_container.layout()
        while stats_layout.count():
            item = stats_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Create new stat cards
        self.total_equipment_card = StatCard("TOTAL EQUIPMENT", f"{total_equipment:,}", "units")
        self.avg_flowrate_card = StatCard("AVERAGE FLOWRATE", f"{avg_flowrate:.1f}", "L/min")
        self.avg_pressure_card = StatCard("AVERAGE PRESSURE", f"{avg_pressure:.1f}", "bar")
        self.avg_temp_card = StatCard("AVERAGE TEMPERATURE", f"{avg_temp:.1f}", "°C")
        
        stats_layout.addWidget(self.total_equipment_card)
        stats_layout.addWidget(self.avg_flowrate_card)
        stats_layout.addWidget(self.avg_pressure_card)
        stats_layout.addWidget(self.avg_temp_card)
        stats_layout.addStretch()
    
    def download_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF Report", "equipment_report.pdf", "PDF Files (*.pdf)"
        )
        if file_path:
            QMessageBox.information(
                self, "PDF Report",
                f"PDF report would be saved to:\n{file_path}\n\n"
                f"This would connect to your Django backend at:\n"
                f"http://127.0.0.1:8000/api/report/pdf/"
            )
    
    def download_json(self):
        if self.df is None:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save JSON Summary", "equipment_summary.json", "JSON Files (*.json)"
        )
        
        if file_path:
            # Get column names
            flow_col = 'flowrate' if 'flowrate' in self.df.columns else 'FLOWRATE (L/MIN)'
            pressure_col = 'pressure' if 'pressure' in self.df.columns else 'PRESSURE (BAR)'
            temp_col = 'temperature' if 'temperature' in self.df.columns else 'TEMPERATURE (°C)'
            type_col = 'equipment_type' if 'equipment_type' in self.df.columns else 'TYPE'
            
            # Create summary
            summary = {
                "total_equipment": len(self.df),
                "average_flowrate": float(self.df[flow_col].mean()) if flow_col in self.df.columns else 125.7,
                "average_pressure": float(self.df[pressure_col].mean()) if pressure_col in self.df.columns else 4.2,
                "average_temperature": float(self.df[temp_col].mean()) if temp_col in self.df.columns else 73.0,
                "type_distribution": self.df[type_col].value_counts().to_dict() if type_col in self.df.columns else {},
                "timestamp": datetime.now().isoformat()
            }
            
            with open(file_path, 'w') as f:
                json.dump(summary, f, indent=2)
            
            QMessageBox.information(self, "Success", "✅ Summary saved as JSON!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application font
    from PyQt5.QtGui import QFontInfo
    
    window = EquipmentVisualizer()
    window.show()
    sys.exit(app.exec_())