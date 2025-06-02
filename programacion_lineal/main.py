#!/usr/bin/env python3
"""
PROYECTO FINAL - PROGRAMACIÓN LINEAL
Implementación completa de métodos de resolución

Autor: [Tu nombre]
Fecha: [Fecha actual]
Curso: [Tu curso]

Este proyecto implementa tres métodos principales de programación lineal:
1. Método Simplex Tradicional
2. Método de la Gran M  
3. Método de Dos Fases

Además incluye manejo completo de casos especiales y ejemplos de prueba.
"""

import sys
import os

# Importar módulos personalizados
from metodos import SimplexTradicional, GranMSimplex, DosFasesSimplex
from utils.validadores import leer_funcion_objetivo, leer_restricciones, mostrar_resumen
from utils.casos_especiales import ManejadorCasosEspeciales
from ejemplos.problemas_test import ProblemasTest

class SuiteProgramacionLineal:
    def __init__(self):
        self.manejador_casos = ManejadorCasosEspeciales()
        self.problemas_test = ProblemasTest()
        
    def mostrar_menu_principal(self):
        """Mostrar el menú principal de opciones"""
        print("\n" + "="*60)
        print("🚀 SUITE DE PROGRAMACIÓN LINEAL")
        print("="*60)
        print("1. 📝 Resolver problema personalizado")
        print("2. 📋 Ejecutar problemas de ejemplo")
        print("3. 🔍 Comparar métodos de resolución")
        print("4. 📚 Información sobre métodos")
        print("5. 🧪 Modo avanzado (casos especiales)")
        print("6. 🌐 Abrir interfaz web (Streamlit)")
        print("7. 🚪 Salir")
        print("="*60)

    def resolver_problema_personalizado(self):
        """Modo interactivo para resolver problema personalizado"""
        print("\n🎯 RESOLVER PROBLEMA PERSONALIZADO")
        print("="*50)
        
        # Leer problema del usuario
        tipo, expr, variables, coeficientes = leer_funcion_objetivo()
        if expr is None:
            return
        
        restricciones, resultados, relaciones = leer_restricciones(variables)
        if restricciones is None:
            return
        
        # Mostrar resumen
        mostrar_resumen(tipo, expr, variables, coeficientes, restricciones, resultados, relaciones)
        
        # Seleccionar método
        metodo = self.seleccionar_metodo(relaciones)
        if metodo is None:
            return
        
        # Confirmar resolución
        confirmacion = input("\n¿Resolver este problema? (s/n): ").strip().lower()
        if confirmacion != 's':
            print("👋 Cancelado por el usuario")
            return
        
        # Resolver problema
        print("\n" + "="*60)
        print("🔧 RESOLVIENDO PROBLEMA")
        print("="*60)
        
        resultado = metodo.resolver(coeficientes, restricciones, resultados, relaciones, tipo)
        
        # Mostrar resultado y análisis
        self.mostrar_resultado_completo(resultado, variables, metodo.__class__.__name__)

    def seleccionar_metodo(self, relaciones):
        """Seleccionar método de resolución apropiado"""
        print("\n🔧 SELECCIÓN DE MÉTODO:")
        
        # Análisis automático
        tiene_no_estandar = any(rel in ['>=', '='] for rel in relaciones)
        
        if not tiene_no_estandar:
            print("✅ Problema en forma estándar - Todos los métodos aplicables")
        else:
            print("⚠️  Problema requiere variables artificiales")
            print("💡 Recomendado: Método Gran M o Dos Fases")
        
        print("\nMétodos disponibles:")
        print("1. Simplex Tradicional (solo problemas en forma estándar)")
        print("2. Método de la Gran M (todos los problemas)")
        print("3. Método de Dos Fases (todos los problemas)")
        print("4. Selección automática")
        
        opcion = input("Seleccione método (1-4): ").strip()
        
        if opcion == '1':
            return SimplexTradicional()
        elif opcion == '2':
            return GranMSimplex()
        elif opcion == '3':
            return DosFasesSimplex()
        elif opcion == '4':
            if tiene_no_estandar:
                print("🤖 Selección automática: Método de Dos Fases")
                return DosFasesSimplex()
            else:
                print("🤖 Selección automática: Simplex Tradicional")
                return SimplexTradicional()
        else:
            print("❌ Opción inválida")
            return None

    def mostrar_resultado_completo(self, resultado, variables, nombre_metodo):
        """Mostrar resultado completo con análisis de casos especiales"""
        print("\n" + "="*60)
        print("🏆 RESULTADO FINAL")
        print("="*60)
        print(f"Método utilizado: {nombre_metodo}")
        
        if resultado['factible']:
            if 'mensaje' in resultado:
                print(f"📝 Mensaje: {resultado['mensaje']}")
            else:
                print("✅ PROBLEMA RESUELTO EXITOSAMENTE")
                print(f"\n💰 Valor óptimo: Z = {resultado['valor_optimo']:.6f}")
                print("\n📍 Solución óptima:")
                for i, valor in enumerate(resultado['solucion']):
                    print(f"  {variables[i]} = {valor:.6f}")
                
                # Análisis adicional si está disponible
                if 'pasos' in resultado:
                    casos = input("\n¿Mostrar análisis de casos especiales? (s/n): ").strip().lower()
                    if casos == 's':
                        print(self.manejador_casos.generar_reporte_casos_especiales())
        
        elif resultado.get('ilimitado'):
            print("❌ PROBLEMA ILIMITADO")
            print("📈 La función objetivo puede crecer indefinidamente")
            print("💡 Verifique las restricciones del problema")
        
        else:
            print("❌ PROBLEMA NO FACTIBLE")
            print("🚫 No existe solución que satisfaga todas las restricciones")
            if 'mensaje' in resultado:
                print(f"📝 Razón: {resultado['mensaje']}")

    def ejecutar_problemas_ejemplo(self):
        """Ejecutar suite de problemas de ejemplo"""
        print("\n📋 PROBLEMAS DE EJEMPLO")
        print("="*50)
        print("1. Ejecutar todos los problemas")
        print("2. Problema estándar (Simplex)")
        print("3. Problema Gran M")
        print("4. Problema Dos Fases")
        print("5. Caso degenerado")
        print("6. Problema ilimitado")
        print("7. Problema infactible")
        print("8. Soluciones múltiples")
        print("9. Volver al menú principal")
        
        opcion = input("Seleccione opción (1-9): ").strip()
        
        if opcion == '1':
            self.problemas_test.ejecutar_todos_los_problemas()
        elif opcion in ['2', '3', '4', '5', '6', '7', '8']:
            problemas_map = {
                '2': 'problema_1', '3': 'problema_2', '4': 'problema_3',
                '5': 'problema_4', '6': 'problema_5', '7': 'problema_6',
                '8': 'problema_7'
            }
            self.problemas_test.ejecutar_problema_especifico(problemas_map[opcion])
        elif opcion == '9':
            return
        else:
            print("❌ Opción inválida")

    def comparar_metodos(self):
        """Comparar los tres métodos en problemas específicos"""
        print("\n🔄 COMPARACIÓN DE MÉTODOS")
        print("="*50)
        self.problemas_test.comparar_metodos()

    def mostrar_informacion_metodos(self):
        """Mostrar información detallada sobre los métodos"""
        print("\n📚 INFORMACIÓN SOBRE MÉTODOS")
        print("="*60)
        
        info = """
🔧 MÉTODO SIMPLEX TRADICIONAL:
   • Para problemas en forma estándar (restricciones ≤)
   • Más rápido y directo
   • Limitado a problemas ya factibles
   
🔍 MÉTODO DE LA GRAN M:
   • Maneja restricciones ≥ y =
   • Introduce variables artificiales con penalización M
   • Puede tener problemas numéricos con M muy grande
   
🚀 MÉTODO DE DOS FASES:
   • Separa factibilidad de optimización
   • Más estable numéricamente que Gran M
   • Ideal para problemas complejos con múltiples tipos de restricciones
   
📊 CASOS ESPECIALES MANEJADOS:
   • Degeneración: Variables básicas con valor cero
   • Soluciones múltiples: Infinitas soluciones óptimas
   • Problemas ilimitados: Función objetivo sin cota
   • Problemas infactibles: Sin solución posible
        """
        print(info)

    def modo_avanzado(self):
        """Modo avanzado para análisis detallado"""
        print("\n🧪 MODO AVANZADO")
        print("="*50)
        print("1. Análisis paso a paso detallado")
        print("2. Detectar casos especiales manualmente")
        print("3. Aplicar regla de Bland (anti-ciclado)")
        print("4. Análisis de sensibilidad")
        print("5. Volver al menú principal")
        
        opcion = input("Seleccione opción (1-5): ").strip()
        
        if opcion == '1':
            print("💡 Use el modo normal - ya incluye pasos detallados")
        elif opcion == '2':
            print("💡 Los casos especiales se detectan automáticamente durante la resolución")
        elif opcion == '3':
            print("💡 La regla de Bland se aplica automáticamente en casos degenerados")
        elif opcion == '4':
            print("💡 El análisis de sensibilidad básico se incluye en los resultados")
        elif opcion == '5':
            return
        else:
            print("❌ Opción inválida")

    def abrir_interfaz_web(self):
        """Abrir la interfaz web con Streamlit"""
        print("\n🌐 INTERFAZ WEB CON STREAMLIT")
        print("="*50)
        print("La interfaz web ofrece:")
        print("✨ Diseño moderno y atractivo")
        print("📊 Gráficos interactivos")
        print("🎛️ Configuración visual de problemas")
        print("📱 Funciona en cualquier dispositivo")
        
        continuar = input("\n¿Desea abrir la interfaz web? (s/n): ").strip().lower()
        
        if continuar == 's':
            try:
                import subprocess
                print("\n🚀 Iniciando servidor web...")
                subprocess.run([sys.executable, "run_streamlit.py"])
            except Exception as e:
                print(f"❌ Error al abrir interfaz web: {e}")
                print("💡 Ejecute manualmente: python run_streamlit.py")
        else:
            print("👍 Puede ejecutar la interfaz web cuando guste con: python run_streamlit.py")

    def ejecutar(self):
        """Ejecutar la aplicación principal"""
        print("🎯 BIENVENIDO AL PROYECTO DE PROGRAMACIÓN LINEAL")
        print("Implementación completa de métodos Simplex")
        
        while True:
            try:
                self.mostrar_menu_principal()
                opcion = input("Seleccione una opción (1-6): ").strip()
                
                if opcion == '1':
                    self.resolver_problema_personalizado()
                elif opcion == '2':
                    self.ejecutar_problemas_ejemplo()
                elif opcion == '3':
                    self.comparar_metodos()
                elif opcion == '4':
                    self.mostrar_informacion_metodos()
                elif opcion == '5':
                    self.modo_avanzado()
                elif opcion == '6':
                    self.abrir_interfaz_web()
                elif opcion == '7':
                    print("\n👋 ¡Gracias por usar la Suite de Programación Lineal!")
                    print("🎓 Proyecto desarrollado para el curso de Investigación de Operaciones")
                    break
                else:
                    print("❌ Opción inválida. Seleccione 1-7.")
                
                input("\nPresione Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Programa interrumpido por el usuario")
                break
            except Exception as e:
                print(f"\n❌ Error inesperado: {e}")
                print("💡 Contacte al desarrollador si el problema persiste")

def verificar_dependencias():
    """Verificar que las dependencias estén instaladas"""
    try:
        import sympy
        import numpy
        print("✅ Dependencias verificadas")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("💡 Instale con: pip install sympy numpy")
        return False

def main():
    """Función principal"""
    # Banner del proyecto
    print("="*60)
    print("🎯 PROYECTO FINAL - PROGRAMACIÓN LINEAL")
    print("="*60)
    print("📚 Métodos implementados:")
    print("   • Simplex Tradicional")
    print("   • Método de la Gran M")
    print("   • Método de Dos Fases")
    print("📋 Casos especiales manejados:")
    print("   • Degeneración, Soluciones múltiples")
    print("   • Problemas ilimitados e infactibles")
    print("="*60)
    
    # Verificar dependencias
    if not verificar_dependencias():
        return
    
    # Ejecutar aplicación
    app = SuiteProgramacionLineal()
    app.ejecutar()

if __name__ == "__main__":
    main()