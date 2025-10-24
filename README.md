#  Proyecto: Sistema Linux Embebido de Control de Iluminación Inteligente

**Autores:** 
**Curso:** Embedded Linux System Programming — 2025-2S  
**Docente:** Juan Bernardo Gómez-Mendoza  
**Plataforma:** Lichee RV Dock (RISC-V)  
**Repositorio:** [GitHub - Proyecto_Iluminacion_Lichee](#)

---

##  Descripción general

Este proyecto consiste en el diseño e implementación de un **sistema embebido basado en Linux** ejecutándose sobre una **placa Lichee RV Dock**, que controla la **intensidad de una lámpara LED** en función de la **iluminación ambiental**.

El sistema ajusta el brillo automáticamente mediante un **daemon de control** que lee un sensor de luz (LDR o BH1750) a través de I²C o ADC, y modula la salida PWM del LED.  
Además, incluye una **interfaz web local (Flask)** que permite al usuario visualizar el nivel de iluminación y cambiar el modo de operación (manual o automático).

---

##  Cómo este proyecto constituye un Sistema Operativo Embebido

Este proyecto no se limita a ejecutar un programa sobre Linux: se **construye un sistema operativo embebido funcional**, adaptado específicamente al control de iluminación.  
Esto implica intervenir y configurar **los tres niveles fundamentales** de un sistema Linux embebido.

###  1. Capa de Sistema Operativo Base
Se parte de una distribución mínima de Linux (por ejemplo, **Buildroot** o **Debian Lite**) configurada para la arquitectura **RISC-V** de la Lichee RV Dock.  
En esta capa se:
- Compilan y personalizan los **módulos del kernel** necesarios (GPIO, PWM, I²C).  
- Configura el **Device Tree** para habilitar los periféricos específicos del proyecto.  
- Se integran herramientas básicas de usuario (`busybox`, `systemd`, `python3`).  

➡️ **Resultado:** un sistema operativo Linux reducido, optimizado y con soporte de hardware específico para el sistema de iluminación.

---

### ⚙️ 2. Capa de Servicios del Sistema (System Services)
Encima del kernel se desarrollan **servicios propios del sistema embebido**:
- Un **daemon de control de iluminación** en Python/C, que lee sensores y regula la salida PWM.  
- Un servicio **systemd** (`lightcontrol.service`) que permite el arranque automático, la supervisión y el reinicio del daemon.  

➡️ **Resultado:** el sistema embebido posee sus **propios servicios gestionados** por el init system, igual que un sistema operativo completo.

---

### 💻 3. Capa de Aplicación y Usuario
Finalmente, se implementa una **interfaz web embebida (Flask)** que permite interacción directa con el sistema:
- Lectura de sensores mediante archivos virtuales en `/sys/class/pwm` y `/sys/bus/i2c/`.  
- Comunicación con el daemon mediante sockets o API REST.  
- Registro y depuración de eventos a través de `journalctl`.  

➡️ **Resultado:** el usuario interactúa con el sistema como si fuera un **OS personalizado para control de iluminación**, con su propio demonio, interfaz y logging.

---

###  En resumen
El sistema embebido integra los tres niveles clásicos de un sistema operativo Linux:

| Nivel | Elemento desarrollado |
|--------|-----------------------|
| Kernel / Device Tree | Configuración de PWM, GPIO e I²C |
| Servicios del sistema | Daemon + servicio systemd |
| Aplicaciones de usuario | API REST / Interfaz web Flask |

🔹 En conjunto, esto convierte a la Lichee RV Dock en un **sistema operativo embebido dedicado a la gestión inteligente de iluminación**, mostrando un dominio completo desde el kernel hasta la capa de usuario.

---

##  Objetivos

### Objetivo general
Implementar un sistema Linux embebido capaz de controlar dinámicamente la intensidad lumínica en función de la luz ambiental, con supervisión y control remoto local a través de una interfaz web.

### Objetivos específicos
1. Personalizar un sistema Linux mínimo (Buildroot o Debian) con soporte GPIO, PWM e I²C.
2. Implementar un **daemon de control de iluminación** en espacio de usuario.
3. Desarrollar una **API REST / interfaz web (Flask)** para el monitoreo y control manual.
4. Configurar **systemd** para iniciar automáticamente el servicio al arranque.
5. Validar el sistema mediante **pruebas unitarias e integración hardware-in-the-loop**.

---

##  Requerimientos del sistema

###  Funcionales
| ID | Descripción | Tipo |
|----|--------------|------|
| RF1 | Leer el nivel de luz ambiental mediante un sensor (LDR o BH1750). | Sensado |
| RF2 | Controlar la intensidad del LED usando PWM. | Actuación |
| RF3 | Ofrecer una interfaz web local para control y monitoreo. | Interfaz |
| RF4 | Ejecutar automáticamente el servicio al arrancar Linux. | Sistema |
| RF5 | Registrar eventos y errores en `journalctl`. | Logging |

###  No funcionales
| ID | Descripción | Tipo |
|----|--------------|------|
| RNF1 | Tiempo máximo de respuesta a solicitudes REST: **<300 ms** | Desempeño |
| RNF2 | Uso promedio de CPU < **30%** | Eficiencia |
| RNF3 | Código compatible con arquitectura **RISC-V 64 bits** | Portabilidad |
| RNF4 | Documentación en formato **Markdown + Diagrama de bloques Draw.io** | Mantenibilidad |

---

##  Arquitectura del sistema

###  Hardware

| Componente | Función | Interfaz |
|-------------|----------|-----------|
| **Lichee RV Dock** | Plataforma Linux embebida | — |
| **Sensor BH1750 / LDR+ADC** | Medición de intensidad lumínica | I²C / ADC |
| **LED + MOSFET driver** | Control de brillo por modulación PWM | GPIO / PWM |
| **Fuente DC 5V** | Alimentación del sistema | — |

### ⚙️ Software
```
+----------------------------------------------------------+
| Interfaz Web Flask |
| - API REST / Control manual |
| - Monitoreo de brillo y luz ambiental |
+----------------------------------------------------------+
| Daemon de Control de Luz |
| - Lectura de sensor |
| - Control PWM automático |
| - Logging en systemd |
+----------------------------------------------------------+
| Controladores Linux (GPIO, I2C, PWM) |
| - Device Tree y Kernel Drivers |
+----------------------------------------------------------+
| Sistema Operativo Linux Embebido |
| - Buildroot / Debian Lite |
+----------------------------------------------------------+
| Hardware Lichee RV Dock |
+----------------------------------------------------------+
```

---

##  Diagrama de bloques (Hardware)

```
     +---------------------------+
     |      Lichee RV Dock       |
     |  (Linux Embebido RISC-V)  |
     +-----------+---------------+
                 |
    I2C          | PWM
 +----------+    |    +-----------------+
 | BH1750   |----|-----| LED + MOSFET   |
 | Sensor   |          |(Luz controlada)|
 +----------+          +----------------+

```




##  Flujo de operación

1. El sistema arranca Linux y `systemd` ejecuta el **servicio de iluminación**.
2. El **daemon** configura los pines I²C y PWM.
3. Se realiza una **lectura periódica** del sensor de luz (cada 500 ms).
4. Si está en modo automático → ajusta el PWM proporcionalmente.
5. Si está en modo manual → aplica el brillo definido por el usuario vía web.
6. El usuario accede desde el navegador (`http://<IP>:8080`) al panel Flask.
7. Todos los eventos quedan registrados en `journalctl -u lightcontrol.service`.

---

##  Tecnologías y herramientas

| Categoría | Herramienta / Librería |
|------------|------------------------|
| SO Embebido | Buildroot / Debian Lite |
| Lenguaje | Python 3.10+ |
| Framework Web | Flask |
| Control de hardware | `smbus2`, `RPi.GPIO` (adaptado a Lichee) |
| Automatización | `systemd`, `bash` scripts |
| Repositorio | Git + GitHub |
| Diagramas | Draw.io / Mermaid |

---

##  Plan de verificación

| Test ID | Req. ID | Descripción | Procedimiento | Resultado esperado | Prioridad |
|----------|----------|--------------|----------------|--------------------|------------|
| TC-001 | RF1 | Verificar lectura de sensor de luz | Conectar sensor y leer valor en log | Valor en lux aumenta/disminuye según luz | Alta |
| TC-002 | RF2 | Verificar control PWM | Cambiar brillo por software | LED varía intensidad visiblemente | Alta |
| TC-003 | RF3 | Verificar interfaz web | Acceder a `http://IP:8080` | Página carga y responde en <300 ms | Media |
| TC-004 | RF4 | Verificar autoinicio | Reiniciar sistema | Servicio corre automáticamente | Alta |
| TC-005 | RF5 | Verificar registro en logs | Consultar `journalctl -u lightcontrol` | Eventos y errores registrados | Media |

---

##  Estructura del repositorio

```
┣ 📂 docs
┃ ┣ 📄 diagramas/
┃ ┣ 📄 requisitos.md
┃ ┗ 📄 pruebas.md
┣ 📂 src
┃ ┣ 📄 main.py
┃ ┣ 📄 control_daemon.py
┃ ┣ 📄 sensor.py
┃ ┗ 📄 pwm_driver.py
┣ 📂 systemd
┃ ┗ 📄 lightcontrol.service
┣ 📂 web
┃ ┣ 📄 app.py
┃ ┗ 📄 templates/
┣ 📄 README.md
┣ 📄 LICENSE
┗ 📄 requirements.txt
```

## Plan de verificación y validación 

| Fase                               | Objetivo                                           | Prueba               | Resultado esperado  |
| :--------------------------------- | :------------------------------------------------- | :------------------- | :------------------ |
| **1. Sistema operativo**           | Confirmar el arranque del entorno Debian RISC-V.   | Boot + SSH           | Sistema estable     |
| **2. GPIO**                        | Activar y desactivar un LED desde Python.          | `gpio_control.py`    | Encendido correcto  |
| **3. Servidor Flask**              | Levantar el servidor web y comprobar acceso local. | `http://<IP>:5000`   | Página accesible    |
| **4. Sensor BH1750**               | Leer valores de luminosidad por I2C.               | Script de prueba     | Lecturas correctas  |
| **5. PWM / MOSFET**                | Controlar intensidad de luz.                       | Script PWM           | Intensidad variable |
| **6. Interfaz HDMI (PyQt)**        | Mostrar mapa 2D con estado de luces.               | HDMI output          | Mapa funcional      |
| **7. Sincronización Flask ↔ PyQt** | Reflejar cambios entre interfaces.                 | Evento encendido     | Sincronía correcta  |
| **8. Red local**                   | Controlar desde celular o PC.                      | WiFi local           | Latencia mínima     |
| **9. Validación integral**         | Verificar funcionamiento total.                    | Interacción completa | Operación estable   |

## Cronograma de avance 

| Etapa | Descripción                              |     Estado     |
| :---- | :--------------------------------------- | :------------: |
| 1     | Instalación del sistema operativo        |        ✅       |
| 2     | Configuración del entorno Python y Flask |        ✅       |
| 3     | Control GPIO funcional                   | 🔄 En progreso |
| 4     | Desarrollo de interfaz HDMI (PyQt)       |   ☐ Pendiente  |
| 5     | Sincronización Flask–GUI                 |   ☐ Pendiente  |
| 6     | Integración del sensor BH1750            |   ☐ Pendiente  |
| 7     | Pruebas de red local                     |   ☐ Pendiente  |
| 8     | Documentación y presentación final       |   ☐ Pendiente  |






