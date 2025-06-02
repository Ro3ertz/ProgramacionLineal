"""
Problemas de ejemplo para demostrar los métodos de programación lineal
Incluye casos que muestran diferentes situaciones especiales
"""

from metodos import SimplexTradicional, GranMSimplex, DosFasesSimplex
from utils.casos_especiales import ManejadorCasosEspeciales

class ProblemasTest:
    def __init__(self):
        self.problemas = {
            'problema_1': self.problema_estandar,
            'problema_2': self.problema_gran_m,
            'problema_3': self.problema_dos_fases,
            'problema_4': self.problema_degenerado,
            'problema_5': self.problema_ilimitado,
            'problema_6': self.problema_infactible,
            'problema_7': self.problema_soluciones_multiples
        }

    def ejecutar_todos_los_problemas(self):
        """Ejecutar todos los problemas de ejemplo"""
        print("🚀 EJECUTANDO SUITE DE PROBLEMAS DE EJEMPLO")
        print("=" * 60)
        
        for nombre, problema_func in self.problemas.items():
            print(f"\n{'='*20} {nombre.upper()} {'='*20}")
            try:
                problema_func()
            except Exception as e:
                print(f"❌ Error en {nombre}: {e}")
            print("=" * 60)

    def problema_estandar(self):
        """
        PROBLEMA 1: Problema estándar para Simplex tradicional
        
        Maximizar Z = 3x1 + 2x2
        Sujeto a:
            2x1 + x2 <= 6
            x1 + 2x2 <= 8
            x1, x2 >= 0
        
        Solución esperada: x1 = 2, x2 = 2, Z = 10
        """
        print("📋 PROBLEMA 1: Simplex Tradicional")
        print("Maximizar Z = 3x1 + 2x2")
        print("Restricciones:")
        print("  2x1 + x2 <= 6")
        print("  x1 + 2x2 <= 8")
        print("  x1, x2 >= 0")
        
        # Datos del problema
        c = [3, 2]
        A = [[2, 1], [1, 2]]
        b = [6, 8]
        tipos = ['<=', '<=']
        tipo_objetivo = 'max'
        
        # Resolver con Simplex tradicional
        solver = SimplexTradicional()
        resultado = solver.resolver(c, A, b, tipos, tipo_objetivo)
        
        # Analizar casos especiales
        if resultado['factible']:
            print(f"\n✅ Resultado: x1 = {resultado['solucion'][0]:.4f}, x2 = {resultado['solucion'][1]:.4f}")
            print(f"💰 Valor óptimo: Z = {resultado['valor_optimo']:.4f}")
            print("🎯 Solución esperada: x1 = 2, x2 = 2, Z = 10")

    def problema_gran_m(self):
        """
        PROBLEMA 2: Problema que requiere método Gran M
        
        Maximizar Z = 3x1 + 2x2
        Sujeto a:
            x1 + x2 >= 1
            2x1 + x2 <= 6
            x1 + 2x2 <= 8
            x1, x2 >= 0
        
        Solución esperada: x1 = 2, x2 = 2, Z = 10
        """
        print("📋 PROBLEMA 2: Método Gran M")
        print("Maximizar Z = 3x1 + 2x2")
        print("Restricciones:")
        print("  x1 + x2 >= 1    # Requiere variable artificial")
        print("  2x1 + x2 <= 6")
        print("  x1 + 2x2 <= 8")
        print("  x1, x2 >= 0")
        
        # Datos del problema
        c = [3, 2]
        A = [[1, 1], [2, 1], [1, 2]]
        b = [1, 6, 8]
        tipos = ['>=', '<=', '<=']
        tipo_objetivo = 'max'
        
        # Resolver con Gran M
        solver = GranMSimplex()
        resultado = solver.resolver(c, A, b, tipos, tipo_objetivo)
        
        if resultado['factible']:
            print(f"\n✅ Resultado: x1 = {resultado['solucion'][0]:.4f}, x2 = {resultado['solucion'][1]:.4f}")
            print(f"💰 Valor óptimo: Z = {resultado['valor_optimo']:.4f}")

    def problema_dos_fases(self):
        """
        PROBLEMA 3: Problema que requiere método Dos Fases
        
        Minimizar Z = 2x1 + 3x2
        Sujeto a:
            x1 + x2 = 4     # Igualdad requiere variable artificial
            2x1 + x2 >= 6   # >= requiere variable artificial
            x1, x2 >= 0
        
        Solución esperada: x1 = 2, x2 = 2, Z = 10
        """
        print("📋 PROBLEMA 3: Método Dos Fases")
        print("Minimizar Z = 2x1 + 3x2")
        print("Restricciones:")
        print("  x1 + x2 = 4      # Igualdad")
        print("  2x1 + x2 >= 6    # Mayor o igual")
        print("  x1, x2 >= 0")
        
        # Datos del problema
        c = [2, 3]
        A = [[1, 1], [2, 1]]
        b = [4, 6]
        tipos = ['=', '>=']
        tipo_objetivo = 'min'
        
        # Resolver con Dos Fases
        solver = DosFasesSimplex()
        resultado = solver.resolver(c, A, b, tipos, tipo_objetivo)
        
        if resultado['factible']:
            print(f"\n✅ Resultado: x1 = {resultado['solucion'][0]:.4f}, x2 = {resultado['solucion'][1]:.4f}")
            print(f"💰 Valor óptimo: Z = {resultado['valor_optimo']:.4f}")

    def problema_degenerado(self):
        """
        PROBLEMA 4: Problema con degeneración
        
        Maximizar Z = x1 + x2
        Sujeto a:
            x1 + x2 <= 2
            x1 <= 0      # Esta restricción causa degeneración
            x2 <= 2
            x1, x2 >= 0
        """
        print("📋 PROBLEMA 4: Degeneración")
        print("Maximizar Z = x1 + x2")
        print("Restricciones:")
        print("  x1 + x2 <= 2")
        print("  x1 <= 0        # Causa degeneración")
        print("  x2 <= 2")
        print("  x1, x2 >= 0")
        
        # Datos del problema
        c = [1, 1]
        A = [[1, 1], [1, 0], [0, 1]]
        b = [2, 0, 2]
        tipos = ['<=', '<=', '<=']
        tipo_objetivo = 'max'
        
        # Resolver y analizar degeneración
        solver = SimplexTradicional()
        resultado = solver.resolver(c, A, b, tipos, tipo_objetivo)
        
        if resultado['factible']:
            print(f"\n✅ Resultado: x1 = {resultado['solucion'][0]:.4f}, x2 = {resultado['solucion'][1]:.4f}")
            print(f"💰 Valor óptimo: Z = {resultado['valor_optimo']:.4f}")
            print("⚠️  Degeneración esperada: x1 = 0 (variable básica en cero)")

    def problema_ilimitado(self):
        """
        PROBLEMA 5: Problema ilimitado (no acotado)
        
        Maximizar Z = x1 + x2
        Sujeto a:
            -x1 + x2 <= 1   # Restricción que no acota superiormente
            x1, x2 >= 0
        """
        print("📋 PROBLEMA 5: Problema Ilimitado")
        print("Maximizar Z = x1 + x2")
        print("Restricciones:")
        print("  -x1 + x2 <= 1   # No acota la función objetivo")
        print("  x1, x2 >= 0")
        
        # Datos del problema
        c = [1, 1]
        A = [[-1, 1]]
        b = [1]
        tipos = ['<=']
        tipo_objetivo = 'max'
        
        # Resolver - debería detectar ilimitación
        solver = SimplexTradicional()
        resultado = solver.resolver(c, A, b, tipos, tipo_objetivo)
        
        if resultado.get('ilimitado'):
            print("✅ Ilimitación detectada correctamente")
        else:
            print("❌ No se detectó la ilimitación")

    def problema_infactible(self):
        """
        PROBLEMA 6: Problema infactible
        
        Maximizar Z = x1 + x2
        Sujeto a:
            x1 + x2 >= 3
            x1 + x2 <= 1    # Contradicción: no puede ser >= 3 y <= 1
            x1, x2 >= 0
        """
        print("📋 PROBLEMA 6: Problema Infactible")
        print("Maximizar Z = x1 + x2")
        print("Restricciones:")
        print("  x1 + x2 >= 3")
        print("  x1 + x2 <= 1    # Contradicción con la anterior")
        print("  x1, x2 >= 0")
        
        # Datos del problema
        c = [1, 1]
        A = [[1, 1], [1, 1]]
        b = [3, 1]
        tipos = ['>=', '<=']
        tipo_objetivo = 'max'
        
        # Resolver con Gran M - debería detectar infactibilidad
        solver = GranMSimplex()
        resultado = solver.resolver(c, A, b, tipos, tipo_objetivo)
        
        if not resultado['factible']:
            print("✅ Infactibilidad detectada correctamente")
        else:
            print("❌ No se detectó la infactibilidad")

    def problema_soluciones_multiples(self):
        """
        PROBLEMA 7: Problema con soluciones óptimas múltiples
        
        Maximizar Z = x1 + x2
        Sujeto a:
            x1 + x2 <= 3    # La función objetivo es paralela a esta restricción
            x1 <= 2
            x2 <= 2
            x1, x2 >= 0
        """
        print("📋 PROBLEMA 7: Soluciones Óptimas Múltiples")
        print("Maximizar Z = x1 + x2")
        print("Restricciones:")
        print("  x1 + x2 <= 3    # Paralela a la función objetivo")
        print("  x1 <= 2")
        print("  x2 <= 2")
        print("  x1, x2 >= 0")
        
        # Datos del problema
        c = [1, 1]
        A = [[1, 1], [1, 0], [0, 1]]
        b = [3, 2, 2]
        tipos = ['<=', '<=', '<=']
        tipo_objetivo = 'max'
        
        # Resolver y analizar soluciones múltiples
        solver = SimplexTradicional()
        resultado = solver.resolver(c, A, b, tipos, tipo_objetivo)
        
        if resultado['factible']:
            print(f"\n✅ Una solución: x1 = {resultado['solucion'][0]:.4f}, x2 = {resultado['solucion'][1]:.4f}")
            print(f"💰 Valor óptimo: Z = {resultado['valor_optimo']:.4f}")
            print("⚠️  Soluciones múltiples esperadas: Cualquier punto en x1 + x2 = 3")

    def ejecutar_problema_especifico(self, nombre_problema):
        """Ejecutar un problema específico por nombre"""
        if nombre_problema in self.problemas:
            print(f"Ejecutando {nombre_problema}...")
            self.problemas[nombre_problema]()
        else:
            print(f"❌ Problema '{nombre_problema}' no encontrado")
            print(f"Problemas disponibles: {list(self.problemas.keys())}")

    def comparar_metodos(self):
        """Comparar los tres métodos en un mismo problema"""
        print("🔄 COMPARACIÓN DE MÉTODOS")
        print("=" * 50)
        print("Problema: Maximizar Z = 3x1 + 2x2")
        print("Restricciones: x1 + x2 >= 1, 2x1 + x2 <= 6, x1 + 2x2 <= 8")
        
        # Datos del problema
        c = [3, 2]
        A = [[1, 1], [2, 1], [1, 2]]
        b = [1, 6, 8]
        tipos = ['>=', '<=', '<=']
        tipo_objetivo = 'max'
        
        metodos = [
            ("Simplex Tradicional", SimplexTradicional()),
            ("Gran M", GranMSimplex()),
            ("Dos Fases", DosFasesSimplex())
        ]
        
        for nombre, solver in metodos:
            print(f"\n--- {nombre} ---")
            resultado = solver.resolver(c, A, b, tipos, tipo_objetivo)
            if resultado['factible']:
                print(f"✅ Resuelto: Z = {resultado['valor_optimo']:.4f}")
            else:
                print(f"❌ {resultado.get('mensaje', 'No factible')}")


# Función para ejecutar desde línea de comandos
def main():
    """Función principal para ejecutar problemas de ejemplo"""
    problemas = ProblemasTest()
    
    print("🎯 PROBLEMAS DE EJEMPLO - PROGRAMACIÓN LINEAL")
    print("=" * 60)
    print("1. Ejecutar todos los problemas")
    print("2. Ejecutar problema específico")
    print("3. Comparar métodos")
    print("4. Salir")
    
    while True:
        opcion = input("\nSeleccione una opción (1-4): ").strip()
        
        if opcion == '1':
            problemas.ejecutar_todos_los_problemas()
        elif opcion == '2':
            print(f"\nProblemas disponibles: {list(problemas.problemas.keys())}")
            nombre = input("Ingrese el nombre del problema: ").strip()
            problemas.ejecutar_problema_especifico(nombre)
        elif opcion == '3':
            problemas.comparar_metodos()
        elif opcion == '4':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    main()