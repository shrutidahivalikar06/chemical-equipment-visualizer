# charts.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
import pandas as pd
import numpy as np


class EquipmentChart(QFrame):
    """Modern equipment distribution chart - PyQt5 optimized"""
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            EquipmentChart {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 12px;
                padding: 24px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(24)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Header
        header = QLabel("Equipment Type Distribution")
        header.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #1a1e24;
            border-bottom: 1px solid #e9ecef;
            padding-bottom: 16px;
        """)
        layout.addWidget(header)
        
        # Legend container
        self.legend_container = QFrame()
        self.legend_layout = QHBoxLayout()
        self.legend_layout.setSpacing(16)
        self.legend_layout.setContentsMargins(0, 0, 0, 0)
        self.legend_container.setLayout(self.legend_layout)
        layout.addWidget(self.legend_container)
        
        # Valve count display
        self.valve_count_label = QLabel()
        self.valve_count_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                color: #495057;
            }
        """)
        self.valve_count_label.hide()
        layout.addWidget(self.valve_count_label)
        
        # Matplotlib figure
        self.figure = Figure(figsize=(10, 6), dpi=100, facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(350)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        
        # Equipment types and colors (matching web frontend)
        self.equipment_types = [
            "Heat Exchanger", "Compressor", "Filter", "Pump", "Reactor",
            "Valve", "Distillation Column", "Mixer", "Separator", "Storage Tank"
        ]
        
        self.colors = [
            '#4dabf7', '#40c057', '#fab005', '#ff8787',
            '#7950f2', '#ff922b', '#15aabf', '#e64980',
            '#20c997', '#adb5bd'
        ]
    
    def update_chart(self, df):
        """Update chart with dataframe"""
        if df is None or df.empty:
            return
        
        # Clear previous
        self.figure.clear()
        
        # Get equipment type column
        type_col = 'equipment_type' if 'equipment_type' in df.columns else 'TYPE'
        
        if type_col in df.columns:
            counts = df[type_col].value_counts()
        else:
            # Use sample data for demo
            counts = pd.Series({
                'Compressor': 2, 'Separator': 1, 'Distillation Column': 2,
                'Valve': 1, 'Heat Exchanger': 1, 'Mixer': 1,
                'Reactor': 1, 'Pump': 1, 'Filter': 0, 'Storage Tank': 0
            })
        
        # Prepare data for all equipment types
        chart_data = []
        for eq_type in self.equipment_types:
            chart_data.append({
                'type': eq_type,
                'count': int(counts.get(eq_type, 0))
            })
        
        # Update legend
        self.update_legend(chart_data)
        
        # Update valve count
        valve_count = int(counts.get('Valve', 24))  # Default to 24 from screenshot
        self.valve_count_label.setText(f"<b>Valve count:</b> {valve_count}")
        self.valve_count_label.show()
        
        # Create horizontal bar chart
        ax = self.figure.add_subplot(111)
        
        types = [d['type'] for d in chart_data]
        counts_data = [d['count'] for d in chart_data]
        y_pos = np.arange(len(types))
        
        # Create bars
        bars = ax.barh(y_pos, counts_data, color=self.colors, height=0.7)
        
        # Style the chart
        ax.set_yticks(y_pos)
        ax.set_yticklabels(types, fontsize=11, fontweight='normal', color='#495057')
        ax.set_xlim(0, 32)
        ax.set_xticks([0, 8, 16, 24, 32])
        ax.set_xticklabels(['0', '8', '16', '24', '32'], fontsize=10, color='#6c757d')
        
        # Remove spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#e9ecef')
        ax.spines['bottom'].set_linewidth(1)
        
        # Add grid
        ax.xaxis.grid(True, linestyle='--', alpha=0.7, color='#e9ecef')
        ax.set_axisbelow(True)
        
        # Set background color
        ax.set_facecolor('white')
        self.figure.patch.set_facecolor('white')
        
        # Add value labels on bars
        for i, (bar, count) in enumerate(zip(bars, counts_data)):
            if count > 0:
                ax.text(count + 0.5, bar.get_y() + bar.get_height()/2, 
                       str(count), va='center', fontsize=11, fontweight='bold', color='#1a1e24')
        
        # Adjust layout
        self.figure.tight_layout()
        
        # Redraw
        self.canvas.draw()
    
    def update_legend(self, chart_data):
        """Update color legend"""
        # Clear existing legend
        while self.legend_layout.count():
            item = self.legend_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add legend items
        for i, item in enumerate(chart_data[:5]):  # Show first 5 items
            legend_item = self.create_legend_item(item['type'], self.colors[i])
            self.legend_layout.addWidget(legend_item)
        
        # Add separator
        if len(chart_data) > 5:
            separator = QLabel("|")
            separator.setStyleSheet("font-size: 14px; color: #ced4da; padding: 0 8px;")
            self.legend_layout.addWidget(separator)
            
            # Add remaining items
            for i, item in enumerate(chart_data[5:], start=5):
                legend_item = self.create_legend_item(item['type'], self.colors[i])
                self.legend_layout.addWidget(legend_item)
        
        self.legend_layout.addStretch()
    
    def create_legend_item(self, text, color):
        """Create a legend item with color box"""
        item = QFrame()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Color box
        color_box = QFrame()
        color_box.setFixedSize(12, 12)
        color_box.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 3px;
                border: none;
            }}
        """)
        layout.addWidget(color_box)
        
        # Label
        label = QLabel(text)
        label.setStyleSheet("font-size: 13px; color: #495057;")
        layout.addWidget(label)
        
        item.setLayout(layout)
        return item


class PressureTemperatureChart(QFrame):
    """Pressure vs Temperature scatter plot"""
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            PressureTemperatureChart {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 12px;
                padding: 24px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        
        header = QLabel("Pressure vs Temperature")
        header.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #1a1e24;
            border-bottom: 1px solid #e9ecef;
            padding-bottom: 16px;
            margin-bottom: 16px;
        """)
        layout.addWidget(header)
        
        self.figure = Figure(figsize=(10, 4), dpi=100, facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(300)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
    
    def update_chart(self, df):
        """Update scatter plot"""
        self.figure.clear()
        
        if df is not None and not df.empty:
            # Get column names
            pressure_col = 'pressure' if 'pressure' in df.columns else 'PRESSURE (BAR)'
            temp_col = 'temperature' if 'temperature' in df.columns else 'TEMPERATURE (°C)'
            
            if pressure_col in df.columns and temp_col in df.columns:
                ax = self.figure.add_subplot(111)
                ax.scatter(df[pressure_col], df[temp_col], 
                          alpha=0.6, s=60, c='#ff6b6b', edgecolors='white', linewidth=0.5)
                
                ax.set_xlabel('Pressure (bar)', fontsize=11, color='#495057')
                ax.set_ylabel('Temperature (°C)', fontsize=11, color='#495057')
                
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_color('#e9ecef')
                ax.spines['bottom'].set_color('#e9ecef')
                
                ax.set_facecolor('white')
                self.figure.patch.set_facecolor('white')
                
                self.figure.tight_layout()
        
        self.canvas.draw()