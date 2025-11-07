# src/test_riscv.py

import platform

print("="*40)
print("✅ Script de Prueba Ejecutado Exitosamente en Lichee RV")
print("="*40)

# Imprimir información del sistema para verificación
print(f"Arquitectura del procesador: {platform.machine()}")
print(f"Sistema Operativo: {platform.system()}")
print(f"Versión de Python: {platform.python_version()}")

# Aseguramos que la ejecución se detiene y no se convierte en un daemon accidental
print("\n[INFO] Prueba completada.")