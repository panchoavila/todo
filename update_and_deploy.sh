#!/bin/bash

# Script para actualizar RSS y publicar en GitHub

echo "📡 Actualizando RSS feed..."
python3 csv_to_rss.py

echo "📦 Preparando commit..."
git add feed.xml
git commit -m "Update RSS feed: $(date '+%Y-%m-%d %H:%M')"

echo "🚀 Publicando en GitHub..."
git push

echo "✅ Feed actualizado y publicado!"
echo "🔗 Tu feed está en: https://TU-USUARIO.github.io/NOMBRE-REPO/feed.xml"