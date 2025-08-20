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

## ⚙️ Configuración

Edita `feed_config.py` para personalizar:
- URL del sitio
- Título del feed
- Descripción

---

Proyecto por [REAL es TODO](https://realestodo.com)