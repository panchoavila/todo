#!/usr/bin/env python3

import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import html
import re
import os

def clean_html(html_string):
    """Clean HTML content for RSS feed"""
    if not html_string:
        return ""
    # Remove script and style tags
    html_string = re.sub(r'<script[^>]*>.*?</script>', '', html_string, flags=re.DOTALL)
    html_string = re.sub(r'<style[^>]*>.*?</style>', '', html_string, flags=re.DOTALL)
    return html_string

def truncate_text(text, max_length=500):
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def extract_text_from_html(html_string):
    """Extract plain text from HTML for description"""
    if not html_string:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html_string)
    # Clean up whitespace
    text = ' '.join(text.split())
    return text

def create_rss_feed(csv_file, output_file='feed.xml', site_url='https://example.com', feed_title='Mi Feed RSS', feed_description='Feed RSS generado desde CSV'):
    """Convert CSV to RSS XML feed"""
    
    # Create RSS root element
    rss = ET.Element('rss', attrib={
        'version': '2.0',
        'xmlns:content': 'http://purl.org/rss/1.0/modules/content/',
        'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
        'xmlns:media': 'http://search.yahoo.com/mrss/',
        'xmlns:atom': 'http://www.w3.org/2005/Atom'
    })
    
    channel = ET.SubElement(rss, 'channel')
    
    # Add channel metadata
    ET.SubElement(channel, 'title').text = feed_title
    ET.SubElement(channel, 'link').text = site_url
    ET.SubElement(channel, 'description').text = feed_description
    ET.SubElement(channel, 'language').text = 'es'
    ET.SubElement(channel, 'generator').text = 'CSV to RSS Generator'
    
    # Add atom:link for feed URL
    atom_link = ET.SubElement(channel, '{http://www.w3.org/2005/Atom}link')
    atom_link.set('href', f"{site_url}/feed.xml")
    atom_link.set('rel', 'self')
    atom_link.set('type', 'application/rss+xml')
    
    # Set lastBuildDate to current time
    build_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    ET.SubElement(channel, 'lastBuildDate').text = build_date
    
    # Read CSV and create items
    items_added = 0
    with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        
        # Sort by date if available
        rows = list(reader)
        rows_with_dates = []
        
        for row in rows:
            # Skip drafts unless you want to include them
            if row.get(':draft', '').lower() == 'true':
                continue
                
            # Parse date
            date_str = row.get('Fecha', '')
            if date_str:
                try:
                    # Parse ISO format date
                    pub_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    rows_with_dates.append((pub_date, row))
                except:
                    # If date parsing fails, use current date
                    rows_with_dates.append((datetime.now(), row))
        
        # Sort by date, newest first
        rows_with_dates.sort(key=lambda x: x[0], reverse=True)
        
        # Create RSS items
        for pub_date, row in rows_with_dates[:50]:  # Limit to 50 most recent items
            item = ET.SubElement(channel, 'item')
            
            # Title
            title = row.get('Título', 'Sin título')
            ET.SubElement(item, 'title').text = title
            
            # Link - construct from slug if available
            slug = row.get('Slug', '')
            if slug:
                item_url = f"{site_url}/{slug}"
            else:
                item_url = site_url
            ET.SubElement(item, 'link').text = item_url
            
            # GUID
            ET.SubElement(item, 'guid', isPermaLink='true').text = item_url
            
            # Publication date
            pub_date_str = pub_date.strftime('%a, %d %b %Y %H:%M:%S +0000')
            ET.SubElement(item, 'pubDate').text = pub_date_str
            
            # Description - use Bajada or extract from Original content
            description = row.get('Bajada', '')
            if not description and row.get('Original'):
                description = extract_text_from_html(row.get('Original', ''))
                description = truncate_text(description, 300)
            if not description:
                description = row.get('Meta', 'Sin descripción')
            ET.SubElement(item, 'description').text = description
            
            # Full content in content:encoded
            original_content = row.get('Original', '')
            if original_content:
                content_elem = ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded')
                content_elem.text = clean_html(original_content)
            
            # Category/Tags
            capitulo = row.get('Capítulo', '')
            if capitulo:
                ET.SubElement(item, 'category').text = capitulo
            
            libro = row.get('Libro', '')
            if libro and libro != capitulo:
                ET.SubElement(item, 'category').text = libro
            
            # Media thumbnail
            portada = row.get('Portada', '') or row.get('Social Share', '')
            if portada:
                media_content = ET.SubElement(item, '{http://search.yahoo.com/mrss/}content')
                media_content.set('url', portada)
                media_content.set('medium', 'image')
                
                media_thumb = ET.SubElement(item, '{http://search.yahoo.com/mrss/}thumbnail')
                media_thumb.set('url', portada)
            
            # Podcast enclosure if available
            podcast_url = row.get('Podcast', '')
            if podcast_url:
                enclosure = ET.SubElement(item, 'enclosure')
                enclosure.set('url', podcast_url)
                enclosure.set('type', 'audio/mpeg')
                # Set a default length since we don't have file size info
                enclosure.set('length', '0')
            
            items_added += 1
    
    # Pretty print XML
    xml_string = ET.tostring(rss, encoding='unicode')
    dom = minidom.parseString(xml_string)
    pretty_xml = dom.toprettyxml(indent="  ")
    
    # Remove extra blank lines
    pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    
    print(f"RSS feed generated successfully!")
    print(f"  Output file: {output_file}")
    print(f"  Total items: {items_added}")
    
    return output_file

def update_feed_config():
    """Create a configuration file for feed settings"""
    config = {
        'site_url': 'https://tu-sitio.com',
        'feed_title': 'Mi Blog Personal',
        'feed_description': 'Artículos sobre crecimiento personal y desarrollo',
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
    # Generate RSS feed with default settings
    # You can customize these values
    create_rss_feed(
        csv_file='Todo.csv',
        output_file='feed.xml',
        site_url='https://realestodo.com/todo',
        feed_title='ATLAS DE TODO',
        feed_description='Hackea el antropoceno; contempla el fin de los tiempos.'
    )
    
    # Also create a config file for easy updates
    update_feed_config()