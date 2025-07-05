# 🎂 Sistema de Gestión de Cumpleaños y Mensajes Automáticos

Un sistema automatizado que lee datos de Google Sheets o PostgreSQL, calcula días para cumpleaños y envía mensajes de felicitación automáticamente a través de email y WhatsApp.

**🔄 Flexibilidad**: El sistema está diseñado para ser adaptable a otros casos de uso como:
- Recordatorios de pronto pago
- Notificaciones de vencimiento de documentos
- Alertas de mantenimiento
- Recordatorios de citas médicas
- Notificaciones de eventos
- Y cualquier otro escenario que requiera envío automático de mensajes basado en fechas

## 🚀 Características

- ✅ **Lectura automática** de Google Sheets o PostgreSQL con datos de personas
- ✅ **Cálculo inteligente** de días restantes para cumpleaños
- ✅ **Envío automático** de correos de felicitación el día del cumpleaños
- ✅ **Envío automático** de mensajes de WhatsApp el día del cumpleaños
- ✅ **Templates HTML** personalizados para correos
- ✅ **Templates de texto** para mensajes de WhatsApp
- ✅ **Bitácora automática** en Google Sheets o PostgreSQL
- ✅ **Configuración segura** con variables de entorno
- ✅ **Arquitectura modular** con procesos independientes
- ✅ **Soporte multi-canal** (Email + WhatsApp)

## 📋 Requisitos

### Software
- Python 3.7+
- Cuenta de Gmail con contraseña de aplicación
- Cuenta de servicio de Google Cloud Platform (para Google Sheets)
- Base de datos PostgreSQL (opcional)

### Librerías
```bash
pip install -r requirements.txt
```

- `gspread` - Para interactuar con Google Sheets
- `google-auth` - Para autenticación con Google
- `pandas` - Para manipulación de datos
- `psycopg2-binary` - Para conexión con PostgreSQL
- `python-dotenv` - Para variables de entorno

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
   - Colocar `cuenta_servicio.json` en la raíz del proyecto (para Google Sheets)

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Configuración de Gmail
GMAIL_USER=tu_email@gmail.com
GMAIL_APP_PASSWORD=tu_contraseña_de_aplicacion

# Configuración de WhatsApp
WHATSAPP_URL=https://tu-api-whatsapp.com/
WHATSAPP_USER=tu_usuario_whatsapp
WHATSAPP_PASS=tu_contraseña_whatsapp

# Configuración de PostgreSQL
POSTGRESQL_HOST=localhost
POSTGRESQL_BBDD=nombre_base_datos
POSTGRESQL_USER=usuario
POSTGRESQL_PASS=contraseña
POSTGRESQL_PORT=5432

