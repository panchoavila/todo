#!/bin/bash

# Script para actualizar y deployar solo el RSS (mantiene código privado)

echo "📡 Generando RSS actualizado..."
python3 csv_to_rss.py

echo "📦 Copiando archivos públicos..."
cp feed.xml ../RSS-public/
cp index.html ../RSS-public/

echo "🚀 Publicando cambios..."
cd ../RSS-public
git add .
git commit -m "Update RSS feed: $(date '+%Y-%m-%d %H:%M')"
git push

echo "✅ RSS actualizado (código fuente permanece privado)"