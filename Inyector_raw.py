import os
import struct

#Diseñado por ZARF

# === CONFIGURA AQUÍ ===
carpeta_originales = r"ruta_wpx_originales"
carpeta_madre_raws = r"ruta_raw_modificados"
carpeta_salida_modificados = r"ruta_wpx_modificados"
# -----------------------

def inyectar_bloques(ruta_orig, carpeta_raws, ruta_out):
    with open(ruta_orig, "rb") as f:
        data_original = bytearray(f.read())

    # 1. Leer tabla de offsets original
    offset = 4
    punteros = []
    patron_fin = b'\x01\x00\x00\x00'

    while offset + 4 <= len(data_original):
        bloque = data_original[offset:offset+4]
        if bloque == patron_fin:
            break
        punteros.append(struct.unpack('<I', bloque)[0])
        offset += 4

    print(f"Punteros encontrados: {len(punteros)}")

    nombre_base = os.path.splitext(os.path.basename(ruta_orig))[0]
    data_modificada = bytearray(data_original)

# 2. Validar e inyectar cada bloque
    for i, inicio in enumerate(punteros):
        if i + 1 < len(punteros):
            fin = punteros[i+1]
        else:
            fin = len(data_original)

        ruta_raw = os.path.join(carpeta_raws, f"{nombre_base}_{i:03d}.raw")
        if not os.path.exists(ruta_raw):
            continue

        with open(ruta_raw, "rb") as rf:
            nuevo_data = rf.read()

        header_en_afs = data_original[inicio : inicio + 54]
        header_del_raw = nuevo_data[:54]

        if header_en_afs == header_del_raw:
            inicio_real = inicio  
            print(f"[{i:03d}] Coincide header -> inyección +0 bytes")
        else:
            inicio_real = inicio + 54 
            print(f"[{i:03d}] No coincide -> inyeccion +54 bytes")
        
        tamano_original = fin - inicio_real

        ruta_raw = os.path.join(carpeta_raws, f"{nombre_base}_{i:03d}.raw")

        if not os.path.exists(ruta_raw):
            print(f"[AVISO] No existe {ruta_raw}, se deja original.")
            continue

        with open(ruta_raw, "rb") as rf:
            nuevo_data = rf.read()

        # 3. Comprobación de tamaño
        if len(nuevo_data) > tamano_original:
            print(f"[ERROR] Bloque {i:03d}: {len(nuevo_data)} bytes > permitido {tamano_original} bytes. Se cancela.")
            return



        # 5. Reemplazar en el archivo
        if header_en_afs == header_del_raw:
            data_a_inyectar = nuevo_data
        else:
            data_a_inyectar = nuevo_data[54:] if len(nuevo_data) > 54 else nuevo_data

        data_modificada[inicio_real: inicio_real + len(nuevo_data)] = nuevo_data

    # 6. Guardar archivo modificado
    with open(ruta_out, "wb") as out:
        out.write(data_modificada)

    print(f"\n¡Archivo modificado guardado en: {ruta_out}")

if __name__ == "__main__":
    os.makedirs(carpeta_salida_modificados, exist_ok=True)

    # Cada subcarpeta en salida = un archivo a reconstruir
    for nombre_carpeta in os.listdir(carpeta_madre_raws):
        ruta_carpeta_raws_actual = os.path.join(carpeta_madre_raws, nombre_carpeta)

        if not os.path.isdir(ruta_carpeta_raws_actual):
            continue

        ruta_orig_actual = os.path.join(carpeta_originales, nombre_carpeta + ".wpx")
        ruta_out_actual = os.path.join(carpeta_salida_modificados, nombre_carpeta + ".wpx")

        if not os.path.exists(ruta_orig_actual):
            print(f"No se encontró original para {nombre_carpeta}")
            continue

        print(f"\n=== Procesando {nombre_carpeta} ===")
        inyectar_bloques(ruta_orig_actual, ruta_carpeta_raws_actual, ruta_out_actual)