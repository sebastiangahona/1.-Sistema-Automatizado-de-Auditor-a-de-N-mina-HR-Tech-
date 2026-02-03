"""
Payroll Auditor - Core Business Logic
Implements Chilean labor law compliance checks for payroll data.

Validates:
- Legal minimum salary compliance (Código del Trabajo, Art. 41)
- Overtime hours limits (Código del Trabajo, Art. 31-32)
- Gratification legal caps (Código del Trabajo, Art. 47)
- Duplicate employee records (RUT validation)

Author: Sistema de Auditoría de Nómina
Date: 2026
"""

import pandas as pd
from typing import List, Dict, Tuple
from datetime import datetime


class PayrollAuditor:
    """
    Main auditor class for payroll compliance validation.
    
    Attributes:
        df (pd.DataFrame): Payroll data to audit
        alerts (List[Dict]): List of detected compliance issues
        min_salary (int): Legal minimum salary in CLP
        imm (int): Ingreso Mínimo Mensual for gratification calculations
    """
    
    def __init__(self, file_path: str, min_salary: int = 500000, imm: int = 500000):
        """
        Initialize the auditor with payroll data.
        
        Args:
            file_path (str): Path to CSV file with payroll data
            min_salary (int): Legal minimum salary in CLP (default: 500,000)
            imm (int): Ingreso Mínimo Mensual (default: 500,000)
        """
        try:
            self.df = pd.read_csv(file_path)
            self.alerts = []
            self.min_salary = min_salary
            self.imm = imm
            print(f"✅ Archivo cargado: {len(self.df)} registros encontrados")
        except FileNotFoundError:
            raise FileNotFoundError(f"❌ Error: No se encontró el archivo {file_path}")
        except Exception as e:
            raise Exception(f"❌ Error al cargar archivo: {str(e)}")
    
    def check_legal_minimum(self) -> pd.DataFrame:
        """
        Validate compliance with minimum wage law.
        
        Legal basis: Código del Trabajo de Chile, Art. 41
        
        Returns:
            pd.DataFrame: Employees with salary below legal minimum
        """
        print(f"\n🔍 Verificando sueldo mínimo legal (CLP ${self.min_salary:,})...")
        
        under_min = self.df[self.df['sueldo_base'] < self.min_salary].copy()
        
        if len(under_min) > 0:
            for _, row in under_min.iterrows():
                alert = {
                    'tipo': 'SUELDO_BAJO_MINIMO',
                    'severidad': 'CRÍTICA',
                    'rut': row['rut'],
                    'nombre': row['nombre'],
                    'detalle': f"Sueldo base ${row['sueldo_base']:,.0f} está bajo el mínimo legal ${self.min_salary:,}",
                    'impacto_financiero': self.min_salary - row['sueldo_base'],
                    'articulo_legal': 'Código del Trabajo, Art. 41'
                }
                self.alerts.append(alert)
            
            print(f"⚠️  {len(under_min)} empleado(s) con sueldo bajo el mínimo legal")
        else:
            print(f"✅ Todos los sueldos cumplen con el mínimo legal")
        
        return under_min
    
    def check_overtime_limit(self) -> pd.DataFrame:
        """
        Validate overtime hours within legal limits.
        
        Legal basis: Código del Trabajo de Chile, Art. 31-32
        - Maximum 2 hours extra per day
        - Maximum 12 hours extra per week
        - Approximately 45-50 hours per month
        
        Returns:
            pd.DataFrame: Employees with excessive overtime hours
        """
        print(f"\n🔍 Verificando límites de horas extras...")
        
        # Monthly limit approximation: 2 hours/day * 5 days/week * 4.5 weeks ≈ 45 hours
        monthly_limit = 45
        excessive_ot = self.df[self.df['horas_extras'] > monthly_limit].copy()
        
        if len(excessive_ot) > 0:
            for _, row in excessive_ot.iterrows():
                alert = {
                    'tipo': 'HORAS_EXTRAS_EXCESIVAS',
                    'severidad': 'ALTA',
                    'rut': row['rut'],
                    'nombre': row['nombre'],
                    'detalle': f"Horas extras: {row['horas_extras']} horas exceden límite mensual de {monthly_limit} horas",
                    'impacto_financiero': 0,  # Potential legal fines, not directly calculable
                    'articulo_legal': 'Código del Trabajo, Art. 31-32'
                }
                self.alerts.append(alert)
            
            print(f"⚠️  {len(excessive_ot)} empleado(s) con horas extras excesivas")
        else:
            print(f"✅ Todas las horas extras están dentro de los límites legales")
        
        return excessive_ot
    
    def validate_gratification(self) -> pd.DataFrame:
        """
        Verify gratification payments comply with legal cap.
        
        Legal basis: Código del Trabajo de Chile, Art. 47
        Maximum annual gratification: 4.75 IMM
        Maximum monthly gratification: (4.75 * IMM) / 12
        
        Returns:
            pd.DataFrame: Employees with gratification exceeding legal cap
        """
        print(f"\n🔍 Verificando topes de gratificación...")
        
        tope_anual = 4.75 * self.imm
        tope_mensual = tope_anual / 12
        
        over_limit = self.df[self.df['gratificacion'] > (tope_mensual + 1)].copy()
        
        if len(over_limit) > 0:
            for _, row in over_limit.iterrows():
                exceso = row['gratificacion'] - tope_mensual
                alert = {
                    'tipo': 'GRATIFICACION_SOBRE_TOPE',
                    'severidad': 'MEDIA',
                    'rut': row['rut'],
                    'nombre': row['nombre'],
                    'detalle': f"Gratificación ${row['gratificacion']:,.0f} excede tope legal ${tope_mensual:,.0f}",
                    'impacto_financiero': exceso,
                    'articulo_legal': 'Código del Trabajo, Art. 47'
                }
                self.alerts.append(alert)
            
            print(f"⚠️  {len(over_limit)} empleado(s) con gratificación sobre el tope legal")
        else:
            print(f"✅ Todas las gratificaciones están dentro del tope legal")
        
        return over_limit
    
    def check_duplicate_rut(self) -> pd.DataFrame:
        """
        Detect duplicate employee records (same RUT).
        
        Returns:
            pd.DataFrame: Employees with duplicate RUT numbers
        """
        print(f"\n🔍 Verificando RUTs duplicados...")
        
        duplicates = self.df[self.df.duplicated(subset=['rut'], keep=False)].copy()
        
        if len(duplicates) > 0:
            # Group by RUT to show all instances
            for rut in duplicates['rut'].unique():
                rut_records = self.df[self.df['rut'] == rut]
                if len(rut_records) > 1:
                    alert = {
                        'tipo': 'RUT_DUPLICADO',
                        'severidad': 'CRÍTICA',
                        'rut': rut,
                        'nombre': 'Múltiples registros',
                        'detalle': f"RUT {rut} aparece {len(rut_records)} veces con diferentes montos",
                        'impacto_financiero': rut_records['sueldo_base'].sum() - rut_records['sueldo_base'].min(),
                        'articulo_legal': 'Integridad de datos'
                    }
                    self.alerts.append(alert)
            
            print(f"⚠️  {len(duplicates['rut'].unique())} RUT(s) duplicado(s) detectado(s)")
        else:
            print(f"✅ No se encontraron RUTs duplicados")
        
        return duplicates
    
    def run_full_audit(self) -> Tuple[int, float]:
        """
        Execute complete audit process with all validations.
        
        Returns:
            Tuple[int, float]: (total_alerts, total_financial_impact)
        """
        print("\n" + "="*80)
        print("🚀 INICIANDO AUDITORÍA COMPLETA DE NÓMINA")
        print("="*80)
        
        # Run all checks
        self.check_duplicate_rut()
        self.check_legal_minimum()
        self.check_overtime_limit()
        self.validate_gratification()
        
        # Calculate total financial impact
        total_impact = sum(alert['impacto_financiero'] for alert in self.alerts)
        
        # Summary
        print("\n" + "="*80)
        print("📊 RESUMEN DE AUDITORÍA")
        print("="*80)
        print(f"Total de empleados auditados: {len(self.df)}")
        print(f"Total de alertas detectadas: {len(self.alerts)}")
        print(f"Impacto financiero total: CLP ${total_impact:,.0f}")
        
        # Count by severity
        critical = sum(1 for a in self.alerts if a['severidad'] == 'CRÍTICA')
        high = sum(1 for a in self.alerts if a['severidad'] == 'ALTA')
        medium = sum(1 for a in self.alerts if a['severidad'] == 'MEDIA')
        
        print(f"\nPor severidad:")
        print(f"  🔴 Crítica: {critical}")
        print(f"  🟠 Alta: {high}")
        print(f"  🟡 Media: {medium}")
        
        return len(self.alerts), total_impact
    
    def get_alerts_dataframe(self) -> pd.DataFrame:
        """
        Get all alerts as a pandas DataFrame.
        
        Returns:
            pd.DataFrame: All detected alerts in tabular format
        """
        if not self.alerts:
            return pd.DataFrame()
        
        return pd.DataFrame(self.alerts)


if __name__ == "__main__":
    """Execute audit when run as main script."""
    try:
        # Create auditor instance
        auditor = PayrollAuditor('nomina_test.csv')
        
        # Run full audit
        total_alerts, financial_impact = auditor.run_full_audit()
        
        # Display alerts
        if total_alerts > 0:
            print("\n📋 DETALLE DE ALERTAS:")
            alerts_df = auditor.get_alerts_dataframe()
            print(alerts_df[['tipo', 'severidad', 'nombre', 'detalle']].to_string(index=False))
        
    except Exception as e:
        print(f"❌ Error durante la auditoría: {str(e)}")
