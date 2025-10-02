#!/usr/bin/env python3

import csv
from datetime import datetime
import html
import re
import os
import glob

def clean_html(html_string):
    """Clean HTML content for RSS feed"""
    if not html_string:
        return ""
    # Remove script and style tags
    html_string = re.sub(r'<script[^>]*>.*?</script>', '', html_string, flags=re.DOTALL)
    html_string = re.sub(r'<style[^>]*>.*?</style>', '', html_string, flags=re.DOTALL)
    return html_string

def escape_xml(text):
    """Escape XML special characters"""
    if not text:
        return ""
    return html.escape(text, quote=True)

def extract_text_from_html(html_string):
    """Extract plain text from HTML for description"""
    if not html_string:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html_string)
    # Clean up whitespace
    text = ' '.join(text.split())
    return text

def truncate_text(text, max_length=500):
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def get_first_value(row, keys, default=""):
    """Return the first non-empty value from the given keys in row."""
    for k in keys:
        v = row.get(k)
        if v is not None and str(v).strip() != "":
            return v
    return default

def _resolve_csv_file(csv_file_pattern):
    """Resolve the CSV file to use. If the exact csv_file_pattern exists, use it.
    Otherwise, try the latest matching 'Todo*.csv' by modification time.
    """
    # Exact file present
    if csv_file_pattern and os.path.exists(csv_file_pattern):
        return csv_file_pattern

    # Fallback: pick most recent matching pattern
    candidates = sorted(
        glob.glob('Todo*.csv'),
        key=lambda p: os.path.getmtime(p),
        reverse=True
    )
    if candidates:
        print(f"[info] 'Todo.csv' no encontrado. Usando CSV más reciente: {candidates[0]}")
        return candidates[0]

    raise FileNotFoundError(f"No se encontró '{csv_file_pattern}' ni archivos 'Todo*.csv' en el directorio actual.")


