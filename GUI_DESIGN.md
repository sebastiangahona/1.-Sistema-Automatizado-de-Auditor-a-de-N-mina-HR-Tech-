# 🎨 GUI Design Mockup

## Application Layout

```
╔═══════════════════════════════════════════════════════════════════════╗
║                    SISTEMA DE AUDITORÍA DE NÓMINA                     ║
╠══════════════════╦════════════════════════════════════════════════════╣
║                  ║                                                    ║
║  📊 HR Tech      ║              🚀 BIENVENIDO                        ║
║     Auditor      ║                                                    ║
║                  ║   Sistema profesional de auditoría de             ║
║  Sistema de      ║   cumplimiento laboral                            ║
║  Auditoría       ║                                                    ║
║  de Nómina       ║   ✅ Validación Código del Trabajo de Chile       ║
║                  ║   ✅ Detección de errores críticos                ║
║ ─────────────────║   ✅ Reportes ejecutivos profesionales            ║
║                  ║                                                    ║
║ 📁 Cargar        ║   Comienza cargando un archivo CSV de nómina     ║
║    Nómina        ║                                                    ║
║                  ║            ┌──────────────────────┐               ║
║ 🔍 Ejecutar      ║            │ 📁 Cargar Archivo   │               ║
║    Auditoría     ║            │    de Nómina        │               ║
║                  ║            └──────────────────────┘               ║
║ 📊 Generar       ║                                                    ║
║    Reportes      ║                                                    ║
║                  ║                                                    ║
║ ─────────────────║                                                    ║
║                  ║                                                    ║
║ 📄 Sin archivo   ║                                                    ║
║ 📋 0 registros   ║                                                    ║
║                  ║                                                    ║
║                  ║                                                    ║
║  © 2026          ║                                                    ║
║  Sebastián       ║                                                    ║
║  Gahona          ║                                                    ║
╠══════════════════╩════════════════════════════════════════════════════╣
║                        Dark Mode - BUK Blue Theme                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Audit Results Screen

```
╔═══════════════════════════════════════════════════════════════════════╗
║                    📊 RESULTADOS DE AUDITORÍA                         ║
╠══════════════════╦════════════════════════════════════════════════════╣
║  [SIDEBAR]       ║  Análisis completado • 03/02/2026 23:35           ║
║                  ║                                                    ║
║  Status:         ║  ┌──────────┐  ┌──────────┐  ┌──────────┐       ║
║  ✅ Loaded       ║  │👥 Emplead│  │⚠️ Alertas│  │💰 Impacto│       ║
║  ✅ Audited      ║  │    50    │  │    10    │  │$1,823,078│       ║
║  ✅ Ready        ║  │Total     │  │4 críticas│  │   CLP    │       ║
║                  ║  └──────────┘  └──────────┘  └──────────┘       ║
║                  ║                                                    ║
║                  ║  ┌───────────────────────────────────────────┐   ║
║                  ║  │ 📋 Distribución por Severidad             │   ║
║                  ║  │                                            │   ║
║                  ║  │ 🔴 CRÍTICA:  4 alerta(s)                  │   ║
║                  ║  │ 🟠 ALTA:     3 alerta(s)                  │   ║
║                  ║  │ 🟡 MEDIA:    3 alerta(s)                  │   ║
║                  ║  └───────────────────────────────────────────┘   ║
║                  ║                                                    ║
║                  ║  ┌───────────────────────────────────────────┐   ║
║                  ║  │ 🔍 Detalle de Alertas (10 encontradas)   │   ║
║                  ║  │                                            │   ║
║                  ║  │ ● CRÍTICA  RUT Duplicado                  │   ║
║                  ║  │ 👤 María Flores (10000633-8)              │   ║
║                  ║  │ RUT 10000633-8 aparece 2 veces con        │   ║
║                  ║  │ diferentes montos                          │   ║
║                  ║  │ 💰 Impacto: CLP $100,000                  │   ║
║                  ║  │                                            │   ║
║                  ║  │ ● CRÍTICA  Sueldo Bajo Mínimo            │   ║
║                  ║  │ 👤 Camila González (10005447-1)          │   ║
║                  ║  │ Sueldo base $305,857 está bajo el         │   ║
║                  ║  │ mínimo legal $500,000                     │   ║
║                  ║  │ 💰 Impacto: CLP $194,143                  │   ║
║                  ║  │                                            │   ║
║                  ║  │ ... y 8 alertas más                       │   ║
║                  ║  └───────────────────────────────────────────┘   ║
╚═══════════════════╩════════════════════════════════════════════════════╝
```

## Color Scheme

### Dark Mode Theme
- **Background Primary**: `#1a1a1a` (Very dark gray)
- **Background Secondary**: `#2b2b2b` (Dark gray)
- **Accent Blue (BUK)**: `#0066cc` (Primary buttons, titles)
- **Accent Green**: `#00cc66` (Success, audit button)

### Alert Colors
- **Critical** 🔴: `#ff4444` (Red - Duplicate RUT, Below minimum)
- **High** 🟠: `#ff9944` (Orange - Excessive overtime)
- **Medium** 🟡: `#ffcc44` (Yellow - Gratification over cap)
- **Success** ✅: `#44ff88` (Green - No issues)

## Interactive Elements

### Buttons
- **Primary**: Blue background, white text, hover effect
- **Success**: Green background, white text, hover effect
- **Disabled**: Gray background, gray text, no hover

### Cards
- **KPI Cards**: Rounded corners, shadow effect
- **Alert Items**: Color-coded left border matching severity
- **Info Cards**: Subtle background, no border

### Typography
- **Title**: Roboto 28pt Bold
- **Subtitle**: Roboto 12pt Regular
- **Button**: Roboto 14pt Bold
- **Body**: Roboto 11-12pt Regular
- **Monospace**: Courier 10pt (for data preview)

## User Flow

```
Start
  │
  ├─> Welcome Screen
  │     │
  │     └─> Click "Cargar Nómina"
  │           │
  │           └─> File Dialog
  │                 │
  │                 └─> File Preview Screen
  │                       │
  │                       └─> Click "Ejecutar Auditoría"
  │                             │
  │                             └─> Progress Screen
  │                                   │
  │                                   └─> Audit Results Screen
  │                                         │
  │                                         ├─> View Alerts
  │                                         │
  │                                         └─> Click "Generar Reportes"
  │                                               │
  │                                               └─> Success Dialog
  │                                                     │
  │                                                     └─> Open reports/ folder
```

## Responsive Behavior

- **Sidebar**: Fixed width 250px, always visible
- **Main Content**: Expands to fill remaining space
- **Scrollable Areas**: Audit results scroll vertically
- **Minimum Window Size**: 1200x750 pixels

## Accessibility

- High contrast colors for readability
- Large clickable areas (45px buttons)
- Clear visual hierarchy
- Status indicators with icons and text
- Progress feedback for long operations

---

**Design Philosophy**: Modern, Professional, Easy-to-Use
**Target Users**: HR Managers, Payroll Administrators, Compliance Officers
**Technology**: CustomTkinter (Modern Tkinter with theme support)
