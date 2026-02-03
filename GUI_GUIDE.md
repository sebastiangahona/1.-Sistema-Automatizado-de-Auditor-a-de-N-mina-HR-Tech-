# 🖥️ GUI Application - Quick Start Guide

## 📋 Prerequisites

Before running the GUI application, ensure you have:

1. **Python 3.8+** installed
2. **Tkinter** library (usually comes with Python)
   - Windows: Included by default
   - macOS: `brew install python-tk`
   - Linux: `sudo apt-get install python3-tk`

## 🚀 Installation

```bash
# Install all dependencies
pip install -r requirements.txt
```

## 💻 Running the Application

### Option 1: Run Directly
```bash
python gui_app.py
```

### Option 2: Build Standalone .exe (Windows)
```bash
# Build executable
python build_exe.py

# The executable will be created in dist/AuditorNomina.exe
# Share this file - no Python installation needed!
```

## 🎨 Application Features

### Modern Enterprise Design
- ✨ **Dark Mode Interface**: Professional appearance with BUK Blue accents
- 📱 **Responsive Layout**: Side navigation with expandable content area
- 🎯 **Intuitive Workflow**: Load → Audit → Report

### Main Screens

#### 1. Welcome Screen
- Initial landing page with quick start guide
- Direct access to file upload

#### 2. File Preview
- Shows loaded data summary
- Displays column information
- Preview of first 10 rows

#### 3. Audit Results
- **KPI Cards**: Total employees, alerts count, financial impact
- **Severity Distribution**: Visual breakdown by critical/high/medium
- **Detailed Alerts**: Scrollable list with all findings
- **Color Coding**:
  - 🔴 Red: Critical issues (duplicate RUT, below minimum salary)
  - 🟠 Orange: High severity (excessive overtime)
  - 🟡 Yellow: Medium severity (gratification over cap)

#### 4. Report Generation
- One-click Excel and Dashboard generation
- Files saved to `reports/` directory

## 🎯 Usage Workflow

1. **Launch Application**
   ```bash
   python gui_app.py
   ```

2. **Load Payroll File**
   - Click "📁 Cargar Nómina" 
   - Select your CSV file
   - Review the preview

3. **Execute Audit**
   - Click "🔍 Ejecutar Auditoría"
   - Wait for analysis (typically 2-5 seconds)
   - Review results

4. **Generate Reports**
   - Click "📊 Generar Reportes"
   - Find reports in `reports/` folder

## 📊 Expected CSV Format

Your payroll CSV should have these columns:
```csv
rut,nombre,sueldo_base,horas_extras,gratificacion,fecha_ingreso,cargo
10000001-1,Juan Pérez,600000,10,50000,2023-01-15,Analista
```

Required columns:
- `rut`: Chilean ID (format: 12345678-9)
- `nombre`: Employee name
- `sueldo_base`: Base salary in CLP
- `horas_extras`: Monthly overtime hours
- `gratificacion`: Monthly gratification in CLP
- `fecha_ingreso`: Hire date (YYYY-MM-DD)
- `cargo`: Job title

## 🔧 Troubleshooting

### "No module named 'tkinter'"
**Solution**: Install tkinter for your OS
- Ubuntu/Debian: `sudo apt-get install python3-tk`
- Fedora: `sudo dnf install python3-tkinter`
- macOS: `brew install python-tk`

### "No module named 'customtkinter'"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Application won't start
**Solution**: Verify Python version
```bash
python --version  # Should be 3.8 or higher
```

## 🏗️ Building Executable

To create a standalone .exe file that can run without Python:

```bash
# Install PyInstaller
pip install pyinstaller

# Run build script
python build_exe.py

# Result: dist/AuditorNomina.exe (~50-80 MB)
```

The executable includes:
- Python interpreter
- All dependencies (Pandas, CustomTkinter, etc.)
- Your application code
- No external installations needed!

### Build Options

Edit `build_exe.py` to customize:
- **Icon**: Place custom `icon.ico` in `assets/`
- **Name**: Change `--name=AuditorNomina`
- **Console**: Remove `--windowed` to show console

## 📸 Screenshots

See `/docs/screenshots/` folder for visual examples:
- Welcome screen
- File preview
- Audit results with KPI cards
- Alert details view

## 🎯 Keyboard Shortcuts

- **Ctrl+O**: Open file dialog (when implemented)
- **Ctrl+Q**: Quit application (when implemented)
- **F5**: Refresh view (when implemented)

## 💡 Tips

1. **Test Data**: Use `python generator.py` to create sample data
2. **Reports**: Reports auto-save to `reports/` folder
3. **Performance**: Handles up to 10,000 employees smoothly
4. **Updates**: Pull latest code for new features

## 📞 Support

For issues or questions:
- Check README.md for detailed documentation
- Review troubleshooting section above
- Create an issue on GitHub

---

**Version**: 1.0  
**Last Updated**: 2026-02-03  
**Author**: Sistema de Auditoría de Nómina
