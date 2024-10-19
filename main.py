# main.py
import os
import requests
from creds import API_KEY
from zipfile import ZipFile

def fetch_images(query, num_images=10):
    """
    Fetch images from Pixabay based on the query and number of images.
    
    Args:
        query (str): The search term for Pixabay API.
        num_images (int): Number of images to fetch.
    
    Returns:
        List of image URLs.
    """
    url = f"https://pixabay.com/api/?key={API_KEY}&q={query}&image_type=photo&per_page={num_images}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and 'hits' in data:
        return [hit['largeImageURL'] for hit in data['hits']]
    else:
        print("Error fetching data from Pixabay.")
        return []

def download_images(image_urls, download_dir, file_name_template):
    """
    Downloads images from given URLs and stores them in the specified directory.
    
    Args:
        image_urls (list): List of image URLs to download.
        download_dir (str): The directory to save images.
        file_name_template (str): The custom file name template.
    
    Returns:
        List of downloaded file paths.
    """
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    file_paths = []
    for i, url in enumerate(image_urls):
        response = requests.get(url)
        file_name = f"{file_name_template}_{i+1}.jpg"  # Use custom file name template
        file_path = os.path.join(download_dir, file_name)
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        file_paths.append(file_path)
    
    return file_paths

def create_zip(file_paths, output_zip):
    """
    Creates a zip file from the list of file paths.
    
    Args:
        file_paths (list): List of file paths to include in the zip.
        output_zip (str): The output zip file path.
    
    Returns:
        str: The path to the created zip file.
    """
    with ZipFile(output_zip, 'w') as zipf:
        for file in file_paths:
            zipf.write(file, os.path.basename(file))
    
    return output_zip
