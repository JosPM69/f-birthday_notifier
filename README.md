# 🎂 Sistema de Envío de Mensajes de Cumpleaños

Un sistema automatizado que lee datos de Google Sheets, calcula días para cumpleaños y envía correos de felicitación automáticamente usando Gmail.

**📊 Google Sheets de Ejemplo**: Este proyecto utiliza como referencia el Google Sheets: [https://docs.google.com/spreadsheets/d/1f3ZZUO9NQ7PS1_6Od6DhOIR9hBaXzFTiI532aEefimI/edit?usp=sharing](https://docs.google.com/spreadsheets/d/1f3ZZUO9NQ7PS1_6Od6DhOIR9hBaXzFTiI532aEefimI/edit?usp=sharing)

**🔄 Flexibilidad**: El sistema está diseñado para ser adaptable a otros casos de uso como:
- Recordatorios de pronto pago
- Notificaciones de vencimiento de documentos
- Alertas de mantenimiento
- Recordatorios de citas médicas
- Notificaciones de eventos
- Y cualquier otro escenario que requiera envío automático de correos basado en fechas

## 🚀 Características

- ✅ **Lectura automática** de Google Sheets con datos de personas
- ✅ **Cálculo inteligente** de días restantes para cumpleaños
- ✅ **Envío automático** de correos de felicitación el día del cumpleaños
- ✅ **Templates HTML** personalizados para correos
- ✅ **Bitácora automática** en Google Sheets
- ✅ **Configuración segura** con cuenta de servicio y variables de entorno

## 📋 Requisitos

### Software
- Python 3.7+
- Cuenta de Gmail con contraseña de aplicación
- Cuenta de servicio de Google Cloud Platform

### Librerías
```bash
pip install -r requirements.txt
```

- `gspread` - Para interactuar con Google Sheets
- `google-auth` - Para autenticación con Google
- `pandas` - Para manipulación de datos

## 🛠️ Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/JosPM69/f-birthday_notifier.git
cd envio_mensaje
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
   - Copiar `.env_example` a `.env`
   - Configurar credenciales en el archivo `.env`
   - Colocar `cuenta_servicio.json` en la raíz del proyecto

## ⚙️ Configuración

### 1. Google Sheets
- **Ejemplo de referencia**: [Google Sheets de ejemplo](https://docs.google.com/spreadsheets/d/1f3ZZUO9NQ7PS1_6Od6DhOIR9hBaXzFTiI532aEefimI/edit?usp=sharing)
- Crear o usar un Google Sheets con las columnas:
  - `nombre`: Nombre de la persona
  - `fecha_nacimiento`: Fecha en formato DD/MM/YYYY
  - `correo`: Email de la persona
- Compartir el Google Sheets con el email de la cuenta de servicio
- **Nota**: Puedes adaptar las columnas según tu caso de uso específico

### 2. Cuenta de Servicio (Google Cloud)
- Crear cuenta de servicio en Google Cloud Console
- Habilitar APIs: Google Sheets API y Google Drive API
- Descargar archivo JSON de credenciales como `cuenta_servicio.json`

### 3. Variables de Entorno
Crear archivo `.env` en la raíz del proyecto:
```bash
# Configuración de Gmail
GMAIL_USER=tu_email@gmail.com
GMAIL_APP_PASSWORD=tu_contraseña_de_aplicacion

# Configuración de Google Sheets
GOOGLE_SHEETS_ID=tu_id_del_google_sheets
GOOGLE_SERVICE_ACCOUNT_FILE=cuenta_servicio.json
```

Para Gmail:
- Activar verificación en 2 pasos
- Generar contraseña de aplicación
- Configurar las variables en el archivo `.env`

### 4. Templates de Correo
Los templates HTML se encuentran en `utils/gmail/templates/`:
- `cumple.html` - Template de cumpleaños
- `bienvenida.html` - Template de bienvenida
- `confirmacion.html` - Template de confirmación

## 🗂️ Estructura del Proyecto

```
envio_mensaje/
├── README.md                 # Documentación del proyecto
├── run.py                    # Script principal (modularizado)
├── requirements.txt          # Dependencias
├── .env                      # Variables de entorno (no versionar)
├── .env_example              # Ejemplo de variables de entorno
├── cuenta_servicio.json      # Credenciales de Google (no versionar)
├── guia.txt                  # Guía adicional
├── logs/                     # Archivos de log (generados automáticamente)
├── utils/                    # Módulos utilitarios
│   ├── logger.py            # Sistema de logging centralizado
│   ├── sheets/              # Módulo Google Sheets
│   │   ├── __init__.py
│   │   └── google_sheets.py # GoogleSheetsManager
│   ├── birthday/            # Módulo cálculos de cumpleaños
│   │   ├── __init__.py
│   │   └── birthday_calculator.py # BirthdayCalculator
│   └── gmail/               # Módulo Gmail
│       ├── main.py          # Clase Gmail principal
│       ├── config.py        # Configuración Gmail
│       └── templates/       # Templates HTML
│           └── cumple.html  # Template de cumpleaños
└── venv/                    # Entorno virtual
```

### 📦 Módulos

#### `utils/logger.py` - Sistema de Logging
- **Logger**: Clase centralizada para logging profesional
- Funciones: `info()`, `debug()`, `warning()`, `error()`, `success()`, `failure()`
- Logs en archivo (`logs/envio_mensaje_YYYYMMDD.log`) y consola

#### `utils/sheets/` - Gestión de Google Sheets
- **GoogleSheetsManager**: Clase principal para manejar operaciones con Google Sheets
- Funciones: conectar, leer datos, escribir bitácora, gestionar hojas
- Configuración mediante variables de entorno

#### `utils/birthday/` - Cálculos de Cumpleaños  
- **BirthdayCalculator**: Clase para cálculos relacionados con cumpleaños
- Funciones: calcular días, generar mensajes, obtener edad, cumpleaños próximos

#### `utils/gmail/` - Envío de Correos
- **Gmail**: Clase para envío de correos con templates
- Templates HTML personalizados con sintaxis `{{variable}}`
- Configuración mediante variables de entorno

## 🏃‍♂️ Uso

### Ejecución Principal
```bash
python run.py
```

### Casos de Uso Adicionales

El sistema puede adaptarse fácilmente para otros escenarios:

#### 📧 Recordatorios de Pronto Pago
```python
# Adaptar columnas: cliente, fecha_vencimiento, correo
# Modificar lógica para calcular días hasta vencimiento
# Usar template de recordatorio de pago
```

#### 📋 Notificaciones de Vencimiento
```python
# Adaptar columnas: documento, fecha_vencimiento, responsable
# Calcular días restantes para renovación
# Enviar alertas de vencimiento
```

#### 🏥 Recordatorios Médicos
```python
# Adaptar columnas: paciente, fecha_cita, correo
# Calcular días hasta la próxima cita
# Enviar recordatorios personalizados
```

### Arquitectura Modularizada
El sistema utiliza una arquitectura modular que separa responsabilidades:

```python
# Ejemplo de uso de los módulos
from utils.sheets import GoogleSheetsManager
from utils.birthday import BirthdayCalculator
from utils.gmail.main import Gmail
from utils.logger import logger

# Gestión de Google Sheets
sheets_manager = GoogleSheetsManager()
sheets_manager.connect()
df = sheets_manager.read_main_sheet()

# Cálculos de cumpleaños
birthday_info = BirthdayCalculator.get_birthday_info("Juan", "15/01/1990")
logger.info(birthday_info['mensaje'])

# Envío de correos
gmail = Gmail("tu_email@gmail.com", "tu_app_password")
gmail.send_email("destino@gmail.com", "cumple", {"nombre": "Juan"})
```

### Flujo de Trabajo
1. **Conecta** con Google Sheets usando GoogleSheetsManager
2. **Lee** datos de la hoja principal (nombres, fechas, correos)
3. **Calcula** días restantes usando BirthdayCalculator
4. **Envía correo** automáticamente si es el cumpleaños (días = 0)
5. **Guarda** registro en hoja "bitacora" con formato:
   - `fecha` (YYYYMMDD)
   - `nombre`
   - `dias_para_cumple`
   - `correo_enviado` (SI/NO)

### Ejemplo de Salida
```
2025-01-15 14:30:25 - envio_mensaje - INFO - Iniciando sistema de cumpleaños modularizado
2025-01-15 14:30:26 - envio_mensaje - INFO - SUCCESS: Conexión exitosa con Google Sheets
2025-01-15 14:30:27 - envio_mensaje - INFO - Abriendo Google Sheets: [ID_SHEET]
2025-01-15 14:30:28 - envio_mensaje - INFO - Hoja seleccionada: Hoja 1
2025-01-15 14:30:29 - envio_mensaje - INFO - Obteniendo datos
2025-01-15 14:30:30 - envio_mensaje - INFO - SUCCESS: Datos obtenidos exitosamente
2025-01-15 14:30:31 - envio_mensaje - INFO - Dimensiones: 1 filas x 3 columnas

2025-01-15 14:30:32 - envio_mensaje - INFO - Procesando: CARLOS
2025-01-15 14:30:33 - envio_mensaje - INFO - Fecha de nacimiento: 06/07/2025
2025-01-15 14:30:34 - envio_mensaje - INFO - Correo: llamabitnaria@gmail.com
2025-01-15 14:30:35 - envio_mensaje - INFO - Días para cumpleaños: 172
2025-01-15 14:30:36 - envio_mensaje - INFO - Edad actual: -1 años
2025-01-15 14:30:37 - envio_mensaje - INFO - Faltan 172 días para el cumpleaños de CARLOS
2025-01-15 14:30:38 - envio_mensaje - INFO - Guardando en bitácora
2025-01-15 14:30:39 - envio_mensaje - INFO - SUCCESS: Datos guardados exitosamente en bitácora

2025-01-15 14:30:40 - envio_mensaje - INFO - RESUMEN DE PROCESAMIENTO
2025-01-15 14:30:41 - envio_mensaje - INFO - Personas procesadas: 1
2025-01-15 14:30:42 - envio_mensaje - INFO - Correos enviados: 0
2025-01-15 14:30:43 - envio_mensaje - INFO - Gmail configurado: llamabitnaria@gmail.com
2025-01-15 14:30:44 - envio_mensaje - INFO - SUCCESS: Proceso completado exitosamente
```

**Nota**: Los logs también se guardan en `logs/envio_mensaje_YYYYMMDD.log` para auditoría y debugging.

## 📊 Google Sheets - Estructura de Datos

### Hoja Principal (Ejemplo de Cumpleaños)
| nombre | fecha_nacimiento | correo |
|--------|------------------|---------|
| CARLOS | 06/07/2025 | llamabitnaria@gmail.com |
| MARIA | 15/12/1990 | maria@example.com |

### Ejemplos de Estructura para Otros Casos de Uso

#### 📧 Recordatorios de Pago
| cliente | fecha_vencimiento | correo | monto |
|---------|-------------------|---------|-------|
| Empresa ABC | 15/02/2025 | abc@empresa.com | $1,500 |
| Cliente XYZ | 20/02/2025 | xyz@cliente.com | $800 |

#### 📋 Vencimiento de Documentos
| documento | fecha_vencimiento | responsable | correo |
|-----------|-------------------|-------------|---------|
| Licencia Comercial | 30/03/2025 | Juan Pérez | juan@empresa.com |
| Certificado ISO | 15/04/2025 | María López | maria@empresa.com |

#### 🏥 Citas Médicas
| paciente | fecha_cita | especialidad | correo |
|----------|------------|--------------|---------|
| Ana García | 25/02/2025 | Cardiología | ana@email.com |
| Carlos Ruiz | 28/02/2025 | Dermatología | carlos@email.com |

### Hoja "bitacora" (Creada automáticamente)
| fecha | nombre | dias_para_cumple | correo_enviado |
|-------|--------|------------------|----------------|
| 20250115 | CARLOS | 172 | NO |
| 20250706 | CARLOS | 0 | SI |

## 📧 Sistema de Correos

### Templates Disponibles
- **cumple.html**: Correo de felicitación de cumpleaños
- **bienvenida.html**: Correo de bienvenida
- **confirmacion.html**: Correo de confirmación

### Templates Adicionales (Crear según necesidad)
- **recordatorio_pago.html**: Recordatorio de pronto pago
- **vencimiento_documento.html**: Alerta de vencimiento
- **recordatorio_cita.html**: Recordatorio de cita médica
- **evento_proximo.html**: Notificación de evento próximo

### Sintaxis de Variables
Los templates usan sintaxis `{{variable}}`:
```html
<!-- Ejemplo cumpleaños -->
<h1>¡Feliz cumpleaños {{nombre}}!</h1>
<p>Esperamos que {{nombre}} tenga un día maravilloso.</p>

<!-- Ejemplo recordatorio de pago -->
<h1>Recordatorio de Pago - {{cliente}}</h1>
<p>Estimado {{cliente}}, su factura por {{monto}} vence el {{fecha_vencimiento}}.</p>

<!-- Ejemplo vencimiento documento -->
<h1>Vencimiento de {{documento}}</h1>
<p>Estimado {{responsable}}, el documento {{documento}} vence el {{fecha_vencimiento}}.</p>
```

### Envío Automático
- **Condición**: `dias_para_cumple = 0` (o días hasta evento = 0)
- **Template**: `cumple.html` (o template específico según caso de uso)
- **Datos**: `{"nombre": "NOMBRE_PERSONA"}` (o variables específicas del caso de uso)

## 🔐 Seguridad

### Archivos Sensibles (No versionar)
- `cuenta_servicio.json` - Credenciales de Google
- `.env` - Variables de entorno con credenciales
- `logs/` - Archivos de log (pueden contener información sensible)

### Buenas Prácticas
- Usar contraseñas de aplicación para Gmail
- Mantener credenciales en variables de entorno
- Revisar permisos de cuenta de servicio
- Usar principio de menor privilegio
- Revisar logs regularmente para detectar problemas

## 🚨 Solución de Problemas

### Error: "No module named 'gmail'"
```bash
# Verificar que existe el archivo
ls utils/gmail/gmail.py

# Si no existe, renombrar
mv utils/gmail/main.py utils/gmail/gmail.py
```

### Error: "Template no encontrado"
```bash
# Verificar templates
ls utils/gmail/templates/
# Debe contener: cumple.html, bienvenida.html, confirmacion.html
```

### Error: "Conexión a Google Sheets"
- Verificar archivo `cuenta_servicio.json`
- Confirmar que Google Sheets está compartido con cuenta de servicio
- Verificar APIs habilitadas en Google Cloud Console

### Error: "Envío de correo"
- Verificar credenciales en el archivo `.env`
- Confirmar contraseña de aplicación de Gmail
- Verificar que la verificación en 2 pasos está activada
- Revisar logs en `logs/envio_mensaje_YYYYMMDD.log` para detalles del error

## 🔄 Automatización

### Ejecutar Diariamente
Para automatizar la ejecución diaria:

**Windows (Task Scheduler)**
```cmd
C:\ruta\a\python.exe C:\ruta\a\envio_mensaje\run.py
```

**Linux/Mac (Cron)**
```bash
0 9 * * * /usr/bin/python3 /ruta/a/envio_mensaje/run.py
```

## 📝 Registro de Actividades

El sistema mantiene registros automáticos en dos lugares:

### Google Sheets - Hoja "bitacora"
- **Fecha**: Formato YYYYMMDD
- **Nombre**: Persona procesada
- **Días**: Días restantes para cumpleaños
- **Correo**: Si se envió correo de cumpleaños

### Archivos de Log
- **Ubicación**: `logs/envio_mensaje_YYYYMMDD.log`
- **Contenido**: Registro detallado de todas las operaciones
- **Formato**: Timestamp - Módulo - Nivel - Mensaje
- **Niveles**: INFO, WARNING, ERROR, SUCCESS

## 🔧 Personalización para Otros Casos de Uso

### Adaptar el Sistema
Para adaptar el sistema a otros casos de uso:

1. **Modificar estructura de datos**: Ajustar columnas en Google Sheets según necesidades
2. **Crear templates HTML**: Desarrollar templates específicos para el caso de uso
3. **Ajustar lógica de cálculo**: Modificar `BirthdayCalculator` para calcular días hasta eventos específicos
4. **Personalizar mensajes**: Adaptar contenido de correos según el contexto

### Ejemplo: Sistema de Recordatorios de Pago
```python
# Modificar GoogleSheetsManager para leer columnas específicas
# Adaptar BirthdayCalculator para calcular días hasta vencimiento
# Crear template recordatorio_pago.html
# Modificar lógica de envío en run.py
```

**¡Feliz cumpleaños a todos!** 🎂

*Sistema flexible para automatizar notificaciones basadas en fechas* 📅

*Creado por la LLamaBitnaria :b*
