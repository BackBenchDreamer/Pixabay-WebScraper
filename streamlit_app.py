# streamlit_app.py
import streamlit as st
from main import fetch_images, download_images, create_zip
import os
import shutil  # For deleting non-empty directories

# Add custom CSS for styling the title and importing Bebas Neue font
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

    .title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 4em;
        text-align: center;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App title with custom style
st.markdown('<div class="title">Pix-a-Harvest</div>', unsafe_allow_html=True)

# Input fields for search term, number of images, and file name template
search_query = st.text_input('Enter the name for the image search:', 'cats')
num_images = st.number_input('Enter the number of images to download:', min_value=1, max_value=50, value=10)
file_name_template = st.text_input('Enter the file name template:', 'image')  # New field for custom file name

# Download button
if st.button('Download Images'):
    # Fetch image URLs from Pixabay
    image_urls = fetch_images(search_query, num_images)

    if image_urls:
        # Create a temporary directory to download images
        download_dir = 'downloads'
        file_paths = download_images(image_urls, download_dir, file_name_template)  # Pass custom file name

        # Create a zip file of the downloaded images
        zip_path = os.path.join(download_dir, 'images.zip')
        create_zip(file_paths, zip_path)

        # Provide a download link for the zip file
        with open(zip_path, 'rb') as f:
            st.download_button('Download ZIP', f, file_name=f'{file_name_template}.zip')

        # Clean up the downloaded images and directory
        for file in file_paths:
            os.remove(file)

        # Remove the directory
        shutil.rmtree(download_dir)  # Use shutil.rmtree instead of os.rmdir

    else:
        st.write("No images found.")