def create_rss_feed(csv_file, output_file='feed.xml', site_url='https://example.com', 
                   feed_title='Mi Feed RSS', feed_description='Feed RSS generado desde CSV'):
    """Convert CSV to RSS XML feed - Simple version"""
    
    # Start building XML manually
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<rss version="2.0"')
    xml_lines.append('  xmlns:content="http://purl.org/rss/1.0/modules/content/"')
    xml_lines.append('  xmlns:dc="http://purl.org/dc/elements/1.1/"')
    xml_lines.append('  xmlns:media="http://search.yahoo.com/mrss/"')
    xml_lines.append('  xmlns:atom="http://www.w3.org/2005/Atom">')
    xml_lines.append('  <channel>')
    
    # Add channel metadata
    xml_lines.append(f'    <title>{escape_xml(feed_title)}</title>')
    xml_lines.append(f'    <link>{escape_xml(site_url)}</link>')
    xml_lines.append(f'    <description>{escape_xml(feed_description)}</description>')
    xml_lines.append('    <language>es</language>')
    xml_lines.append('    <generator>CSV to RSS Generator</generator>')
    xml_lines.append(f'    <atom:link href="{escape_xml(site_url)}/feed.xml" rel="self" type="application/rss+xml"/>')
    
    # Set lastBuildDate to current time
    build_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    xml_lines.append(f'    <lastBuildDate>{build_date}</lastBuildDate>')
    
    # Read CSV and create items
    items_added = 0
    csv_path = _resolve_csv_file(csv_file)
    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)

        # Sort by date if available
        rows = list(reader)
        rows_with_dates = []

        for row in rows:
            # Skip drafts
            estado = str(row.get('Estado', '')).strip().lower()
            if row.get(':draft', '').lower() == 'true' or estado in {'draft', 'borrador', 'true', '1'}:
                continue

            # Parse date: prefer 'Fecha', fallback to 'Actualizado'
            date_str = get_first_value(row, ['Fecha', 'Actualizado'], '')
            if date_str:
                try:
                    pub_date = datetime.fromisoformat(str(date_str).replace('Z', '+00:00'))
                except Exception:
                    pub_date = datetime.now()
            else:
                pub_date = datetime.now()
            rows_with_dates.append((pub_date, row))

        # Sort by date, newest first
        rows_with_dates.sort(key=lambda x: x[0], reverse=True)

        # Create RSS items
        for pub_date, row in rows_with_dates[:50]:  # Limit to 50 most recent items
            xml_lines.append('    <item>')
            
            # Title
            title = get_first_value(row, ['Título', 'Nombre'], 'Sin título')
            xml_lines.append(f'      <title>{escape_xml(title)}</title>')
            
            # Link
            slug = row.get('Slug', '')
            if slug:
                item_url = f"{site_url}/{slug}"
            else:
                item_url = site_url
            xml_lines.append(f'      <link>{escape_xml(item_url)}</link>')
            
            # GUID
            xml_lines.append(f'      <guid isPermaLink="true">{escape_xml(item_url)}</guid>')
            
            # Publication date
            pub_date_str = pub_date.strftime('%a, %d %b %Y %H:%M:%S +0000')
            xml_lines.append(f'      <pubDate>{pub_date_str}</pubDate>')
            
            # Description
            description = row.get('Bajada', '')
            if not description:
                original_or_content = get_first_value(row, ['Original', 'Contenido', 'Content'], '')
                if original_or_content:
                    description = extract_text_from_html(original_or_content)
                description = truncate_text(description, 300)
            if not description:
                description = row.get('Meta', 'Sin descripción')
            xml_lines.append(f'      <description>{escape_xml(description)}</description>')
            
            # Full content in content:encoded with CDATA
            original_content = get_first_value(row, ['Original', 'Contenido', 'Content'], '')
            bajada = row.get('Bajada', '')
            
            # Combine bajada as subtitle with original content
            if original_content or bajada:
                full_content = ""
                if bajada:
                    # Add bajada as a subtitle at the beginning
                    full_content = f'<h2>{bajada}</h2>'
                if original_content:
                    full_content += clean_html(original_content)
                xml_lines.append(f'      <content:encoded><![CDATA[{full_content}]]></content:encoded>')
            
            # Categories
            capitulo = row.get('Capítulo', '')
            if capitulo:
                xml_lines.append(f'      <category>{escape_xml(capitulo)}</category>')
            
            libro = row.get('Libro', '')
            if libro and libro != capitulo:
                xml_lines.append(f'      <category>{escape_xml(libro)}</category>')
            
            # Media thumbnail
            portada = row.get('Portada', '') or row.get('Social Share', '')
            if portada:
                xml_lines.append(f'      <media:content url="{escape_xml(portada)}" type="image/jpeg" medium="image"/>')
                xml_lines.append(f'      <media:thumbnail url="{escape_xml(portada)}"/>')
            
            # Podcast enclosure
            podcast_url = row.get('Podcast', '')
            if podcast_url:
                xml_lines.append(f'      <enclosure url="{escape_xml(podcast_url)}" type="audio/mpeg" length="0"/>')
            
            xml_lines.append('    </item>')
            items_added += 1
    
    # Close XML
    xml_lines.append('  </channel>')
    xml_lines.append('</rss>')
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))
    
    print(f"RSS feed generated successfully!")
    print(f"  Output file: {output_file}")
    print(f"  Total items: {items_added}")
    
    return output_file

def update_feed_config():
    """Create a configuration file for feed settings"""
    config = {
        'site_url': 'https://realestodo.com/todo',
        'feed_title': 'ATLAS DE TODO',
        'feed_description': 'Hackea el antropoceno; contempla el fin de los tiempos.',
        'csv_file': 'Todo.csv',
        'output_file': 'feed.xml'
    }
    
    # Check if config exists
    config_file = 'feed_config.py'
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            f.write("# RSS Feed Configuration\n")
            f.write("# Edit these values according to your needs\n\n")
            for key, value in config.items():
                f.write(f"{key.upper()} = '{value}'\n")
        print(f"Configuration file created: {config_file}")
        print("Please edit the configuration with your actual values.")
    
    return config

if __name__ == "__main__":
    # Generate RSS feed with configured settings
    create_rss_feed(
        csv_file='Todo.csv',
        output_file='feed.xml',
        site_url='https://realestodo.com/todo',
        feed_title='ATLAS DE TODO',
        feed_description='Hackea el antropoceno; contempla el fin de los tiempos.'
    )
    
    # Also create a config file for easy updates
    update_feed_config()
