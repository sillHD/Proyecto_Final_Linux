# 💡 Proyecto IoT con Lichee RV Dock  
### Control inteligente de iluminación con interfaz HDMI y acceso móvil

---

## 🧠 Contexto general

Este proyecto desarrolla un **sistema de control de iluminación inteligente** basado en la **Lichee RV Dock** (arquitectura RISC-V).  
El sistema integra:

- **Control físico** de luces mediante **GPIO**.  
- **Interfaz local HDMI** que muestra un **mapa 2D de la casa** con los estados de las luces.  
- **Interfaz web móvil** desarrollada con **Flask**, accesible desde cualquier dispositivo en la red local.  
- Capacidad de expansión hacia un ecosistema **IoT completo (MQTT, Node-RED, Home Assistant)**.

El objetivo es lograr un sistema **autónomo, visual y accesible** para el control doméstico desde una plataforma embebida optimizada.

---

## ⚙️ 1️⃣ Hardware involucrado

| Componente | Descripción / Función |
|:--|:--|
| **Lichee RV Dock** | Placa principal RISC-V con salida HDMI y pines GPIO |
| **Fuente de alimentación 5 V / 2 A** | Energía estable para la placa y periféricos |
| **Relés 5 V** | Control de luces o cargas mediante GPIO |
| **LEDs o bombillos de prueba** | Simulan luminarias del hogar |
| **Pantalla HDMI (7″ o monitor)** | Visualización del mapa e interfaz local |
| **WiFi o Ethernet** | Comunicación con dispositivos móviles |
| **(Opcional) Sensores DHT11 / PIR / LDR** | Extensión futura para monitoreo ambiental o detección de presencia |

---

## 🖥️ 2️⃣ Software base

| Elemento | Uso |
|:--|:--|
| **Sistema operativo** | Debian RISC-V o Tina Linux, cargado con Raspberry Pi Imager |
| **Python 3 + Flask** | Servidor web y control lógico |
| **PyQt5 / PySide6** | Interfaz local en HDMI (mapa 2D) |
| **Periphery o lgpio** | Manejo de pines GPIO desde Linux |
| **Bootstrap + JavaScript** | Interfaz móvil/web responsiva |
| **SQLite (opcional)** | Registro de estados e historial |
| **MQTT (opcional)** | Integración futura con sistemas IoT externos |

---

## 🧩 3️⃣ Arquitectura del sistema

       ┌────────────────────────────────────────────┐
       │                 Lichee RV Dock              │
       │────────────────────────────────────────────│
       │ Flask Server (Python)                      │
       │  ├── API REST / WebSocket / MQTT           │
       │  ├── Control de GPIO (luces)               │
       │  ├── Base de datos / logs                  │
       │  └── Interfaz HDMI (PyQt o webview)        │
       └─────────────┬──────────────────────────────┘
                     │ WiFi local (HTTP o MQTT)
     ┌───────────────┴────────────────┐
     │                                │
┌──────────────────┐ ┌─────────────────────┐
│ Interfaz Web Móvil│ │ Relés / Luces GPIO │
│ (HTML + JS + CSS) │ │ Control físico │
└──────────────────┘ └─────────────────────┘
---

## 💡 4️⃣ Funcionalidades principales

✅ Control manual de luces desde:
- Interfaz HDMI (PyQt)
- Interfaz móvil/web (Flask + HTML)

✅ Visualización del **mapa 2D** de la casa:
- Zonas con luces encendidas o apagadas.
- Colores dinámicos según estado GPIO.

✅ Sincronización en tiempo real entre:
- Interfaz local y web (vía Flask o WebSocket).

✅ Registro básico de acciones:
- Fecha, hora y evento (encendido/apagado).

✅ Arquitectura extensible:
- Sensores (temperatura, movimiento, luminosidad).
- Control por voz o IoT (MQTT).
- Integración con Node-RED o Home Assistant.

---

## 🧰 5️⃣ Estructura del proyecto

