import os
import struct

#Diseñado por ZARF

# === CONFIGURA AQUÍ ===
carpeta_entrada = r"ruta_wpx_originales"
ruta_salida = r"ruta_raw"
# -----------------------


def extraer_bloques(ruta_in, ruta_out):
    if not os.path.exists(ruta_in):
        print(f"No se encontró: {ruta_in}")
        return

    os.makedirs(ruta_out, exist_ok=True)

    with open(ruta_in, "rb") as f:
        data = f.read()

    # 1. Leer tabla de punteros (misma lógica que usaste)
    offset = 4
    punteros = []
    patron_fin = b'\x01\x00\x00\x00'

    while offset + 4 <= len(data):
        bloque = data[offset:offset+4]
        if bloque == patron_fin:
            break
        # Little Endian
        valor = struct.unpack('<I', bloque)[0]
        punteros.append(valor)
        offset += 4

    print(f"Encontrados {len(punteros)} punteros: {punteros}")

    if not punteros:
        print("No se encontró tabla.")
        return

    nombre_base = os.path.splitext(os.path.basename(ruta_in))[0]

    # 2. Extraer cada bloque
    for i, inicio in enumerate(punteros):
        if i + 1 < len(punteros):
            fin = punteros[i+1] # termina donde empieza el siguiente
        else:
            fin = len(data) # último bloque hasta el final del archivo

        bloque_audio = data[inicio:fin]

        nombre_salida = f"{nombre_base}_{i:03d}.raw"
        ruta_completa_out = os.path.join(ruta_out, nombre_salida)

        with open(ruta_completa_out, "wb") as out:
            out.write(bloque_audio)

        print(f"[{i:03d}] {hex(inicio)} -> {hex(fin)} ({len(bloque_audio)} bytes) => {nombre_salida}")

    print("\n¡Extracción completa en RAW!")

if __name__ == "__main__":
    # Busca todos los.wpx
    for archivo in os.listdir(carpeta_entrada):
        if archivo.lower().endswith(".wpx"):
            ruta_in = os.path.join(carpeta_entrada, archivo)

            # Crea subcarpeta con el mismo nombre del wpx
            nombre_base = os.path.splitext(archivo)[0]
            ruta_out_individual = os.path.join(ruta_salida, nombre_base)

            print(f"\n=== Procesando {archivo} ===")
            extraer_bloques(ruta_in, ruta_out_individual)