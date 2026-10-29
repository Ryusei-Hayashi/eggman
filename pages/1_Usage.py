import streamlit as st

st.set_page_config('EgGMAn', ':musical_note:', 'wide', 'expanded')
st.sidebar.link_button('Contact Us', 'https://forms.gle/A4vWuEAp4pPEY4sf9', use_container_width=True)

st.title('Usage')

st.iframe('https://drive.google.com/file/d/1X0O0hd9EHayuhPaUyPzXYJZljInnRtgO/preview')

st.header('Source Music')
st.markdown('- Enter the music prepared for the development game\n  - URL Input: Enter the URL of [these sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) or the direct link\n  - File Input: Enter the audio file')

st.header('Target Scene')
st.markdown('- Enter the scene where no music is prepared\n- Enter the scene by combining about 200 tags such as _Opening_, _Dungeon_, ...')

st.subheader('Emotion of Target Scene')
st.markdown('- Enter the emotion of the scene using sliders\n  - Valence: Rises in positive scenes and falls in negative scenes\n  - Arousal: Rises in active scenes and falls in passive scenes')

st.header('Target Music')
st.markdown('- EgGMAn searches for music in Target Scene for the development game\n  - Mute Artist: Enter the artist to mute\n  - Mute Site: Enter the site to mute\n  - Playtime: Enter the playtime of the music\n  - Filter by Target Scene: Select whether to filter the search result by Target Scene')