# Configuración de Google Sheets (opcional)
GOOGLE_SHEETS_ID=tu_id_del_google_sheets
GOOGLE_SERVICE_ACCOUNT_FILE=cuenta_servicio.json
```

### Configuración de Gmail
- Activar verificación en 2 pasos
- Generar contraseña de aplicación
- Configurar las variables en el archivo `.env`

### Configuración de PostgreSQL (Opcional)
Ejecuta el script de esquema para crear las tablas necesarias:

```bash
psql -U tu_usuario -d tu_base_datos -f utils/postgresql/schema.sql
```

### Templates de Correo
Los templates HTML se encuentran en `utils/gmail/templates/`:
- `cumple.html` - Template de cumpleaños
- `bienvenida.html` - Template de bienvenida
- `confirmacion.html` - Template de confirmación

## 🗂️ Estructura del Proyecto

```
envio_mensaje/
├── main.py                    # Punto de entrada principal
├── processes/                 # Procesos específicos
│   ├── send_email.py         # Proceso de envío de emails
│   └── send_whatsapp.py      # Proceso de envío de WhatsApp
├── utils/                     # Utilidades y módulos
│   ├── sheets.py             # Gestión de Google Sheets
│   ├── birthday.py           # Cálculos de cumpleaños
│   ├── gmail/                # Integración con Gmail
│   │   ├── main.py           # Clase Gmail principal
│   │   └── templates/        # Templates HTML
│   ├── whatsapp/             # Integración con WhatsApp
│   │   └── main.py           # Función de envío de WhatsApp
│   ├── postgresql/           # Gestión de PostgreSQL
│   │   ├── main.py           # Clase PostgreSQLManager
│   │   └── schema.sql        # Esquema de base de datos
│   └── logger.py             # Sistema de logging
├── requirements.txt           # Dependencias
├── .env                      # Variables de entorno
├── .env_example              # Ejemplo de variables de entorno
├── cuenta_servicio.json      # Credenciales de Google (opcional)
└── logs/                     # Archivos de log
```

## 🏃‍♂️ Uso

### Ejecutar proceso de envío de emails

```bash
python main.py --process send_email
```

O de forma abreviada:

```bash
python main.py -p send_email
```

### Ejecutar proceso de envío de WhatsApp

```bash
python main.py --process send_whatsapp
```

O de forma abreviada:

```bash
python main.py -p send_whatsapp
```

### Ver ayuda

```bash
python main.py --help
```

## 📊 Fuentes de Datos

### Google Sheets
El sistema puede leer datos de Google Sheets con las siguientes columnas:
- `nombre`: Nombre de la persona
- `fecha_nacimiento`: Fecha en formato DD/MM/YYYY
- `correo`: Email de la persona
- `telefono`: Número de teléfono (para WhatsApp)

### PostgreSQL
El sistema puede leer datos de las siguientes tablas:

#### Tabla `persona`
```sql
CREATE TABLE persona (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    correo VARCHAR(255),
    telefono VARCHAR(20),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabla `bitacora`
```sql
CREATE TABLE bitacora (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    dias_para_cumple INTEGER NOT NULL,
    notificacion_enviada BOOLEAN NOT NULL,
    tipo_notificacion VARCHAR(20) DEFAULT 'whatsapp',
    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📧 Sistema de Mensajes

### Templates de Email Disponibles
- **cumple.html**: Correo de felicitación de cumpleaños
- **bienvenida.html**: Correo de bienvenida
- **confirmacion.html**: Correo de confirmación

### Templates de WhatsApp Disponibles
- **cumple**: Mensaje de felicitación de cumpleaños
- **bienvenida**: Mensaje de bienvenida
- **confirmacion**: Mensaje de confirmación

### Sintaxis de Variables
Los templates usan sintaxis `{{variable}}` para emails y `{variable}` para WhatsApp:

```html
<!-- Template de email -->
<h1>¡Feliz cumpleaños {{nombre}}!</h1>
<p>Esperamos que {{nombre}} tenga un día maravilloso.</p>
```

```text
<!-- Template de WhatsApp -->
¡Feliz cumpleaños {nombre}! 🎂🎉

Esperamos que {nombre} tenga un día maravilloso lleno de alegría y buenos momentos.
```

### Envío Automático
- **Condición**: `dias_para_cumple = 0` (día del cumpleaños)
- **Email**: Template `cumple.html` con datos personalizados
- **WhatsApp**: Template `cumple` con datos personalizados

## 🔧 Procesos Disponibles

### send_email
- Lee datos de cumpleaños desde Google Sheets o PostgreSQL
- Calcula si es el cumpleaños de hoy
- Envía emails de felicitación automáticamente
- Guarda registro en bitácora

### send_whatsapp
- Lee datos de cumpleaños desde Google Sheets o PostgreSQL
- Calcula si es el cumpleaños de hoy
- Envía mensajes de WhatsApp automáticamente
- Guarda registro en bitácora

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

### Error: "Variables de entorno no configuradas"
```bash
# Verificar archivo .env
cat .env

# Asegúrate de tener todas las variables necesarias configuradas
```

### Error: "Conexión a PostgreSQL"
- Verificar variables de entorno de PostgreSQL
- Confirmar que la base de datos existe y es accesible
- Verificar que las tablas están creadas

### Error: "Conexión a Google Sheets"
- Verificar archivo `cuenta_servicio.json`
- Confirmar que Google Sheets está compartido con cuenta de servicio
- Verificar APIs habilitadas en Google Cloud Console

### Error: "Envío de mensajes"
- Verificar credenciales en el archivo `.env`
- Confirmar contraseña de aplicación de Gmail
- Verificar configuración de WhatsApp API

## 🔄 Automatización

### Ejecutar Diariamente
Para automatizar la ejecución diaria:

**Windows (Task Scheduler)**
```cmd
C:\ruta\a\python.exe C:\ruta\a\envio_mensaje\main.py -p send_email
C:\ruta\a\python.exe C:\ruta\a\envio_mensaje\main.py -p send_whatsapp
```

**Linux/Mac (Cron)**
```bash
0 9 * * * /usr/bin/python3 /ruta/a/envio_mensaje/main.py -p send_email
0 10 * * * /usr/bin/python3 /ruta/a/envio_mensaje/main.py -p send_whatsapp
```

## 📝 Registro de Actividades

El sistema mantiene registros automáticos en:

### Google Sheets - Hoja "bitacora"
- **Fecha**: Formato YYYYMMDD
- **Nombre**: Persona procesada
- **Días**: Días restantes para cumpleaños
- **Notificación**: Si se envió mensaje

### PostgreSQL - Tabla "bitacora"
- **Fecha**: Fecha de procesamiento
- **Nombre**: Persona procesada
- **Días**: Días restantes para cumpleaños
- **Notificación**: Si se envió mensaje
- **Tipo**: Tipo de notificación (email/whatsapp)

### Archivos de Log
- **Ubicación**: `logs/envio_mensaje_YYYYMMDD.log`
- **Contenido**: Registro detallado de todas las operaciones
- **Formato**: Timestamp - Módulo - Nivel - Mensaje
- **Niveles**: INFO, WARNING, ERROR, SUCCESS

## 🔧 Personalización para Otros Casos de Uso

### Adaptar el Sistema
Para adaptar el sistema a otros casos de uso:

1. **Modificar estructura de datos**: Ajustar columnas según necesidades
2. **Crear templates**: Desarrollar templates específicos para el caso de uso
3. **Ajustar lógica de cálculo**: Modificar `BirthdayCalculator` para calcular días hasta eventos específicos
4. **Personalizar mensajes**: Adaptar contenido según el contexto

### Ejemplo: Sistema de Recordatorios de Pago
```python
# Modificar estructura de datos para incluir: cliente, fecha_vencimiento, monto
# Adaptar BirthdayCalculator para calcular días hasta vencimiento
# Crear templates recordatorio_pago.html y recordatorio_pago (WhatsApp)
# Modificar lógica de envío en los procesos
```

## 📊 Vistas Útiles (PostgreSQL)

El esquema incluye vistas para facilitar consultas:

```sql
-- Ver personas con cumpleaños próximos
SELECT * FROM v_cumpleanos_proximos;

-- Ver estadísticas de procesamiento diario
SELECT * FROM v_estadisticas_bitacora WHERE fecha = CURRENT_DATE;

-- Ver bitácora de una persona específica
SELECT * FROM bitacora WHERE nombre = 'Juan Pérez' ORDER BY fecha DESC;
```

## 🎯 Ejemplos de Uso

### Procesar cumpleaños con email
```bash
python main.py -p send_email
```

### Procesar cumpleaños con WhatsApp
```bash
python main.py -p send_whatsapp
```

### Ver ayuda del sistema
```bash
python main.py --help
```

**¡Feliz cumpleaños a todos!** 🎂

*Sistema flexible para automatizar notificaciones basadas en fechas* 📅

*Creado por la LLamaBitnaria :b*