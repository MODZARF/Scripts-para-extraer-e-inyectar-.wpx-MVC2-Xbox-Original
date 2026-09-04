> **Disclaimer:** Esta herramienta no contiene ni distribuye ningún archivo del juego. Necesitas una copia legal de Marvel vs Capcom 2 para obtener los archivos `.wpx` originales. Este proyecto no está afiliado con Capcom o Marvel.

### Características
- Trabajo por lotes (batch)
- Validación de tamaño para evitar crashes
- Padding automático con 0x00
- No recalcula punteros, 100% seguro para el formato

### ¿Cómo funciona?
El formato `.wpx` es un contenedor sin compresión. El script analiza el header para encontrar la tabla de punteros para cada bloque de audio.

- `Extractor_raw.py`: Extrae cada bloque como `.raw` individual.
- `Inyector_raw.py`: Reemplaza los bloques originales por tus `.raw` modificados, respetando el tamaño original.

### Requisitos
- Python 3.8+
- Ninguna librería externa

### Uso

#### 1. Extraer
Edita las variables de rutas en `Extractor_raw.py` y ejecútalo.
El script extraerá en la ruta de salida los audios (wav) como `.raw` sin headers, en carpetas con el mismo nombre del `.wpx`.

#### 2. Inyectar
Edita las variables de rutas en `Inyector_raw.py` y ejecútalo.
El script tomará los `.raw` modificados y los insertará en su correspondiente `.wpx` y los guardará en la ruta de salida.

### Importante
Los `.raw` modificados deben ser de igual o menor tamaño al original. Si son más grandes, serán rechazados para evitar corrupción del archivo.
