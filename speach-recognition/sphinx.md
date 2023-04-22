## speech recognition https://github.com/cmusphinx/pocketsphinx
# 
```sh
sudo apt-get install build-essential swig libpulse-dev
sudo pip install pocketsphinx
sudo apt-get install portaudio19-dev
```

```python3
from pocketsphinx import LiveSpeech
for phrase in LiveSpeech():
    print(phrase)
```
