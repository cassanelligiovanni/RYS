# RYS: RateYourMusic to Spotify Playlist

Convert your [RateYourMusic.com](https://rateyourmusic.com) charts into Spotify playlists using Streamlit.

## Overview

The primary goal of this repository is to simplify the process of music discovery in a highly customizable manner. With this application, users can easily convert a chart they customize on [RateYourMusic.com](https://rateyourmusic.com/charts/) into Spotify Playlists.

To begin, generate a chart on [RateYourMusic](https://rateyourmusic.com/charts/), utilize the filters on the right side of the page, then copy the URL of that chart. Upon entering this URL into the Streamlit app, a corresponding Spotify playlist is created.

## Limitations

This application is primarily designed for local execution using Streamlit due to its dependency on Selenium, which requires a browser driver (specifically, Chromedriver in this case).

Running Selenium in cloud environments can be more intricate, often involving configurations like Docker coupled with OS-specific images, such as Debian. While feasible, implementing such configurations extends beyond this repository's intent.

## Configuration

To set up and run the application:

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up an application on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
3. Obtain `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` from the Spotify application you've created.
4. Save the `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, and the desired redirect `URL` in a `.env` file.
5. Launch the application:
   ```bash
   streamlit run app.py
   ```

## Video Guide

A comprehensive video walkthrough detailing the application flow will be provided soon. Stay tuned!
