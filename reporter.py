"""
Payroll Audit Reporter - Professional Report Generation
Generates executive reports with visual analytics and formatted exports.

Outputs:
- Excel reports with color-coded alerts
- Visual dashboards with matplotlib
- Financial impact analysis

Author: Sistema de Auditoría de Nómina
Date: 2026
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os


class PayrollReporter:
    """
    Generates professional audit reports with visualizations.
    
    Attributes:
        auditor: PayrollAuditor instance with audit results
        output_dir (str): Directory for saving reports
    """
    
    def __init__(self, auditor, output_dir='reports'):
        """
        Initialize the reporter.
        
        Args:
            auditor: PayrollAuditor instance with completed audit
            output_dir (str): Directory to save reports
        """
        self.auditor = auditor
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"📁 Directorio creado: {output_dir}/")
    
    def export_to_excel(self, filename='reporte_auditoria.xlsx'):
        """
        Export audit results to formatted Excel file.
        
        Features:
        - Critical findings highlighted in red
        - Professional formatting
        - Multiple sheets for different data views
        
        Args:
            filename (str): Output Excel filename
        """
        filepath = os.path.join(self.output_dir, filename)
        
        print(f"\n📊 Generando reporte Excel...")
        
        # Create Excel writer
        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Define formats
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1
            })
            
            critical_format = workbook.add_format({
                'bg_color': '#FF6B6B',
                'font_color': 'white',
                'border': 1
            })
            
            high_format = workbook.add_format({
                'bg_color': '#FFA500',
                'font_color': 'white',
                'border': 1
            })
            
            medium_format = workbook.add_format({
                'bg_color': '#FFD93D',
                'border': 1
            })
            
            currency_format = workbook.add_format({
                'num_format': '$#,##0',
                'border': 1
            })
            
            # Sheet 1: Critical Findings
            if self.auditor.alerts:
                alerts_df = self.auditor.get_alerts_dataframe()
                alerts_df.to_excel(writer, sheet_name='Hallazgos Críticos', index=False)
                
                worksheet = writer.sheets['Hallazgos Críticos']
                
                # Apply header format
                for col_num, value in enumerate(alerts_df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                
                # Apply conditional formatting based on severity
                for row_num in range(len(alerts_df)):
                    severity = alerts_df.iloc[row_num]['severidad']
                    
                    if severity == 'CRÍTICA':
                        row_format = critical_format
                    elif severity == 'ALTA':
                        row_format = high_format
                    else:
                        row_format = medium_format
                    
                    for col_num in range(len(alerts_df.columns)):
                        if alerts_df.columns[col_num] == 'impacto_financiero':
                            worksheet.write(row_num + 1, col_num, 
                                          alerts_df.iloc[row_num, col_num], 
                                          currency_format)
                        else:
                            worksheet.write(row_num + 1, col_num, 
                                          alerts_df.iloc[row_num, col_num], 
                                          row_format)
                
                # Adjust column widths
                worksheet.set_column('A:A', 25)  # tipo
                worksheet.set_column('B:B', 12)  # severidad
                worksheet.set_column('C:C', 15)  # rut
                worksheet.set_column('D:D', 25)  # nombre
                worksheet.set_column('E:E', 60)  # detalle
                worksheet.set_column('F:F', 18)  # impacto_financiero
                worksheet.set_column('G:G', 30)  # articulo_legal
            
            # Sheet 2: Full Data
            self.auditor.df.to_excel(writer, sheet_name='Datos Completos', index=False)
            worksheet2 = writer.sheets['Datos Completos']
            
            # Apply header format
            for col_num, value in enumerate(self.auditor.df.columns.values):
                worksheet2.write(0, col_num, value, header_format)
            
            # Adjust column widths
            for i, col in enumerate(self.auditor.df.columns):
                max_len = max(
                    self.auditor.df[col].astype(str).apply(len).max(),
                    len(col)
                ) + 2
                worksheet2.set_column(i, i, min(max_len, 50))
            
            # Sheet 3: Summary Statistics
            summary_data = {
                'Métrica': [
                    'Total Empleados',
                    'Total Alertas',
                    'Alertas Críticas',
                    'Alertas Altas',
                    'Alertas Medias',
                    'Impacto Financiero Total (CLP)'
                ],
                'Valor': [
                    len(self.auditor.df),
                    len(self.auditor.alerts),
                    sum(1 for a in self.auditor.alerts if a['severidad'] == 'CRÍTICA'),
                    sum(1 for a in self.auditor.alerts if a['severidad'] == 'ALTA'),
                    sum(1 for a in self.auditor.alerts if a['severidad'] == 'MEDIA'),
                    sum(alert['impacto_financiero'] for alert in self.auditor.alerts)
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Resumen Ejecutivo', index=False)
            
            worksheet3 = writer.sheets['Resumen Ejecutivo']
            for col_num, value in enumerate(summary_df.columns.values):
                worksheet3.write(0, col_num, value, header_format)
            
            worksheet3.set_column('A:A', 35)
            worksheet3.set_column('B:B', 25)
        
        print(f"✅ Reporte Excel generado: {filepath}")
        return filepath
    
    def create_dashboard(self, filename='dashboard_auditoria.png'):
        """
        Create visual dashboard with key metrics and charts.
        
        Args:
            filename (str): Output image filename
        """
        filepath = os.path.join(self.output_dir, filename)
        
        print(f"\n📈 Generando dashboard visual...")
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (16, 10)
        
        # Create figure with subplots
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # Title
        fig.suptitle('📊 Dashboard de Auditoría de Nómina', 
                     fontsize=20, fontweight='bold', y=0.98)
        
        if not self.auditor.alerts:
            # No alerts case
            ax = fig.add_subplot(gs[:, :])
            ax.text(0.5, 0.5, '✅ No se encontraron problemas\nTodos los registros cumplen con la normativa',
                   ha='center', va='center', fontsize=24, color='green')
            ax.axis('off')
        else:
            alerts_df = self.auditor.get_alerts_dataframe()
            
            # 1. Alerts by Type
            ax1 = fig.add_subplot(gs[0, 0])
            type_counts = alerts_df['tipo'].value_counts()
            colors_type = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
            type_counts.plot(kind='bar', ax=ax1, color=colors_type[:len(type_counts)])
            ax1.set_title('Alertas por Tipo', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Tipo de Alerta', fontsize=11)
            ax1.set_ylabel('Cantidad', fontsize=11)
            ax1.tick_params(axis='x', rotation=45)
            
            # 2. Alerts by Severity
            ax2 = fig.add_subplot(gs[0, 1])
            severity_counts = alerts_df['severidad'].value_counts()
            colors_severity = {'CRÍTICA': '#FF6B6B', 'ALTA': '#FFA500', 'MEDIA': '#FFD93D'}
            severity_colors = [colors_severity.get(x, '#CCCCCC') for x in severity_counts.index]
            severity_counts.plot(kind='pie', ax=ax2, colors=severity_colors, autopct='%1.1f%%')
            ax2.set_title('Distribución por Severidad', fontsize=14, fontweight='bold')
            ax2.set_ylabel('')
            
            # 3. Financial Impact by Type
            ax3 = fig.add_subplot(gs[1, :])
            impact_by_type = alerts_df.groupby('tipo')['impacto_financiero'].sum().sort_values(ascending=False)
            colors_impact = plt.cm.Reds(range(50, 200, 150//len(impact_by_type)))
            impact_by_type.plot(kind='barh', ax=ax3, color=colors_impact)
            ax3.set_title('💰 Impacto Financiero por Tipo de Error (CLP)', 
                         fontsize=14, fontweight='bold')
            ax3.set_xlabel('Impacto Financiero (CLP)', fontsize=11)
            ax3.set_ylabel('Tipo de Error', fontsize=11)
            
            # Format currency on x-axis
            ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
            
            # 4. Summary Statistics
            ax4 = fig.add_subplot(gs[2, :])
            ax4.axis('off')
            
            total_impact = alerts_df['impacto_financiero'].sum()
            critical_count = sum(1 for a in self.auditor.alerts if a['severidad'] == 'CRÍTICA')
            
            summary_text = f"""
            📋 RESUMEN EJECUTIVO DE AUDITORÍA
            
            Total de Empleados Auditados: {len(self.auditor.df)}
            Total de Alertas Detectadas: {len(self.auditor.alerts)}
            
            Alertas Críticas: {critical_count}
            Alertas Altas: {sum(1 for a in self.auditor.alerts if a['severidad'] == 'ALTA')}
            Alertas Medias: {sum(1 for a in self.auditor.alerts if a['severidad'] == 'MEDIA')}
            
            💵 Impacto Financiero Total: CLP ${total_impact:,.0f}
            
            ⚖️  Base Legal: Código del Trabajo de Chile
            📅 Fecha de Auditoría: {datetime.now().strftime('%d/%m/%Y %H:%M')}
            """
            
            ax4.text(0.1, 0.5, summary_text, fontsize=12, family='monospace',
                    verticalalignment='center',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        # Save figure
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Dashboard generado: {filepath}")
        return filepath
    
    def generate_full_report(self):
        """
        Generate complete audit report package.
        
        Returns:
            dict: Paths to generated report files
        """
        print("\n" + "="*80)
        print("📝 GENERANDO REPORTES PROFESIONALES")
        print("="*80)
        
        reports = {}
        
        # Generate Excel report
        reports['excel'] = self.export_to_excel()
        
        # Generate visual dashboard
        reports['dashboard'] = self.create_dashboard()
        
        print("\n" + "="*80)
        print("✅ REPORTES GENERADOS EXITOSAMENTE")
        print("="*80)
        print(f"📁 Ubicación: {self.output_dir}/")
        print(f"📊 Excel: {os.path.basename(reports['excel'])}")
        print(f"📈 Dashboard: {os.path.basename(reports['dashboard'])}")
        
        return reports


if __name__ == "__main__":
    """Generate reports when run as main script."""
    from auditor import PayrollAuditor
    
    try:
        # Run audit
        auditor = PayrollAuditor('nomina_test.csv')
        auditor.run_full_audit()
        
        # Generate reports
        reporter = PayrollReporter(auditor)
        reports = reporter.generate_full_report()
        
        print(f"\n✅ Proceso completado. Revise los archivos en la carpeta '{reporter.output_dir}/'")
        
    except Exception as e:
        print(f"❌ Error generando reportes: {str(e)}")
