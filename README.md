# Descargador YouTube

Aplicación de escritorio mínima para descargar videos de YouTube como MP3 (audio) o MP4 (video).

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![yt-dlp](https://img.shields.io/badge/yt--dlp-FF0000?style=flat)
![Licencia](https://img.shields.io/badge/licencia-MIT-green?style=flat)
![Último commit](https://img.shields.io/github/last-commit/ViceAguilera/Py_downloader?style=flat)

## Descripción

Interfaz gráfica sencilla (Tkinter) que envuelve a `yt-dlp` y `ffmpeg`. Pegas el link, eliges el formato y la descarga queda en `Descargas\musica`, con barra de progreso.

## Características

- MP3: mejor calidad disponible, con portada y metadatos incrustados.
- MP4: prefiere H.264 + AAC para que abra en cualquier reproductor.
- Descarga solo el video del link, aunque venga dentro de una playlist.
- Barra de progreso, botón para abrir la carpeta de destino y descarga en un hilo aparte para no congelar la ventana.
- Descarga con Enter y validación de que el link empiece con `http://` o `https://`.

## Tecnologías

- Python 3.12 (solo biblioteca estándar: `tkinter`, sin dependencias de pip)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) y [ffmpeg](https://ffmpeg.org/)

## Requisitos

- Windows (usa `os.startfile` para abrir la carpeta).
- Python 3.12.
- `yt-dlp` y `ffmpeg` en el PATH:

```powershell
winget install yt-dlp.yt-dlp   # instala también ffmpeg
```

## Uso

Doble clic en `descargador.pyw` (o `pythonw descargador.pyw`), pega el link, elige MP3 o MP4 y presiona **Descargar**.

Si deja de funcionar, casi siempre se arregla actualizando `yt-dlp`, ya que YouTube cambia con frecuencia:

```powershell
winget upgrade yt-dlp.yt-dlp
```

## Mejoras pendientes

- Descarga en FLAC como tercera opción: en `construir_comando` bastaría con `-x --audio-format flac`. YouTube entrega audio con pérdida (Opus/AAC), por lo que el FLAC no gana calidad; solo sirve como formato sin pérdida para editar o archivar.

## Estructura del proyecto

```
descargador.pyw   # Aplicación completa (interfaz y llamada a yt-dlp)
```

## Licencia

Distribuido bajo la licencia MIT. Ver [LICENSE](LICENSE).

## Autor

**Vicente Aguilera Arias** — [Portafolio](https://portfolio.iamsirius.cl) · [GitHub](https://github.com/ViceAguilera) · [LinkedIn](https://www.linkedin.com/in/vicenteaguilera/)
