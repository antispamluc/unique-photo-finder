# Unique Photo Finder v1.1 🚀

Una potente herramienta web para consolidar sus copias de seguridad desorganizadas. Diseñada para ayudarle a encontrar archivos huérfanos (archivos presentes en discos antiguos pero ausentes en su respaldo principal) y gestionar sus colecciones multimedia de manera eficiente.

## 💡 Caso de Uso - ¿Cuándo Necesita Esta Herramienta?

**Problema**: Tiene varios discos duros de respaldo acumulados durante varios años. Algunos archivos están duplicados, otros han sido renombrados en ciertos discos pero no en otros, los respaldos se hicieron en diferentes momentos, y nunca está completamente seguro de si un disco particular tiene todas sus fotos o documentos de un período específico. Todo está desorganizado, y desea **consolidar y limpiar** sin perder nada importante.

**Solución**: Esta herramienta le ayuda a:
1. **Comparar** cualquier disco con su respaldo "principal" para encontrar lo que **falta**
2. **Consolidar** todos los archivos únicos en un solo disco sin temor a perder datos
3. **Preparar** sus discos para formatearlos y crear respaldos limpios y organizados

**Flujo de trabajo**:
- Escanee todos sus discos de respaldo desorganizados
- Encuentre archivos huérfanos (archivos que existen en respaldos antiguos pero faltan en su respaldo maestro actual)
- Copie esos huérfanos a su respaldo maestro
- Una vez consolidado todo, use otra herramienta para organizar sus archivos adecuadamente
- Formatee los discos antiguos y cree respaldos frescos y limpios

## 🚀 Características

- **Escaneo Inteligente**: Indexa archivos (Fotos, Videos, Audio, Documentos) con deduplicación basada en hash.
- **Modo Actualización**: Capacidad de "Reanudar" para escanear solo archivos nuevos o modificados, significativamente más rápido para re-escaneos.
- **Detección de Huérfanos**: Compare un disco "Origen" (para limpiar) contra un disco "Caja Fuerte" (respaldo) para encontrar archivos únicos.
- **Interfaz Visual**:
    - **Cuadrícula Responsiva**: Vea miles de fotos en una cuadrícula densa de carga diferida (hasta 10 columnas).
    - **Búsqueda Instantánea**: Filtre resultados por ruta de carpeta o nombre de archivo.
    - **Vistas Previas**: Vistas previas de alta calidad para imágenes.
- **Gestión de Archivos**:
    - **Copiar/Mover**: Copia o movimiento por lotes a una carpeta de destino.
    - **Eliminar**: Mueva archivos no deseados de forma segura a la **Papelera** (soporta `gio trash` en Linux).
    - **Limpieza Automática**: Elimina automáticamente los archivos borrados de la base de datos para mantener su índice limpio.
    - **Abrir en Explorador**: Doble clic o use el botón [↗️] para abrir carpetas en su administrador de archivos del sistema operativo.
- **Privacidad Primero**: Se ejecuta localmente en su máquina. Ningún dato sale de su red.
- **Multi-idioma**: 🇫🇷 Français, 🇬🇧 English, 🇪🇸 Español.

## 🛠️ Instalación

### Requisitos Previos
- Python 3.8+
- Linux (Soporte principal) o Windows (Experimental)

### Configuración

1.  **Clonar el repositorio**
    ```bash
    git clone https://github.com/tuusuario/disk-sort-tool.git
    cd disk-sort-tool
    ```

2.  **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar la aplicación**
    ```bash
    python server.py
    ```
    O use el script de shell proporcionado:
    ```bash
    ./Lancer_Tri.sh
    ```

4.  **Abrir su navegador**
    Vaya a `http://localhost:8000`

## 📖 Guía de Uso

1.  **Inicio (Accueil)**:
    - Seleccione un disco para escanear en la sección "A Clasificar / Limpiar".
    - Seleccione su disco de respaldo en la sección "Caja Fuerte".
    - Haga clic en "Escanear" para indexar los archivos.

2.  **Resultados (Résultats)**:
    - La herramienta compara automáticamente los dos discos.
    - Navegue por la estructura de carpetas de archivos "huérfanos" (archivos en Origen no encontrados en Caja Fuerte).
    - Use la barra de búsqueda para filtrar por nombre (ej: "vacaciones", "2023").
    - Seleccione archivos/carpetas y use la barra inferior para Copiar, Mover o Eliminar.

## ⚠️ Descargo de Responsabilidad

**Este software modifica y elimina archivos.**
Aunque existen medidas de seguridad (diálogos de confirmación, verificación de hash), asegúrese siempre de tener copias de seguridad antes de realizar operaciones de eliminación o movimiento masivo. Los autores no son responsables de la pérdida de datos.

## 💻 Compatibilidad

- **Linux**: Totalmente soportado y probado. Utiliza herramientas del sistema como `lsblk` y `xdg-open`.
- **Windows**: Experimental. La funcionalidad básica debería funcionar, pero la detección de discos y la apertura de archivos pueden requerir ajustes.

## 📄 Licencia

GNU General Public License v3.0 (GPLv3).
Usted es libre de usar, modificar y distribuir este software bajo los términos de la GPLv3.
