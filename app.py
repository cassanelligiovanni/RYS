import streamlit as st
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os
import json
import time
from components import card_layout
import requests
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import time

load_dotenv()


# Initialize Spotify API client
sp_oauth = SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                         client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                         redirect_uri="http://localhost:8501/redirect",
                         scope="user-read-email, user-read-private")

# Function to save token_info to a file
def save_token_to_file(token_info):
    with open('token_info.json', 'w') as f:
        json.dump(token_info, f)

# Function to load token_info from a file
def load_token_from_file():
    try:
        with open('token_info.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# Function to check if the token is expired
def is_token_expired(token_info):
    now = int(time.time())
    return token_info['expires_at'] - now < 60

# Function to scroll to the bottom of the page
def scroll_to_bottom(driver):
    for _ in range(4):  # Scroll 4 times
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.3)


# Load token from file
token_info = load_token_from_file()


# Check if loaded token is expired or not present
if token_info and not is_token_expired(token_info):
    sp = Spotify(auth=token_info['access_token'])
else:
    # Show authorization URL
    auth_url = sp_oauth.get_authorize_url()
    st.write(f"Please login [here]({auth_url}).")
    url = st.text_input("Enter the URL you were redirected to: ")

    if url:
        try:
            code = sp_oauth.parse_response_code(url)
            token_info = sp_oauth.get_access_token(code)
            sp = Spotify(auth=token_info['access_token'])
            save_token_to_file(token_info)
        except Exception as e:
            st.write(f"An error occurred: {e}")

# Once logged in, display user info and Additional UI
if token_info and not is_token_expired(token_info):
    me = sp.me()
    card_layout(me['images'][0]['url'], me['display_name'], me['email'], me['country'])

    st.write("## Rate Your Spotify")


    # Check if 'pressed' is not already set in the session state
    if not hasattr(st.session_state, 'pressed'):
        st.session_state.pressed = False

    playlistName = st.text_input("Name of the playlist", "RYS - Romantic - 2023")
    url = st.text_input("Enter chart URL from Rate your Music (only Singles)", "https://rateyourmusic.com/charts/top/single/2023/d:romantic/")
    n_tracks = st.selectbox("Number of tracks", [40, 80, 120, 160, 200, 240, 280, 320], index=0)

    if st.button("Create Playlist"):
        st.session_state.pressed = True

    if st.session_state.pressed:

        try:
            chromedriver_autoinstaller.install()
            driver = webdriver.Chrome()
            driver.get(url)
            wait = WebDriverWait(driver, 10) 

            try:
                consent_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Consent"]')))
                consent_button.click()

                track_ids = []
                count = 0
                
                for page in range(1, int(n_tracks/40)+1):

                    if page > 1:
                        print(url+f"/{page}")
                        driver.get(url+f"/{page}")
                        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[id*="pos"]')))
                    
                    scroll_to_bottom(driver)

                    singles = driver.find_elements(By.CSS_SELECTOR, '[id*="pos"]')
                    
                    if len(singles) > 0:
                        
                        # Iterate through the list of singles 
                        for single in singles:
                            count += 1
                            
                            # st.write(single.get_attribute('outerHTML'))
                            title = single.find_elements(By.CLASS_NAME, 'ui_name_locale')[0].text
                            artist = single.find_elements(By.CLASS_NAME, 'ui_name_locale')[1].text

                            query = f"{title} {artist}"

                            # Search for the track on Spotify
                            results = sp.search(q=query, limit=10, offset=0, type='track')
                            
                            if len(results['tracks']['items']) == 0:
                                st.write(f"Single #{count} not found : {query}")
                                continue

                            track_id = results['tracks']['items'][0]['id']
                            track_ids.append(track_id)

                if len(track_ids) > 0:
                    # Create a new playlist called Rate Your Spotify
                    playlist = sp.user_playlist_create(me['id'], playlistName, public=False) 

                    # Add the tracks to the playlist     
                    sp.playlist_add_items(playlist['id'], track_ids)

                else:
                    st.write("No singles found")
                
                st.write("Completed!")
                driver.quit()

            except TimeoutException as e:
                st.write(f"Consent Button not Found or other TimeoutException")
            
            except Exception as e:
                print(e)
                st.write(f"An error occurred: {e}")

            

        except Exception as e:
            print(e)
            st.write(f"An error occurred: {e}")