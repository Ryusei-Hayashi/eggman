# EgGMAn
- This repository is for Deploying [EgGMAn (Engine of Game Music Analysis)](https://eggman.streamlit.app)
- EgGMAn searches for game music balancing game-wise consistency and scene-wise individuality

## Usage
### Source Music
- Enter the music prepared for the development game
  - Web Service: Enter the URL of [these sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)
  - Direck Link: Enter the URL of the audio file
  - Audio file: Enter the uploaded audio file

### Traget Scene
- Enter the scene where no music is prepared
- Enter the scene by combining about 200 tags such as _Opening_, _Dungeon_, ...

#### Valence-Arousal of Target Scene
- Enter the valence-arousal of the scene using sliders
  - Valence: Rises in positive scenes and falls in negative scenes
  - Arousal: Rises in active scenes and falls in passive scenes

### Target Music
- EgGMAn searches for music in Target Scene for the development game
  - Mute Artist: Enter the artist to mute
  - Mute Site: Enter the site to mute
  - Playtime: Enter the playtime of the music

## System
- Compute the embedding $\mathbf{z^p}$ for Source Music
- Compute the representative embedding $\mathbf{r^q}$ for Target Scene
  - Collect music tracks to use in the same scene as Target Scene
  - Compute the center of embedding for collected music tracks
- Predict the embedding $\mathbf{z^p}$ for Target Music from $\mathbf{z^p}$ and $\mathbf{r^q}$
- Search for music with embeddings close to $\mathbf{z^p}$

## Requirement
- [tensorflow](https://www.tensorflow.org)
- [streamlit](https://streamlit.io)
- [essentia](https://essentia.upf.edu)
- [requests](https://requests.readthedocs.io)
- [librosa](https://librosa.org)
- [yt_dlp](https://github.com/yt-dlp/yt-dlp)
- [gdown](https://github.com/wkentaro/gdown)
- [numpy](https://numpy.org)

## Licence
- [MIT License](https://en.wikipedia.org/wiki/MIT_License)
