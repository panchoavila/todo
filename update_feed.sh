#!/bin/bash

# Script para actualizar el RSS feed y publicar en GitHub

echo "🔄 Actualizando RSS feed..."
python3 csv_to_rss.py

echo "📝 Añadiendo cambios a git..."
git add feed.xml

echo "💾 Creando commit..."
git commit -m "Update RSS feed: $(date '+%Y-%m-%d %H:%M')"

echo "🚀 Publicando en GitHub..."
git push

echo "✅ ¡Feed actualizado!"
echo "🔗 Ver en: https://panchoavila.github.io/RSS/feed.xml"