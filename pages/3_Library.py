import streamlit as st

st.set_page_config('EgGMAn', ':musical_note:', 'wide', 'expanded')
st.sidebar.link_button('Contact Us', 'https://forms.gle/A4vWuEAp4pPEY4sf9', use_container_width=True)

st.title('Library')

st.header('Paper')
st.iframe('https://drive.google.com/file/d/18H8dnbhL-D53BUWb09nGVWGWyot06OM6/preview')

st.header('Slide')
st.iframe('https://drive.google.com/file/d/1MIN0am-lZV7TqGx20CjgG1CSQXyLkgOO/preview')
