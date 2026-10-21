# Código das peças da Star Óleo

1. `bash _codigo/setup.sh` (fontes Barlow Condensed e Manrope, pillow-heif e transcrição local).
2. Imagens: `from star_lib import *` (stories, feed, carrosséis, prévia). Ver docstrings.
3. Reels de vídeo já gravado (cliente/dica, 4:5): `from reel_lib import make_reel` (exemplo em `referencia/build_l2_reels.py`).
4. Transcrição com tempo das palavras (0 crédito): `node _codigo/transcrever.mjs audio.wav` (wav mono 16 kHz, pedaços de até 28 s).
5. Reels de fotos com locução da ElevenLabs: ver `referencia/reel_fotos_locucao_r15mil.py` (o melhor modelo) e `reel_fotos_locucao_kicks.py`; adapte os caminhos.
6. Controle do acervo: `_controle/acervo.json` (arquivos conhecidos e usados).
Regras de conteúdo e marca: doc `claude/star-marketing-operacao.md` no Projeto "Star Óleo".
