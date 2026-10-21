#!/usr/bin/env bash
# Prepara o ambiente para produzir as peças da Star (rodar uma vez por sessão).
set -e
AQUI="$(cd "$(dirname "$0")" && pwd)"
mkdir -p ~/.fonts && cp "$AQUI"/fonts/*.ttf ~/.fonts/ && fc-cache -f >/dev/null 2>&1 || true
python3 -c "import pillow_heif" 2>/dev/null || pip install -q --break-system-packages pillow-heif
which ffmpeg >/dev/null || { echo "ffmpeg ausente"; exit 1; }
# Transcrição local (0 crédito): Whisper small via transformers.js
if [ ! -d "$HOME/asr/node_modules/sts-whisper-small" ]; then
  mkdir -p "$HOME/asr" && cd "$HOME/asr" && npm init -y >/dev/null && npm i -s sts-whisper-small @huggingface/transformers@3.7.1 wavefile >/dev/null
fi
echo "ambiente pronto"
