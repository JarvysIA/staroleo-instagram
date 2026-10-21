// Uso: node transcrever.mjs audio.wav > palavras.json   (wav mono 16 kHz: ffmpeg -i video.mp4 -ac 1 -ar 16000 audio.wav)
// Para áudio com mais de ~30 s, corte em pedaços de até 28 s e some o deslocamento (o modelo perde o começo em arquivos longos).
import os from 'os';
const H = os.homedir();
const { pipeline, env } = await import(`${H}/asr/node_modules/@huggingface/transformers/src/transformers.js`);
const fs = (await import('fs')).default;
const wavefile = (await import(`${H}/asr/node_modules/wavefile/dist/wavefile.js`)).default;
env.allowRemoteModels = false;
env.localModelPath = `${H}/asr/node_modules/sts-whisper-small/models/`;
const asr = await pipeline('automatic-speech-recognition', 'Xenova/whisper-small', { dtype: 'q8' });
const wav = new wavefile.WaveFile(fs.readFileSync(process.argv[2]));
wav.toBitDepth('32f'); wav.toSampleRate(16000);
let s = wav.getSamples(); if (Array.isArray(s)) s = s[0];
const out = await asr(s, { language: 'portuguese', task: 'transcribe', return_timestamps: 'word', chunk_length_s: 30 });
console.log(JSON.stringify(out));
