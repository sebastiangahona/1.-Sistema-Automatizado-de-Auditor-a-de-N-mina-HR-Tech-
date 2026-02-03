"""
GUI Application for Payroll Auditing System
Modern Enterprise Design with Dark Mode

Features:
- Side navigation menu
- File upload functionality
- KPI cards for metrics
- Real-time audit results
- Color-coded alerts by severity
- Interactive visualizations

Author: Sistema de Auditoría de Nómina
Date: 2026
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
from auditor import PayrollAuditor
from reporter import PayrollReporter
import os
from datetime import datetime
import threading


class AuditApp(ctk.CTk):
    """
    Main GUI Application for Payroll Auditing System.
    
    Modern Enterprise design with dark mode, side navigation,
    and interactive audit results display.
    """
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("Sistema de Auditoría de Nómina - HR Tech")
        self.geometry("1200x750")
        
        # Set dark mode with BUK Blue accent
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Application state
        self.current_file = None
        self.auditor = None
        self.audit_complete = False
        
        # Color scheme - Modern Enterprise
        self.colors = {
            'bg_primary': '#1a1a1a',
            'bg_secondary': '#2b2b2b',
            'accent_blue': '#0066cc',
            'accent_green': '#00cc66',
            'critical': '#ff4444',
            'high': '#ff9944',
            'medium': '#ffcc44',
            'success': '#44ff88'
        }
        
        # Create UI
        self.create_layout()
        
    def create_layout(self):
        """Create the main layout with sidebar and content area."""
        
        # ===== SIDEBAR =====
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        
        # Logo/Title
        self.label_title = ctk.CTkLabel(
            self.sidebar, 
            text="📊 HR Tech\nAuditor",
            font=("Roboto", 28, "bold"),
            text_color=self.colors['accent_blue']
        )
        self.label_title.pack(pady=(30, 10), padx=20)
        
        self.label_subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Sistema de Auditoría\nde Nómina",
            font=("Roboto", 12),
            text_color="#cccccc"
        )
        self.label_subtitle.pack(pady=(0, 30), padx=20)
        
        # Separator
        separator1 = ctk.CTkFrame(self.sidebar, height=2, fg_color="#444444")
        separator1.pack(fill="x", padx=20, pady=10)
        
        # Menu Buttons
        self.btn_upload = ctk.CTkButton(
            self.sidebar,
            text="📁 Cargar Nómina",
            command=self.load_file,
            font=("Roboto", 14, "bold"),
            height=45,
            corner_radius=8,
            fg_color=self.colors['accent_blue'],
            hover_color="#0052a3"
        )
        self.btn_upload.pack(pady=10, padx=20, fill="x")
        
        self.btn_audit = ctk.CTkButton(
            self.sidebar,
            text="🔍 Ejecutar Auditoría",
            command=self.run_audit,
            font=("Roboto", 14, "bold"),
            height=45,
            corner_radius=8,
            state="disabled",
            fg_color=self.colors['accent_green'],
            hover_color="#00a352"
        )
        self.btn_audit.pack(pady=10, padx=20, fill="x")
        
        self.btn_reports = ctk.CTkButton(
            self.sidebar,
            text="📊 Generar Reportes",
            command=self.generate_reports,
            font=("Roboto", 14, "bold"),
            height=45,
            corner_radius=8,
            state="disabled",
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.btn_reports.pack(pady=10, padx=20, fill="x")
        
        # Separator
        separator2 = ctk.CTkFrame(self.sidebar, height=2, fg_color="#444444")
        separator2.pack(fill="x", padx=20, pady=(20, 10))
        
        # Info section
        self.info_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.info_frame.pack(pady=10, padx=20, fill="x")
        
        self.label_file_status = ctk.CTkLabel(
            self.info_frame,
            text="📄 Sin archivo",
            font=("Roboto", 11),
            text_color="#999999",
            anchor="w"
        )
        self.label_file_status.pack(fill="x", pady=2)
        
        self.label_records = ctk.CTkLabel(
            self.info_frame,
            text="📋 0 registros",
            font=("Roboto", 11),
            text_color="#999999",
            anchor="w"
        )
        self.label_records.pack(fill="x", pady=2)
        
        # Footer
        self.label_footer = ctk.CTkLabel(
            self.sidebar,
            text="© 2026 Sebastián Gahona\nHR Tech Solutions",
            font=("Roboto", 9),
            text_color="#666666"
        )
        self.label_footer.pack(side="bottom", pady=20, padx=20)
        
        # ===== MAIN CONTENT AREA =====
        self.main_content = ctk.CTkFrame(self, corner_radius=0)
        self.main_content.pack(side="right", fill="both", expand=True, padx=0, pady=0)
        
        # Create initial welcome screen
        self.create_welcome_screen()
    
    def create_welcome_screen(self):
        """Create the initial welcome screen."""
        
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.destroy()
        
        welcome_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        welcome_frame.pack(expand=True)
        
        # Welcome message
        welcome_title = ctk.CTkLabel(
            welcome_frame,
            text="🚀 Bienvenido al Sistema de Auditoría de Nómina",
            font=("Roboto", 32, "bold"),
            text_color=self.colors['accent_blue']
        )
        welcome_title.pack(pady=(0, 20))
        
        welcome_text = ctk.CTkLabel(
            welcome_frame,
            text="Sistema profesional de auditoría de cumplimiento laboral\n\n"
                 "✅ Validación automática del Código del Trabajo de Chile\n"
                 "✅ Detección de errores críticos en segundos\n"
                 "✅ Reportes ejecutivos profesionales\n\n"
                 "Comienza cargando un archivo CSV de nómina",
            font=("Roboto", 14),
            text_color="#cccccc",
            justify="center"
        )
        welcome_text.pack(pady=20)
        
        # Quick start button
        quick_start_btn = ctk.CTkButton(
            welcome_frame,
            text="📁 Cargar Archivo de Nómina",
            command=self.load_file,
            font=("Roboto", 16, "bold"),
            height=50,
            width=300,
            corner_radius=10,
            fg_color=self.colors['accent_blue'],
            hover_color="#0052a3"
        )
        quick_start_btn.pack(pady=30)
    
    def load_file(self):
        """Handle file upload functionality."""
        
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de nómina",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Load file to verify it's valid
                df = pd.read_csv(file_path)
                
                self.current_file = file_path
                self.audit_complete = False
                
                # Update UI
                filename = os.path.basename(file_path)
                self.label_file_status.configure(text=f"📄 {filename}")
                self.label_records.configure(text=f"📋 {len(df)} registros")
                
                # Enable audit button
                self.btn_audit.configure(state="normal")
                self.btn_reports.configure(state="disabled")
                
                # Show file preview
                self.show_file_preview(df, filename)
                
                messagebox.showinfo(
                    "Archivo Cargado",
                    f"✅ Archivo cargado exitosamente\n\n"
                    f"Registros: {len(df)}\n"
                    f"Columnas: {', '.join(df.columns.tolist()[:5])}..."
                )
                
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"❌ No se pudo cargar el archivo:\n\n{str(e)}"
                )
    
    def show_file_preview(self, df, filename):
        """Display preview of loaded file."""
        
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text=f"📄 {filename}",
            font=("Roboto", 24, "bold"),
            text_color=self.colors['accent_blue']
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text=f"Vista previa • {len(df)} empleados cargados",
            font=("Roboto", 12),
            text_color="#999999"
        )
        subtitle.pack(anchor="w")
        
        # Info cards
        info_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        info_frame.pack(fill="x", padx=30, pady=10)
        
        # Columns info
        col_card = ctk.CTkFrame(info_frame, corner_radius=10)
        col_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            col_card,
            text=f"📊 Columnas: {len(df.columns)}",
            font=("Roboto", 14, "bold")
        ).pack(pady=10, padx=15)
        
        ctk.CTkLabel(
            col_card,
            text=", ".join(df.columns.tolist()[:4]) + "...",
            font=("Roboto", 10),
            text_color="#999999"
        ).pack(pady=(0, 10), padx=15)
        
        # Data types info
        type_card = ctk.CTkFrame(info_frame, corner_radius=10)
        type_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            type_card,
            text=f"📋 Registros: {len(df)}",
            font=("Roboto", 14, "bold")
        ).pack(pady=10, padx=15)
        
        ctk.CTkLabel(
            type_card,
            text="Listos para auditar",
            font=("Roboto", 10),
            text_color="#999999"
        ).pack(pady=(0, 10), padx=15)
        
        # Preview text
        preview_frame = ctk.CTkFrame(self.main_content, corner_radius=10)
        preview_frame.pack(fill="both", expand=True, padx=30, pady=(10, 20))
        
        preview_label = ctk.CTkLabel(
            preview_frame,
            text="Vista Previa (primeras 10 filas):",
            font=("Roboto", 12, "bold")
        )
        preview_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        # Create scrollable text area for preview
        preview_text = ctk.CTkTextbox(
            preview_frame,
            font=("Courier", 10),
            height=300
        )
        preview_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Insert preview data
        preview_data = df.head(10).to_string()
        preview_text.insert("1.0", preview_data)
        preview_text.configure(state="disabled")
        
        # Call to action
        cta_label = ctk.CTkLabel(
            self.main_content,
            text="👉 Haz clic en 'Ejecutar Auditoría' para comenzar el análisis",
            font=("Roboto", 14, "bold"),
            text_color=self.colors['accent_green']
        )
        cta_label.pack(pady=(0, 20))
    
    def run_audit(self):
        """Execute the payroll audit."""
        
        if not self.current_file:
            messagebox.showwarning("Advertencia", "Por favor carga un archivo primero")
            return
        
        # Disable buttons during audit
        self.btn_audit.configure(state="disabled", text="⏳ Auditando...")
        self.btn_upload.configure(state="disabled")
        
        # Show progress screen
        self.show_progress_screen()
        
        # Run audit in separate thread to avoid freezing UI
        thread = threading.Thread(target=self._execute_audit)
        thread.start()
    
    def show_progress_screen(self):
        """Display progress/loading screen during audit."""
        
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.destroy()
        
        progress_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        progress_frame.pack(expand=True)
        
        ctk.CTkLabel(
            progress_frame,
            text="🔍 Ejecutando Auditoría...",
            font=("Roboto", 28, "bold"),
            text_color=self.colors['accent_blue']
        ).pack(pady=20)
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            width=400,
            mode="indeterminate"
        )
        self.progress_bar.pack(pady=20)
        self.progress_bar.start()
        
        ctk.CTkLabel(
            progress_frame,
            text="Validando cumplimiento del Código del Trabajo...\n"
                 "Este proceso puede tomar unos segundos.",
            font=("Roboto", 12),
            text_color="#cccccc"
        ).pack(pady=10)
    
    def _execute_audit(self):
        """Internal method to execute audit in background thread."""
        
        try:
            # Create auditor instance
            self.auditor = PayrollAuditor(self.current_file)
            
            # Run full audit
            total_alerts, financial_impact = self.auditor.run_full_audit()
            
            self.audit_complete = True
            
            # Update UI in main thread
            self.after(0, self._audit_complete_callback)
            
        except Exception as e:
            self.after(0, lambda: self._audit_error_callback(str(e)))
    
    def _audit_complete_callback(self):
        """Callback when audit completes successfully."""
        
        # Stop progress bar
        if hasattr(self, 'progress_bar'):
            self.progress_bar.stop()
        
        # Re-enable buttons
        self.btn_audit.configure(state="normal", text="🔍 Ejecutar Auditoría")
        self.btn_upload.configure(state="normal")
        self.btn_reports.configure(state="normal")
        
        # Show results
        self.show_audit_results()
        
        # Show completion message
        messagebox.showinfo(
            "Auditoría Completa",
            f"✅ Auditoría ejecutada exitosamente\n\n"
            f"Total de alertas: {len(self.auditor.alerts)}\n"
            f"Impacto financiero: CLP ${sum(a['impacto_financiero'] for a in self.auditor.alerts):,.0f}"
        )
    
    def _audit_error_callback(self, error_msg):
        """Callback when audit encounters an error."""
        
        # Stop progress bar
        if hasattr(self, 'progress_bar'):
            self.progress_bar.stop()
        
        # Re-enable buttons
        self.btn_audit.configure(state="normal", text="🔍 Ejecutar Auditoría")
        self.btn_upload.configure(state="normal")
        
        messagebox.showerror(
            "Error en Auditoría",
            f"❌ Ocurrió un error durante la auditoría:\n\n{error_msg}"
        )
        
        self.create_welcome_screen()
    
    def show_audit_results(self):
        """Display audit results with KPI cards and alerts."""
        
        if not self.auditor:
            return
        
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.destroy()
        
        # Create scrollable frame for results
        scrollable_frame = ctk.CTkScrollableFrame(
            self.main_content,
            corner_radius=0,
            fg_color="transparent"
        )
        scrollable_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Header
        header_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text="📊 Resultados de Auditoría",
            font=("Roboto", 28, "bold"),
            text_color=self.colors['accent_blue']
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text=f"Análisis completado • {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            font=("Roboto", 12),
            text_color="#999999"
        )
        subtitle.pack(anchor="w")
        
        # KPI Cards
        kpi_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        kpi_frame.pack(fill="x", padx=30, pady=20)
        
        # Total employees
        self.create_kpi_card(
            kpi_frame,
            "👥 Empleados",
            str(len(self.auditor.df)),
            "Total auditados",
            self.colors['accent_blue']
        ).pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Total alerts
        critical_count = sum(1 for a in self.auditor.alerts if a['severidad'] == 'CRÍTICA')
        alert_color = self.colors['critical'] if critical_count > 0 else self.colors['success']
        
        self.create_kpi_card(
            kpi_frame,
            "⚠️ Alertas",
            str(len(self.auditor.alerts)),
            f"{critical_count} críticas",
            alert_color
        ).pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Financial impact
        total_impact = sum(a['impacto_financiero'] for a in self.auditor.alerts)
        
        self.create_kpi_card(
            kpi_frame,
            "💰 Impacto",
            f"${total_impact:,.0f}",
            "CLP",
            self.colors['high']
        ).pack(side="left", fill="both", expand=True)
        
        # Severity breakdown
        severity_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
        severity_frame.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(
            severity_frame,
            text="📋 Distribución por Severidad",
            font=("Roboto", 16, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        severity_counts = {
            'CRÍTICA': sum(1 for a in self.auditor.alerts if a['severidad'] == 'CRÍTICA'),
            'ALTA': sum(1 for a in self.auditor.alerts if a['severidad'] == 'ALTA'),
            'MEDIA': sum(1 for a in self.auditor.alerts if a['severidad'] == 'MEDIA')
        }
        
        for severity, count in severity_counts.items():
            if count > 0:
                color = {
                    'CRÍTICA': self.colors['critical'],
                    'ALTA': self.colors['high'],
                    'MEDIA': self.colors['medium']
                }[severity]
                
                severity_item = ctk.CTkFrame(severity_frame, fg_color="transparent")
                severity_item.pack(fill="x", padx=20, pady=5)
                
                ctk.CTkLabel(
                    severity_item,
                    text=f"● {severity}:",
                    font=("Roboto", 14, "bold"),
                    text_color=color,
                    width=100,
                    anchor="w"
                ).pack(side="left")
                
                ctk.CTkLabel(
                    severity_item,
                    text=f"{count} alerta(s)",
                    font=("Roboto", 14),
                    text_color="#cccccc"
                ).pack(side="left")
        
        ctk.CTkLabel(severity_frame, text="").pack(pady=5)  # Spacing
        
        # Alerts detail
        if self.auditor.alerts:
            alerts_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
            alerts_frame.pack(fill="both", expand=True, padx=30, pady=10)
            
            ctk.CTkLabel(
                alerts_frame,
                text=f"🔍 Detalle de Alertas ({len(self.auditor.alerts)} encontradas)",
                font=("Roboto", 16, "bold")
            ).pack(anchor="w", padx=20, pady=(15, 10))
            
            # Display first 20 alerts
            for i, alert in enumerate(self.auditor.alerts[:20]):
                alert_item = self.create_alert_item(alerts_frame, alert)
                alert_item.pack(fill="x", padx=20, pady=5)
            
            if len(self.auditor.alerts) > 20:
                ctk.CTkLabel(
                    alerts_frame,
                    text=f"... y {len(self.auditor.alerts) - 20} alertas más\n"
                         f"Ver reporte completo en Excel",
                    font=("Roboto", 11),
                    text_color="#999999"
                ).pack(pady=10)
            
            ctk.CTkLabel(alerts_frame, text="").pack(pady=10)  # Spacing
        else:
            # No alerts - success message
            success_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10, fg_color="#1a4d2e")
            success_frame.pack(fill="x", padx=30, pady=10)
            
            ctk.CTkLabel(
                success_frame,
                text="✅ ¡Excelente! No se encontraron problemas",
                font=("Roboto", 18, "bold"),
                text_color=self.colors['success']
            ).pack(pady=20)
            
            ctk.CTkLabel(
                success_frame,
                text="Todos los registros cumplen con la normativa legal vigente",
                font=("Roboto", 12),
                text_color="#cccccc"
            ).pack(pady=(0, 20))
    
    def create_kpi_card(self, parent, title, value, subtitle, color):
        """Create a KPI card widget."""
        
        card = ctk.CTkFrame(parent, corner_radius=10)
        
        ctk.CTkLabel(
            card,
            text=title,
            font=("Roboto", 12),
            text_color="#999999"
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            card,
            text=value,
            font=("Roboto", 32, "bold"),
            text_color=color
        ).pack(pady=5)
        
        ctk.CTkLabel(
            card,
            text=subtitle,
            font=("Roboto", 10),
            text_color="#666666"
        ).pack(pady=(0, 15))
        
        return card
    
    def create_alert_item(self, parent, alert):
        """Create an alert item widget."""
        
        severity_colors = {
            'CRÍTICA': self.colors['critical'],
            'ALTA': self.colors['high'],
            'MEDIA': self.colors['medium']
        }
        
        item_frame = ctk.CTkFrame(parent, corner_radius=8)
        
        # Severity badge
        badge_color = severity_colors.get(alert['severidad'], '#666666')
        
        header = ctk.CTkFrame(item_frame, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(
            header,
            text=f"● {alert['severidad']}",
            font=("Roboto", 11, "bold"),
            text_color=badge_color,
            width=80,
            anchor="w"
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text=alert['tipo'].replace('_', ' ').title(),
            font=("Roboto", 12, "bold"),
            text_color="#ffffff"
        ).pack(side="left", padx=10)
        
        # Details
        ctk.CTkLabel(
            item_frame,
            text=f"👤 {alert['nombre']} ({alert['rut']})",
            font=("Roboto", 11),
            text_color="#cccccc",
            anchor="w"
        ).pack(fill="x", padx=15, pady=2)
        
        ctk.CTkLabel(
            item_frame,
            text=alert['detalle'],
            font=("Roboto", 10),
            text_color="#999999",
            anchor="w",
            wraplength=700
        ).pack(fill="x", padx=15, pady=2)
        
        if alert['impacto_financiero'] > 0:
            ctk.CTkLabel(
                item_frame,
                text=f"💰 Impacto: CLP ${alert['impacto_financiero']:,.0f}",
                font=("Roboto", 10, "bold"),
                text_color=self.colors['high'],
                anchor="w"
            ).pack(fill="x", padx=15, pady=(2, 10))
        else:
            ctk.CTkLabel(item_frame, text="").pack(pady=5)
        
        return item_frame
    
    def generate_reports(self):
        """Generate professional reports (Excel and Dashboard)."""
        
        if not self.auditor or not self.audit_complete:
            messagebox.showwarning(
                "Advertencia",
                "Por favor ejecuta una auditoría primero"
            )
            return
        
        try:
            # Disable button during generation
            self.btn_reports.configure(state="disabled", text="⏳ Generando...")
            
            # Generate reports
            reporter = PayrollReporter(self.auditor)
            reports = reporter.generate_full_report()
            
            # Re-enable button
            self.btn_reports.configure(state="normal", text="📊 Generar Reportes")
            
            # Show success message with file locations
            messagebox.showinfo(
                "Reportes Generados",
                f"✅ Reportes generados exitosamente\n\n"
                f"📊 Excel: {os.path.basename(reports['excel'])}\n"
                f"📈 Dashboard: {os.path.basename(reports['dashboard'])}\n\n"
                f"Ubicación: reports/"
            )
            
        except Exception as e:
            self.btn_reports.configure(state="normal", text="📊 Generar Reportes")
            messagebox.showerror(
                "Error",
                f"❌ Error al generar reportes:\n\n{str(e)}"
            )


def main():
    """Main entry point for the GUI application."""
    app = AuditApp()
    app.mainloop()


if __name__ == "__main__":
    main()
