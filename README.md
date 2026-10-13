# Descargador YouTube

App de escritorio mínima para bajar videos de YouTube como **MP3** (audio) o **MP4** (video).
Los archivos quedan en `Descargas\musica`.

## Requisitos

- Python 3.12 (trae `tkinter`, no hay dependencias de pip)
- `yt-dlp` y `ffmpeg` en el PATH:

```powershell
winget install yt-dlp.yt-dlp   # instala también ffmpeg
```

## Uso

Doble clic en `descargador.pyw`, pega el link, elige MP3 o MP4 y presiona **Descargar** (o Enter).

- MP3: mejor calidad disponible, con portada y metadatos incrustados.
- MP4: prefiere H.264 + AAC para que abra en cualquier reproductor.
- Solo baja el video del link, aunque venga dentro de una playlist.

## Si deja de funcionar

YouTube cambia seguido y rompe los descargadores. Casi siempre se arregla actualizando:

```powershell
winget upgrade yt-dlp.yt-dlp
```

## Mejoras pendientes

- **Descarga en FLAC**: agregar una tercera opción junto a MP3/MP4. En `construir_comando` bastaría con
  `-x --audio-format flac`. Ojo: YouTube entrega audio con pérdida (Opus/AAC), así que el FLAC no
  gana calidad respecto al original; solo sirve si se quiere un formato sin pérdida para editar o archivar.
