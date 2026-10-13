"""Descargador simple de YouTube a MP3/MP4 usando yt-dlp + ffmpeg."""

import os
import queue
import re
import shutil
import subprocess
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk

CARPETA_DESTINO = Path.home() / "Downloads" / "musica"
PCT_RE = re.compile(r"^PCT\s+([\d.]+)%")

# Evita que se abra una ventana de consola por cada descarga en Windows.
SIN_CONSOLA = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def construir_comando(ytdlp: str, url: str, formato: str) -> list[str]:
    comando = [
        ytdlp,
        "--no-playlist",
        "--newline",
        "--encoding", "utf-8",
        "--progress-template", "download:PCT %(progress._percent_str)s",
        "-o", str(CARPETA_DESTINO / "%(title)s.%(ext)s"),
    ]
    if formato == "mp3":
        comando += [
            "-x", "--audio-format", "mp3", "--audio-quality", "0",
            "--embed-thumbnail", "--embed-metadata",
        ]
    else:
        # H.264 primero: AV1/VP9 no se reproducen en todos los reproductores de Windows.
        comando += [
            "-f", "bv*[vcodec^=avc1]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b",
            "--merge-output-format", "mp4",
        ]
    # "--" impide que una URL que empiece con "-" se interprete como opción.
    return comando + ["--", url]


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Descargador YouTube")
        self.geometry("560x260")
        self.minsize(460, 240)
        self.eventos: queue.Queue = queue.Queue()
        self.ytdlp = shutil.which("yt-dlp")

        marco = ttk.Frame(self, padding=16)
        marco.pack(fill="both", expand=True)

        ttk.Label(marco, text="Link del video").pack(anchor="w")
        self.url = tk.StringVar()
        entrada = ttk.Entry(marco, textvariable=self.url)
        entrada.pack(fill="x", pady=(4, 10))
        entrada.focus()
        entrada.bind("<Return>", lambda _e: self.descargar())

        fila = ttk.Frame(marco)
        fila.pack(fill="x")
        self.formato = tk.StringVar(value="mp3")
        ttk.Radiobutton(fila, text="MP3 (audio)", value="mp3", variable=self.formato).pack(side="left")
        ttk.Radiobutton(fila, text="MP4 (video)", value="mp4", variable=self.formato).pack(side="left", padx=12)
        ttk.Button(fila, text="Abrir carpeta", command=self.abrir_carpeta).pack(side="right")
        self.boton = ttk.Button(fila, text="Descargar", command=self.descargar)
        self.boton.pack(side="right", padx=8)

        self.progreso = ttk.Progressbar(marco, maximum=100)
        self.progreso.pack(fill="x", pady=(14, 6))
        self.estado = tk.StringVar()
        ttk.Label(marco, textvariable=self.estado, wraplength=520).pack(anchor="w")
        ttk.Label(marco, text=f"Destino: {CARPETA_DESTINO}", foreground="gray").pack(anchor="w", side="bottom")

        if self.ytdlp:
            self.estado.set("Pega un link y presiona Descargar.")
        else:
            self.estado.set("No encuentro yt-dlp. Instálalo con: winget install yt-dlp.yt-dlp")
            self.boton.state(["disabled"])

        self.after(100, self.procesar_eventos)

    def descargar(self) -> None:
        url = self.url.get().strip()
        if not self.ytdlp or "disabled" in self.boton.state():
            return
        if not url.startswith(("https://", "http://")):
            self.estado.set("El link debe empezar con https://")
            return
        CARPETA_DESTINO.mkdir(parents=True, exist_ok=True)
        self.boton.state(["disabled"])
        self.progreso["value"] = 0
        self.estado.set("Iniciando…")
        comando = construir_comando(self.ytdlp, url, self.formato.get())
        threading.Thread(target=self.ejecutar, args=(comando,), daemon=True).start()

    def ejecutar(self, comando: list[str]) -> None:
        ultimo_error = ""
        try:
            proceso = subprocess.Popen(
                comando,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=SIN_CONSOLA,
            )
            for linea in proceso.stdout:
                linea = linea.strip()
                if match := PCT_RE.match(linea):
                    self.eventos.put(("progreso", float(match.group(1))))
                elif linea.startswith("ERROR"):
                    ultimo_error = linea
                elif "[ExtractAudio]" in linea or "[Merger]" in linea:
                    self.eventos.put(("estado", "Convirtiendo…"))
            proceso.wait()
            if proceso.returncode == 0:
                self.eventos.put(("fin", "Listo. Guardado en la carpeta musica."))
            else:
                self.eventos.put(("fin", ultimo_error or f"Falló (código {proceso.returncode})."))
        except OSError as error:
            self.eventos.put(("fin", f"No pude ejecutar yt-dlp: {error}"))

    def procesar_eventos(self) -> None:
        while not self.eventos.empty():
            tipo, valor = self.eventos.get_nowait()
            if tipo == "progreso":
                self.progreso["value"] = valor
                self.estado.set(f"Descargando… {valor:.0f}%")
            elif tipo == "estado":
                self.estado.set(valor)
            elif tipo == "fin":
                self.estado.set(valor)
                self.boton.state(["!disabled"])
                if valor.startswith("Listo"):
                    self.progreso["value"] = 100
                    self.url.set("")
        self.after(100, self.procesar_eventos)

    def abrir_carpeta(self) -> None:
        CARPETA_DESTINO.mkdir(parents=True, exist_ok=True)
        os.startfile(CARPETA_DESTINO)


if __name__ == "__main__":
    App().mainloop()