/home/lichee/iot_home_project/
│
├── app.py → Servidor Flask principal
├── gpio_control.py → Módulo de control GPIO
├── templates/
│ └── index.html → Interfaz web móvil
├── static/
│ ├── style.css → Estilos del panel web
│ └── script.js → Lógica de botones AJAX
├── gui_hdmi.py → Interfaz PyQt para pantalla local
├── house_map.png → Imagen del plano de la casa
├── data/
│ └── log.db → Base de datos de eventos (opcional)
└── requirements.txt → Dependencias Python

## ⚡ 6️⃣ Flujo operativo

1. La **Lichee RV Dock inicia** y lanza automáticamente el servidor Flask.  
2. La **interfaz HDMI local (PyQt)** muestra el plano de la casa con las luces.  
3. Desde un **celular o PC**, el usuario accede vía navegador:
4. Al pulsar un botón:
- Flask recibe la orden `/light/on` o `/light/off`.
- Se activa/desactiva un GPIO (relé o LED).
- Flask actualiza el estado global (y lo refleja en PyQt y en la web).

---

## 🧪 7️⃣ Etapas de desarrollo (Checklist técnica)

| Etapa | Descripción | Estado |
|:--|:--|:--:|
| [ ] 1. Instalación del sistema operativo | Cargar Debian RISC-V en microSD usando Raspberry Pi Imager. | ☐ |
| [ ] 2. Configuración del entorno Python | Instalar `python3`, `pip`, `flask`, `pyqt5`, `periphery`. | ☐ |
| [ ] 3. Prueba de servidor Flask básico | Crear y ejecutar `app.py` mostrando “Hola Lichee”. | ☐ |
| [ ] 4. Control GPIO local | Encender/apagar un LED desde Flask. | ☐ |
| [ ] 5. Interfaz web responsiva | Crear panel HTML con botones de control y feedback. | ☐ |
| [ ] 6. Interfaz HDMI local (PyQt) | Mostrar mapa 2D con luces dinámicas. | ☐ |
| [ ] 7. Comunicación bidireccional | Sincronizar estados entre PyQt y Flask. | ☐ |
| [ ] 8. Registro de eventos (SQLite) | Guardar acciones y horarios. | ☐ |
| [ ] 9. Pruebas en red local | Acceso desde un celular por WiFi y control correcto. | ☐ |
| [ ] 10. Documentación técnica | Manual de instalación, código y arquitectura. | ☐ |
| [ ] 11. Extensión IoT (opcional) | MQTT / Node-RED / Home Assistant. | ☐ |

---

## 🔒 8️⃣ Seguridad y mantenimiento

- Ejecutar Flask solo en red local (no expuesto a Internet).  
- Añadir **token o login básico** en `/login` si se requiere acceso restringido.  
- Usar **firewall (ufw)** o control de puertos.  
- Reinicio automático del servicio con `systemd`.

---

## 🚀 9️⃣ Objetivos finales del proyecto

- [ ] Mostrar el **estado de luces y sensores** en tiempo real.  
- [ ] Permitir **control local y remoto** desde cualquier dispositivo.  
- [ ] Integrar visualización por **HDMI (mapa 2D)**.  
- [ ] Mantener **bajo consumo y estabilidad** en hardware RISC-V.  
- [ ] Documentar el sistema para ampliaciones IoT futuras.

---

## 🧩 🔜 10️⃣ Extensiones futuras

- [ ] Integrar sensores de temperatura y humedad (DHT11).  
- [ ] Añadir detección de movimiento (PIR).  
- [ ] Sincronizar con aplicaciones externas vía MQTT.  
- [ ] Enviar notificaciones móviles o Telegram Bot.  
- [ ] Implementar control de voz local.

---

## ✅ Conclusión

Este proyecto demuestra cómo una **plataforma RISC-V embebida** como la **Lichee RV Dock** puede ejecutar un **sistema IoT funcional**, combinando:

- **Interfaz gráfica local (HDMI)**  
- **Control remoto web responsivo**  
- **Manejo físico de hardware (GPIO)**  
- **Arquitectura extensible hacia IoT completo**

---

### 📁 Repositorio sugerido

📂 iot_lichee_project
┣ 📂 templates
┣ 📂 static
┣ 📂 data
┣ 📜 app.py
┣ 📜 gpio_control.py
┣ 📜 gui_hdmi.py
┣ 🖼️ house_map.png
┗ 📜 README.md






