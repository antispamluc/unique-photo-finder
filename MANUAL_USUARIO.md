# Manual de Usuario - Buscador de Fotos Únicas

Bienvenido al manual de usuario del **Buscador de Fotos Únicas** (Unique Photo Finder). Este software le ayuda a identificar archivos **huérfanos** - archivos que están presentes en un disco de origen pero **faltan** en su disco de respaldo. El objetivo es ayudarle a completar sus copias de seguridad y organizar sus colecciones multimedia.

---

## 🏁 Inicio Rápido

1.  **Iniciar la aplicación**: Haga doble clic en `Lancer_Tri.sh` o ejecute `./Lancer_Tri.sh` en una terminal.
2.  **Abrir navegador**: La interfaz se abre automáticamente en `http://localhost:8000`.
3.  **Elegir idioma**: Haga clic en las banderas 🇫🇷 / 🇬🇧 / 🇪🇸 en la esquina superior derecha.

---

## 🏠 Pestaña Inicio (Escanear)

Aquí es donde indexa el contenido de sus discos duros.

### 1. Seleccionar Discos
- **Disco a Clasificar (Origen)**: El disco que desea limpiar u organizar.
- **Respaldo Principal (Maestro)**: Su disco de respaldo principal (el que contiene "todo").

### 2. Opciones de Escaneo
- **Modo "Actualización"** (Marcado por defecto):
  - ✅ Recomendado. Escanea solo archivos nuevos o modificados. Mucho más rápido.
  - Desmarque para forzar un re-escaneo completo (si sospecha errores).
- **Filtros**: Elija qué tipos de archivos escanear (Fotos, Videos, Audio, Documentos).

### 3. Iniciar Escaneo
Haga clic en el botón **"ESCANEAR"**. Aparece una barra de progreso. Puede pausar o detener el escaneo en cualquier momento.

---

## 📊 Pestaña Resultados (Comparar)

Una vez completados los escaneos, vaya a esta pestaña para encontrar "huérfanos" (archivos presentes en Origen pero NO en Caja Fuerte).

### 1. Configuración
- **Disco Origen**: Seleccione el disco a limpiar.
- **Disco Caja Fuerte**: Seleccione el disco de referencia.
- **Filtros**: Marque los tipos de archivos a mostrar.
- **Comparar Todo**: Marque esta casilla para seleccionar todo a la vez.

### 2. Iniciar Búsqueda
Haga clic en **"🔍 Buscar huérfanos"**.

### 3. Gestionar Resultados
- **Lista de Carpetas** (izquierda): Haga clic en una carpeta para ver su contenido.
- **Cuadrícula de Archivos** (centro):
  - Vea sus fotos y videos.
  - Marque los archivos a procesar (o use "Seleccionar Todo").
  - Doble clic en una imagen para verla en tamaño completo (si es compatible).
  - Clic derecho para abrir el archivo en su explorador de archivos.

### 4. Acciones (abajo)
- **🗑️ ELIMINAR**: Envía los archivos seleccionados a la papelera.
  - *Nota: La base de datos se actualiza automáticamente.*
- **COPIAR / MOVER**:
  - Elija una carpeta de destino.
  - Haga clic en "COPIAR" (duplica) o active "Modo MOVER" luego haga clic en "MOVER" (mueve y elimina el original).

---

## ❓ Preguntas Frecuentes (FAQ)

**P: ¿Eliminé archivos manualmente, pero siguen apareciendo?**
R: El software actualiza su base de datos cuando elimina a través de la interfaz. Si elimina manualmente a través del explorador de Windows/Linux, ejecute un escaneo en modo "Actualización" para refrescar la lista.

**P: ¿El escaneo está atascado?**
R: Verifique la consola (F12 en el navegador) o la terminal para ver si hay errores. Puede detener y reiniciar el servidor de forma segura.

**P: ¿Dónde están mis archivos eliminados?**
R: Están en la Papelera de su sistema, a menos que la papelera no esté disponible (discos de red, etc.), en cuyo caso podrían eliminarse permanentemente (el software le advertirá).
