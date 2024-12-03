# Generate speech from book
Test generate speech from book using [F5-TTS](https://github.com/SWivid/F5-TTS)

## Access the docker container in a terminal

```
docker exec -it namenode bash
```

## Run the following command to install all necessary dependencies:
```
apt-get update && apt-get install -y git curl vim build-essential libbz2-dev libncurses5-dev libncursesw5-dev libffi-dev libreadline-dev libssl-dev zlib1g-dev libsqlite3-dev liblzma-dev tk-dev libgdbm-dev libdb-dev uuid-dev xz-utils
```

## Install pyenv
```
curl https://pyenv.run | bash
```

## Open the `.bashrc` file
```
cd ~
ls -a
vim .bashrc
```

## Add the following to the bashrc
```
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
```

## Install python 3.11.5
```
pyenv install 3.11.5
```

## Go to the project path and Set the local version for your project:
```
pyenv local 3.11.5
```

### Add this line to your ~/.bashrc or ~/.zshrc for it to persist:
```
echo 'export PATH="/path/to/python3.11:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Creating the Virtual Environment
```
python -m venv venv
```

## Activate the virtual environment:
```
source venv/bin/activate
```

## F5-TTS Installation
```
# Install packages without caching to reduce memory usage:
pip install --no-cache-dir torch==2.3.0+cu118 torchaudio==2.3.0+cu118 --extra-index-url https://download.pytorch.org/whl/cu118

pip install git+https://github.com/SWivid/F5-TTS.git
```
### Install `ffmeg` and add a symlink to the venv ([source](https://github.com/jiaaro/pydub/issues/404#issuecomment-1867736059))
```
apt-get install -y ffmpeg


ln -s /usr/bin/ffprobe /media/notebooks/mia/venv/bin/ffprobe
```

# Run the script
Pass the chapter number to speech (limited by code to the 20)

```
python3.11 generate_speech_from_book.py 2
```

