#!/usr/bin/python3
"""
Script to generate a comprehensive JSON catalog of all audio files in the repository.
"""

import os
import json
import re
from datetime import datetime

def extract_artist_from_filename(filename):
    """Extract artist name from filename using common patterns."""
    # Remove file extension
    name = filename.replace('.mp3', '')
    
    # Common patterns for artist extraction
    patterns = [
        r'by\s+([^-]+?)(?:\s*-|\s*$)',  # "by Artist"
        r'feat\.\s+([^-]+?)(?:\s*-|\s*$)',  # "feat. Artist"
        r'^([^-]+?)\s*-',  # "Artist - Title"
        r'-\s*([^-]+?)(?:\s*\(|\s*$)',  # "- Artist"
    ]
    
    # Known artists from the collection
    known_artists = [
        'Omar Esa', 'Maher Zain', 'Muhammad al Muqit', 'Muhammad Al Muqit', 
        'Muhammad Al-Muqit', 'Nadeem Mohammed', 'Ahmed Bukhatir', 'Zain Bhikha',
        'Khaled Siddique', 'Labbayk', 'Ahmad Hussain', 'Mishari Rashid Al Afasy',
        'Sami Yusuf', 'Mesut Kurtis', 'Mohammed Alomari', 'Anas Dosari',
        'Kamal Uddin', 'Othman Al Ibrahim', 'Ehsaan Tahmid', 'Ali Gulam',
        'Ishaq Ayubi', 'Yusuf Islam', 'Raid al-Qahtani', 'Seyifunmi'
    ]
    
    # Check for known artists in filename
    for artist in known_artists:
        if artist.lower() in name.lower():
            return artist
    
    # Try pattern matching
    for pattern in patterns:
        match = re.search(pattern, name, re.IGNORECASE)
        if match:
            artist = match.group(1).strip()
            # Clean up common prefixes/suffixes
            artist = re.sub(r'^(Official|Nasheed|Video)', '', artist, flags=re.IGNORECASE).strip()
            if artist and len(artist) > 2:
                return artist
    
    return "Unknown"

def categorize_nasheed(filename, title):
    """Categorize nasheed based on filename and title."""
    text = (filename + " " + title).lower()
    
    if any(word in text for word in ['emotional', 'tear', 'sad', 'broken', 'longing']):
        return "emotional"
    elif any(word in text for word in ['motivational', 'rise', 'happy', 'guidance']):
        return "motivational"
    elif any(word in text for word in ['allah', 'rabbi', 'lord', 'dua', 'prayer']):
        return "supplication"
    elif any(word in text for word in ['prophet', 'nabi', 'muhammad', 'mustafa']):
        return "prophet"
    elif any(word in text for word in ['quran', 'surah', 'fatiha']):
        return "quran"
    elif any(word in text for word in ['ramadan', 'eid', 'hajj']):
        return "seasonal"
    elif any(word in text for word in ['palestine', 'syria', 'social']):
        return "social"
    elif any(word in text for word in ['burdah', 'classical']):
        return "classical"
    elif any(word in text for word in ['dhikr', 'remembrance', 'allahu']):
        return "dhikr"
    elif any(word in text for word in ['unity', 'together', 'community']):
        return "unity"
    else:
        return "religious"

def detect_language(filename, title):
    """Detect language based on filename and title."""
    text = (filename + " " + title).lower()
    
    if any(word in text for word in ['bangla', 'matir', 'sharey']):
        return "bangla"
    elif any(word in text for word in ['urdu', 'pyaareh', 'tera', 'kiya']):
        return "urdu"
    elif any(word in text for word in ['arabic', 'ya', 'al', 'bil', 'mawlaya', 'rahman']):
        return "arabic"
    else:
        return "english"

def generate_tags(filename, title, artist, category):
    """Generate relevant tags for the nasheed."""
    text = (filename + " " + title).lower()
    tags = []
    
    # Add category as tag
    tags.append(category)
    
    # Common Islamic terms
    islamic_terms = ['allah', 'prophet', 'muhammad', 'dua', 'prayer', 'quran', 
                    'ramadan', 'eid', 'hajj', 'dhikr', 'remembrance']
    for term in islamic_terms:
        if term in text:
            tags.append(term)
    
    # Emotional descriptors
    emotions = ['peaceful', 'beautiful', 'powerful', 'heart touching', 'soothing']
    for emotion in emotions:
        if emotion in text:
            tags.append(emotion.replace(' ', '_'))
    
    # Remove duplicates and return
    return list(set(tags))

def clean_title(filename):
    """Extract clean title from filename."""
    # Remove file extension
    title = filename.replace('.mp3', '')
    
    # Remove common prefixes and patterns
    title = re.sub(r'^\d+\.\s*', '', title)  # Remove track numbers
    title = re.sub(r'\s*-\s*Official.*?Video', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*\(Official.*?\)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*by\s+[^-]+', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*-\s*[^-]*Nasheed', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*feat\..*', '', title, flags=re.IGNORECASE)
    
    # Clean up quotes and extra spaces
    title = title.strip('\'"').strip()
    
    return title

def main():
    """Generate the complete audio catalog."""
    base_path = "/workspace"
    files = []
    file_id = 1
    
    # Get all MP3 files
    for filename in os.listdir(base_path):
        if filename.endswith('.mp3'):
            # Extract information
            title = clean_title(filename)
            artist = extract_artist_from_filename(filename)
            category = categorize_nasheed(filename, title)
            language = detect_language(filename, title)
            tags = generate_tags(filename, title, artist, category)
            
            # Create file entry
            file_entry = {
                "id": file_id,
                "filename": filename,
                "title": title,
                "artist": artist,
                "format": "mp3",
                "path": f"/workspace/{filename}",
                "category": category,
                "language": language,
                "tags": tags
            }
            
            files.append(file_entry)
            file_id += 1
    
    # Sort files by artist, then by title
    files.sort(key=lambda x: (x['artist'], x['title']))
    
    # Create artist index
    artists = {}
    for file_entry in files:
        artist = file_entry['artist']
        if artist not in artists:
            artists[artist] = []
        artists[artist].append(file_entry['id'])
    
    # Create category index
    categories = {}
    for file_entry in files:
        category = file_entry['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(file_entry['id'])
    
    # Create language index
    languages = {}
    for file_entry in files:
        language = file_entry['language']
        if language not in languages:
            languages[language] = []
        languages[language].append(file_entry['id'])
    
    # Create complete catalog
    catalog = {
        "metadata": {
            "collection_name": "Nasheed Collection",
            "description": "Collection of Islamic vocal music (Nasheeds) for backup purposes",
            "total_files": len(files),
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "format": "mp3",
            "base_path": "/workspace",
            "version": "1.0"
        },
        "files": files,
        "indices": {
            "artists": artists,
            "categories": categories,
            "languages": languages
        },
        "api_endpoints": {
            "all_files": "/api/files",
            "by_artist": "/api/files/artist/{artist_name}",
            "by_category": "/api/files/category/{category_name}",
            "by_language": "/api/files/language/{language_code}",
            "search": "/api/files/search?q={query}",
            "file_details": "/api/files/{file_id}"
        }
    }
    
    # Write to JSON file
    with open(f"{base_path}/audio_catalog.json", "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    
    print(f"Generated catalog with {len(files)} files")
    print(f"Artists: {len(artists)}")
    print(f"Categories: {len(categories)}")
    print(f"Languages: {len(languages)}")

if __name__ == "__main__":
    main()