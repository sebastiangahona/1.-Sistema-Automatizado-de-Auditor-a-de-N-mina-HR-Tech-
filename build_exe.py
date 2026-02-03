#!/usr/bin/env python3
"""
Build Script for Payroll Auditing System
Creates standalone .exe using PyInstaller

Usage:
    python build_exe.py

Output:
    dist/AuditorNomina.exe - Standalone executable
"""

import os
import sys
import subprocess
import shutil

def create_icon():
    """Create a simple icon file if it doesn't exist."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a 256x256 icon with blue background
        img = Image.new('RGB', (256, 256), color='#0066cc')
        draw = ImageDraw.Draw(img)
        
        # Draw a simple chart icon
        draw.rectangle([60, 180, 80, 220], fill='white')
        draw.rectangle([100, 150, 120, 220], fill='white')
        draw.rectangle([140, 120, 160, 220], fill='white')
        draw.rectangle([180, 90, 200, 220], fill='white')
        
        # Save as ICO
        img.save('assets/icon.ico', format='ICO', sizes=[(256, 256)])
        print("✅ Icon created: assets/icon.ico")
        return True
        
    except Exception as e:
        print(f"⚠️  Could not create icon: {e}")
        return False

def build_exe():
    """Build the executable using PyInstaller."""
    
    print("\n" + "="*70)
    print("🔧 CONSTRUCCIÓN DE EJECUTABLE")
    print("="*70 + "\n")
    
    # Ensure assets directory exists
    if not os.path.exists('assets'):
        os.makedirs('assets')
        print("📁 Created assets directory")
    
    # Create icon if it doesn't exist
    icon_path = 'assets/icon.ico'
    if not os.path.exists(icon_path):
        print("🎨 Creating application icon...")
        create_icon()
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--name=AuditorNomina',
        '--onefile',
        '--windowed',  # No console window
        '--clean',
        '--noconfirm',
    ]
    
    # Add icon if it exists
    if os.path.exists(icon_path):
        cmd.append(f'--icon={icon_path}')
    
    # Add hidden imports for dependencies
    hidden_imports = [
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'openpyxl',
        'xlsxwriter',
        'customtkinter',
        'PIL',
        'tkinter'
    ]
    
    for module in hidden_imports:
        cmd.extend(['--hidden-import', module])
    
    # Add the main script
    cmd.append('gui_app.py')
    
    print("🔨 Ejecutando PyInstaller...")
    print(f"Comando: {' '.join(cmd)}\n")
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("\n" + "="*70)
        print("✅ CONSTRUCCIÓN EXITOSA")
        print("="*70)
        print(f"\n📦 Ejecutable creado: dist/AuditorNomina.exe")
        print(f"📁 Tamaño: {os.path.getsize('dist/AuditorNomina.exe') / (1024*1024):.1f} MB")
        print("\n💡 Puedes compartir este archivo sin necesidad de Python instalado")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print("\n" + "="*70)
        print("❌ ERROR EN LA CONSTRUCCIÓN")
        print("="*70)
        print(f"\n{e.stderr}")
        return False
    
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False

def clean_build_files():
    """Clean up build artifacts."""
    
    print("\n🧹 Limpiando archivos de construcción...")
    
    dirs_to_remove = ['build', '__pycache__']
    files_to_remove = ['AuditorNomina.spec']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Eliminado: {dir_name}/")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"   Eliminado: {file_name}")

def main():
    """Main build process."""
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller no está instalado")
        print("💡 Instala con: pip install pyinstaller")
        sys.exit(1)
    
    # Check if we're in the right directory
    if not os.path.exists('gui_app.py'):
        print("❌ Error: gui_app.py no encontrado")
        print("💡 Ejecuta este script desde el directorio raíz del proyecto")
        sys.exit(1)
    
    # Build executable
    success = build_exe()
    
    # Clean up
    clean_build_files()
    
    if success:
        print("\n✨ ¡Listo! Tu aplicación está empaquetada y lista para distribuir")
        sys.exit(0)
    else:
        print("\n💔 La construcción falló. Revisa los errores arriba.")
        sys.exit(1)

if __name__ == "__main__":
    main()
