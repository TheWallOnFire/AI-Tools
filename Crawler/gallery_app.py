import streamlit as st
import os
import math

# Page configuration
st.set_page_config(page_title="AI-Tools Image Gallery", layout="wide")

st.title("🖼️ Paginated Image Gallery")
st.markdown("View all collected images in a customizable grid layout.")

# Configuration
URL_FILE = "url_img.txt"

def load_urls(file_path):
    """Loads and filters URLs from the specified file."""
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, "r", encoding="utf-8") as f:
        # Filter out empty lines and whitespace
        urls = [line.strip() for line in f if line.strip()]
    return urls

urls = load_urls(URL_FILE)

if not urls:
    st.warning(f"No URLs found in `{URL_FILE}`. Please run the crawler first!")
    st.stop()

# Sidebar Settings
st.sidebar.header("Grid Settings")
cols = st.sidebar.number_input("Columns", min_value=1, max_value=10, value=4)
rows = st.sidebar.number_input("Rows per Page", min_value=1, max_value=20, value=3)
images_per_page = cols * rows

total_images = len(urls)
total_pages = math.ceil(total_images / images_per_page)

st.sidebar.divider()
st.sidebar.header("Navigation")

# Pagination State Management
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

def next_page():
    if st.session_state.current_page < total_pages:
        st.session_state.current_page += 1

def prev_page():
    if st.session_state.current_page > 1:
        st.session_state.current_page -= 1

def first_page():
    st.session_state.current_page = 1

def last_page():
    st.session_state.current_page = total_pages

# Page selection slider
st.sidebar.slider("Go to Page", 1, total_pages, key="page_slider_key")
# Sync slider with session state
st.session_state.current_page = st.session_state.page_slider_key

# Calculation of indices
start_idx = (st.session_state.current_page - 1) * images_per_page
end_idx = min(start_idx + images_per_page, total_images)
page_urls = urls[start_idx:end_idx]

# Page Info Display
st.markdown(f"**Showing {start_idx + 1} - {end_idx} of {total_images} results (Page {st.session_state.current_page}/{total_pages})**")

# Top Navigation Buttons
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1, 1, 1, 1])
with nav_col1:
    st.button("⏪ First", on_click=first_page, use_container_width=True)
with nav_col2:
    st.button("◀️ Prev", on_click=prev_page, use_container_width=True)
with nav_col3:
    st.button("Next ▶️", on_click=next_page, use_container_width=True)
with nav_col4:
    st.button("Last ⏩", on_click=last_page, use_container_width=True)

st.divider()

# Rendering the Grid
for i in range(0, len(page_urls), cols):
    columns = st.columns(cols)
    for j in range(cols):
        idx = i + j
        if idx < len(page_urls):
            with columns[j]:
                current_url = page_urls[idx]
                try:
                    # Provide an ID and a container for better layout
                    st.image(current_url, use_container_width=True)
                    # Show truncated URL and a link
                    st.caption(f"Index: {start_idx + idx + 1}")
                    st.markdown(f"[Link]({current_url})", help=current_url)
                except Exception as e:
                    st.error(f"Error loading image {start_idx + idx + 1}")

st.divider()

# Bottom Navigation (same as top)
b_nav_col1, b_nav_col2, b_nav_col3, b_nav_col4 = st.columns([1, 1, 1, 1])
with b_nav_col1:
    st.button("⏪ First", on_click=first_page, key="b_first", use_container_width=True)
with b_nav_col2:
    st.button("◀️ Prev", on_click=prev_page, key="b_prev", use_container_width=True)
with b_nav_col3:
    st.button("Next ▶️", on_click=next_page, key="b_next", use_container_width=True)
with b_nav_col4:
    st.button("Last ⏩", on_click=last_page, key="b_last", use_container_width=True)

# Sidebar metadata
st.sidebar.divider()
st.sidebar.write(f"📁 Source: `{URL_FILE}`")
st.sidebar.button("Refresh Data", on_click=lambda: st.cache_data.clear())
