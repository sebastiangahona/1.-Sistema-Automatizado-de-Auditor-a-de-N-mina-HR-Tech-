"""
Data Generator for Payroll Auditing System
Generates test payroll data with intentional errors for auditing purposes.

Author: Sistema de Auditoría de Nómina
Date: 2026
"""

import pandas as pd
import random
from datetime import datetime

class PayrollDataGenerator:
    """Generates payroll data with intentional errors for testing the audit system."""
    
    def __init__(self, num_employees=50):
        """
        Initialize the generator.
        
        Args:
            num_employees (int): Number of employee records to generate
        """
        self.num_employees = num_employees
        self.min_salary = 500000  # Chilean minimum wage (example)
        self.imm = 500000  # Ingreso Mínimo Mensual (example)
        
        # Common Chilean names
        self.first_names = [
            "Juan", "María", "Pedro", "Ana", "Carlos", "Sofía", "Diego", "Valentina",
            "José", "Francisca", "Luis", "Camila", "Miguel", "Javiera", "Andrés",
            "Catalina", "Jorge", "Fernanda", "Roberto", "Daniela"
        ]
        self.last_names = [
            "González", "Rodríguez", "Pérez", "Muñoz", "Díaz", "Soto", "Torres",
            "Rojas", "Silva", "Contreras", "Álvarez", "Ramírez", "Flores", "Morales"
        ]
    
    def generate_rut(self, index):
        """Generate a Chilean RUT (Rol Único Tributario)."""
        base = 10000000 + index * 1000 + random.randint(0, 999)
        # Simple verification digit calculation
        rut_str = str(base)
        return f"{rut_str}-{random.randint(0, 9)}"
    
    def generate_clean_employees(self, count):
        """Generate employees with correct payroll data."""
        employees = []
        for i in range(count):
            emp = {
                'rut': self.generate_rut(i),
                'nombre': f"{random.choice(self.first_names)} {random.choice(self.last_names)}",
                'sueldo_base': random.randint(self.min_salary, 2000000),
                'horas_extras': random.randint(0, 20),  # Safe amount
                'gratificacion': random.randint(0, int((4.75 * self.imm) / 12 - 50000)),
                'fecha_ingreso': f"2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                'cargo': random.choice(['Analista', 'Desarrollador', 'Gerente', 'Asistente', 'Coordinador'])
            }
            employees.append(emp)
        return employees
    
    def inject_errors(self, employees):
        """
        Inject intentional errors into the employee data.
        
        Errors injected:
        1. Duplicate RUT with different amounts
        2. Salary below minimum wage
        3. Excessive overtime hours
        4. Gratification exceeding legal cap
        """
        
        # Error 1: Duplicate RUT with different amounts
        if len(employees) >= 3:
            duplicate_rut = employees[0]['rut']
            employees[2]['rut'] = duplicate_rut  # Same RUT
            employees[2]['sueldo_base'] = employees[0]['sueldo_base'] + 100000  # Different salary
            employees[2]['nombre'] = employees[0]['nombre'] + " (Duplicado)"
        
        # Error 2: Salary below minimum wage (add 2-3 cases)
        for i in range(5, min(8, len(employees))):
            employees[i]['sueldo_base'] = random.randint(300000, self.min_salary - 1)
        
        # Error 3: Excessive overtime hours (more than 45 hours monthly)
        for i in range(10, min(13, len(employees))):
            employees[i]['horas_extras'] = random.randint(50, 80)  # Excessive
        
        # Error 4: Gratification exceeding legal cap (4.75 IMM annually / 12)
        max_gratification_monthly = (4.75 * self.imm) / 12
        for i in range(15, min(18, len(employees))):
            employees[i]['gratificacion'] = int(max_gratification_monthly + random.randint(10000, 100000))
        
        return employees
    
    def generate_dataset(self, output_file='nomina_test.csv'):
        """
        Generate complete payroll dataset with errors and save to CSV.
        
        Args:
            output_file (str): Output CSV filename
            
        Returns:
            pd.DataFrame: Generated payroll data
        """
        print(f"🔧 Generando datos de nómina para {self.num_employees} empleados...")
        
        # Generate clean employees
        employees = self.generate_clean_employees(self.num_employees)
        
        # Inject intentional errors
        employees = self.inject_errors(employees)
        
        # Create DataFrame
        df = pd.DataFrame(employees)
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        
        print(f"✅ Archivo generado: {output_file}")
        print(f"📊 Total empleados: {len(df)}")
        print(f"⚠️  Errores intencionales inyectados:")
        print(f"   - RUTs duplicados: 1 caso")
        print(f"   - Sueldos bajo mínimo: ~3 casos")
        print(f"   - Horas extras excesivas: ~3 casos")
        print(f"   - Gratificaciones sobre tope: ~3 casos")
        
        return df


if __name__ == "__main__":
    """Execute data generation when run as main script."""
    generator = PayrollDataGenerator(num_employees=50)
    df = generator.generate_dataset('nomina_test.csv')
    
    # Show sample data
    print("\n📋 Muestra de datos generados:")
    print(df.head(10))
    print(f"\n💾 Datos guardados en: nomina_test.csv")
