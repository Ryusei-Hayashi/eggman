import streamlit as st

st.set_page_config('EgGMAn', ':musical_note:', 'wide', 'expanded')
st.sidebar.link_button('Contact Us', 'https://forms.gle/A4vWuEAp4pPEY4sf9', use_container_width=True)

st.title('System')
st.iframe('https://drive.google.com/file/d/1a167-_xiTrvA9JtiEfI8RST_T8996Stu/preview')
st.markdown('- Compute the embedding $\mathbf{z^p}$ for Source Music\n- Compute the representative embedding $\mathbf{r^q}$ for Target Scene\n  - Collect music tracks to use in the same scene as Target Scene\n  - Compute the center of embedding for collected music tracks\n- Predict the embedding $\mathbf{z^q}$ for Target Music from $\mathbf{z^p}$ and $\mathbf{r^q}$\n- Search for music with embeddings close to $\mathbf{z^q}$')
