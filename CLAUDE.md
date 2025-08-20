# Proyecto RSS Feed Generator

## Descripción
Este proyecto convierte un archivo CSV (`Todo.csv`) con contenido de blog/artículos en un feed RSS XML válido que puede ser consumido por lectores RSS y agregadores de contenido.

## Estructura del Proyecto

### Archivos principales:
- `Todo.csv` - Archivo fuente con el contenido (artículos, podcasts, metadata)
- `csv_to_rss.py` - Script principal que convierte CSV a RSS XML
- `feed.xml` - Archivo RSS generado
- `feed_config.py` - Configuración del feed (URL, título, descripción)
- `analyze_csv.py` - Script de análisis de la estructura del CSV

## Estructura del CSV

El archivo CSV contiene las siguientes columnas:
- **Slug**: Identificador único para URL
- **:draft**: Estado de borrador (true/false)
- **Título**: Título del artículo
- **Podcast**: URL del archivo de audio (opcional)
- **Episodio**: Número de episodio
- **Fecha**: Fecha de publicación (formato ISO)
- **Bajada**: Subtítulo o resumen corto
- **Meta**: Descripción meta
- **Cita 1/2**: Citas destacadas
- **Portada**: URL de imagen principal
- **Social Share**: Imagen para compartir en redes
- **Capítulo/Libro**: Categorías
- **Youtube**: Link de YouTube (opcional)
- **Original**: Contenido HTML completo del artículo

## Cómo usar

### 1. Configuración inicial
Edita el archivo `feed_config.py` con tus valores:
```python
SITE_URL = 'https://tu-sitio.com'
FEED_TITLE = 'Tu Blog'
FEED_DESCRIPTION = 'Descripción de tu feed'
CSV_FILE = 'Todo.csv'
OUTPUT_FILE = 'feed.xml'
```

### 2. Generar el RSS
```bash
python3 csv_to_rss.py
```

### 3. Actualizar el feed
Cuando actualices el CSV, simplemente vuelve a ejecutar:
```bash
python3 csv_to_rss.py
```

## Características del RSS generado

- **Formato RSS 2.0** con namespaces para contenido enriquecido
- **Límite de 50 items** más recientes (configurable)
- **Ordenado por fecha** (más reciente primero)
- **Excluye borradores** (items con :draft = true)
- **Soporte multimedia**:
  - Imágenes (portadas)
  - Podcasts (archivos de audio como enclosures)
- **Contenido completo** en `content:encoded`
- **Categorías** desde campos Capítulo y Libro

## Personalización

### Modificar el límite de items
En `csv_to_rss.py`, línea ~95:
```python
for pub_date, row in rows_with_dates[:50]:  # Cambiar 50 por el número deseado
```

### Incluir borradores
En `csv_to_rss.py`, línea ~75, comentar o modificar:
```python
# if row.get(':draft', '').lower() == 'true':
#     continue
```

### Cambiar formato de fecha
Modificar las líneas con `strftime` para ajustar el formato de fecha RSS.

## Validación del RSS

Puedes validar tu feed RSS en:
- https://validator.w3.org/feed/
- https://www.feedvalidator.org/

## Automatización (opcional)

Para actualizar automáticamente el feed cuando cambie el CSV:

### Opción 1: Cron job (Linux/Mac)
```bash
# Editar crontab
crontab -e

# Añadir línea para ejecutar cada hora
0 * * * * cd /Users/pancho/Development/RSS && python3 csv_to_rss.py
```

### Opción 2: Script watcher
Crear un script que monitoree cambios en el CSV y regenere el feed automáticamente.

## Troubleshooting

### Error de encoding
Si hay problemas con caracteres especiales, el script ya maneja UTF-8 con `errors='ignore'`.

### Fechas incorrectas
Verificar que las fechas en el CSV estén en formato ISO (YYYY-MM-DDTHH:MM:SS.sssZ).

### RSS no válido
- Revisar que las URLs de imágenes y podcasts sean válidas
- Verificar que no haya caracteres especiales no escapados en el HTML

## Notas importantes

- Los items marcados como borrador (:draft = true) NO se incluyen en el feed
- El contenido HTML se limpia automáticamente (se eliminan scripts y estilos)
- Las descripciones se truncan a 300 caracteres si son muy largas
- El feed se regenera completamente cada vez (no es incremental)