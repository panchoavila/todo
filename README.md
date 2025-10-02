# ATLAS DE TODO - RSS Feed

Hackea el antropoceno; contempla el fin de los tiempos.

## 📡 Suscribirse al Feed

**RSS Feed**: https://panchoavila.github.io/RSS/feed.xml  
**Página web**: https://panchoavila.github.io/RSS/

### Cómo suscribirse:
1. Copia la URL del feed
2. Pégala en tu lector RSS favorito (Feedly, Inoreader, etc.)
3. ¡Listo! Recibirás las actualizaciones automáticamente

## 🛠 Estructura del Proyecto

```
RSS/
├── csv_to_rss.py      # Script principal para generar RSS
├── analyze_csv.py     # Analizador de estructura CSV
├── feed_config.py     # Configuración del feed
├── update_feed.sh     # Script para actualizar y publicar
├── feed.xml          # RSS generado (no editar manualmente)
├── index.html        # Página web del feed
└── Todo.csv          # Datos fuente (privado, no en git)
```

## 📝 Uso

### Generar/actualizar el feed:
```bash
python3 csv_to_rss.py
```

### Actualizar y publicar en GitHub:
```bash
./update_feed.sh
```

## 📊 Formato del CSV

El CSV debe tener las siguientes columnas:
- `Slug`: ID único para URLs
- `Título`: Título del artículo
- `Fecha`: Fecha ISO (YYYY-MM-DDTHH:MM:SS.sssZ)
- `Bajada`: Descripción corta
- `Original`: Contenido HTML completo
- `Portada`: URL de imagen
- `Podcast`: URL de audio (opcional)
- Y más campos opcionales...

## 🔁 Patrón de actualización (Fecha y Slug)

Para facilitar identificar qué contenido es el más reciente en el feed y en los lectores RSS, sigue este patrón sencillo:

- Usa `Fecha` como “última actualización”. Al editar un ítem existente, actualiza `Fecha` al momento de la edición en formato ISO 8601 (ej.: `2025-09-30T18:42:00Z`). El feed se ordena por `Fecha` (más reciente primero).
- Mantén `Slug` estable para correcciones menores o ajustes de contenido: el GUID del RSS es la URL (`SITE_URL/Slug`). Muchos lectores mostrarán el ítem con su `pubDate` actualizado sin crear duplicados.
- Si quieres que una revisión mayor aparezca como entrada nueva en algunos lectores (que deduplican por GUID), crea un nuevo `Slug` (p. ej., añade un sufijo `-v2`, `-2025-10`, etc.).
- Evita duplicar `Slug` en el CSV: cada fila debe tener un identificador único.
- Para ocultar borradores, usa `:draft=true` (esas filas no se incluyen en el feed).

Ejemplos rápidos:
- Actualización menor: `Slug=energia-solar`, `Fecha=2025-09-30T18:42:00Z` (mismo Slug; el ítem se reordena como más reciente).
- Re-publicación como nueva entrada: `Slug=energia-solar-v2`, `Fecha=2025-10-01T09:15:00Z` (nuevo Slug; se verá como ítem nuevo en todos los lectores).

## ⚙️ Configuración

Edita `feed_config.py` para personalizar:
- URL del sitio
- Título del feed
- Descripción

---

Proyecto por [REAL es TODO](https://realestodo.com)
