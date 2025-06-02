import numpy as np
from sympy import symbols, sympify, Matrix
from sympy.parsing.sympy_parser import parse_expr

class SimplexTradicional:
    def __init__(self):
        self.tolerancia = 1e-10
        self.max_iteraciones = 100
        self.pasos = []

    def agregar_paso(self, texto):
        """Agregar un paso al proceso de solución"""
        self.pasos.append(texto)
        print(texto)

    def resolver(self, c, A, b, tipos, tipo_objetivo):
        """Método principal para resolver con Simplex tradicional"""
        self.pasos = []
        self.agregar_paso("🎯 INICIANDO MÉTODO SIMPLEX TRADICIONAL")
        self.agregar_paso(f"Tipo de problema: {tipo_objetivo.upper()}")
        
        # Verificar si el problema está en forma estándar
        if not self.verificar_forma_estandar(tipos):
            self.agregar_paso("❌ PROBLEMA NO ESTÁ EN FORMA ESTÁNDAR")
            self.agregar_paso("💡 Use el método de Gran M o Dos Fases para restricciones >= o =")
            return {
                'solucion': None,
                'valor_optimo': None,
                'factible': False,
                'mensaje': 'Problema no está en forma estándar',
                'pasos': self.pasos
            }
        
        # Convertir a forma estándar para Simplex tradicional
        resultado = self.convertir_forma_estandar_simple(c, A, b, tipo_objetivo)
        
        if not resultado['factible']:
            return {
                'solucion': None,
                'valor_optimo': None,
                'factible': False,
                'pasos': self.pasos
            }
        
        tableau = resultado['tableau']
        base_vars = resultado['base_vars']
        
        self.mostrar_tableau(tableau, base_vars, 0)
        
        # Aplicar método simplex
        iteracion = 1
        while iteracion <= self.max_iteraciones:
            # Verificar optimalidad
            col_pivote = self.encontrar_columna_pivote(tableau, tipo_objetivo)
            
            if col_pivote == -1:
                self.agregar_paso("✅ CONDICIÓN DE OPTIMALIDAD ALCANZADA")
                break
            
            # Encontrar fila pivote
            fila_pivote = self.encontrar_fila_pivote(tableau, col_pivote)
            
            if fila_pivote == -1:
                self.agregar_paso("❌ PROBLEMA ILIMITADO - No hay solución acotada")
                return {
                    'solucion': None,
                    'valor_optimo': None,
                    'factible': False,
                    'ilimitado': True,
                    'pasos': self.pasos
                }
            
            self.agregar_paso(f"\n🔄 ITERACIÓN {iteracion}")
            self.agregar_paso(f"Variable que entra: x{col_pivote + 1}")
            self.agregar_paso(f"Variable que sale: x{base_vars[fila_pivote] + 1}")
            self.agregar_paso(f"Elemento pivote: {tableau[fila_pivote][col_pivote]:.4f}")
            
            # Actualizar variable base
            base_vars[fila_pivote] = col_pivote
            
            # Operaciones de pivoteo
            self.pivotear(tableau, fila_pivote, col_pivote)
            self.mostrar_tableau(tableau, base_vars, iteracion)
            
            iteracion += 1
        
        if iteracion > self.max_iteraciones:
            self.agregar_paso("❌ MÁXIMO NÚMERO DE ITERACIONES ALCANZADO")
            return {
                'solucion': None,
                'valor_optimo': None,
                'factible': False,
                'pasos': self.pasos
            }
        
        # Extraer solución
        solucion = self.extraer_solucion(tableau, base_vars, len(c))
        valor_optimo = tableau[-1][-1] if tipo_objetivo == 'max' else -tableau[-1][-1]
        
        self.agregar_paso("\n🎊 SOLUCIÓN ÓPTIMA ENCONTRADA")
        self.agregar_paso(f"Valor óptimo: {valor_optimo:.4f}")
        
        return {
            'solucion': solucion,
            'valor_optimo': valor_optimo,
            'factible': True,
            'pasos': self.pasos
        }

    def verificar_forma_estandar(self, tipos):
        """Verificar si todas las restricciones son <="""
        return all(tipo == '<=' for tipo in tipos)

    def convertir_forma_estandar_simple(self, c, A, b, tipo_objetivo):
        """Convertir a forma estándar agregando variables de holgura"""
        m = len(A)
        n = len(c)
        
        self.agregar_paso("\n📋 CONVERSIÓN A FORMA ESTÁNDAR")
        
        # Verificar factibilidad básica (b >= 0)
        for i in range(m):
            if b[i] < 0:
                self.agregar_paso(f"❌ b[{i}] = {b[i]} < 0. Multiplicando restricción por -1")
                b[i] = -b[i]
                for j in range(n):
                    A[i][j] = -A[i][j]
        
        # Construir tableau con variables de holgura
        total_cols = n + m + 1  # vars originales + vars holgura + RHS
        tableau = []
        base_vars = []
        
        # Construir restricciones con variables de holgura
        for i in range(m):
            fila = [0.0] * total_cols
            # Variables originales
            for j in range(n):
                fila[j] = float(A[i][j])
            # Variable de holgura
            fila[n + i] = 1.0
            # RHS
            fila[-1] = float(b[i])
            tableau.append(fila)
            base_vars.append(n + i)  # Variable de holgura es básica
        
        # Función objetivo
        fila_objetivo = [0.0] * total_cols
        for j in range(n):
            fila_objetivo[j] = -float(c[j]) if tipo_objetivo == 'max' else float(c[j])
        
        tableau.append(fila_objetivo)
        
        self.agregar_paso(f"Variables de holgura agregadas: s1, s2, ..., s{m}")
        self.agregar_paso(f"Variables básicas iniciales: {[f's{i+1}' for i in range(m)]}")
        
        return {
            'tableau': tableau,
            'base_vars': base_vars,
            'factible': True
        }

    def encontrar_columna_pivote(self, tableau, tipo_objetivo):
        """Encontrar columna pivote (variable que entra)"""
        fila_objetivo = tableau[-1]
        col_pivote = -1
        mejor_valor = 0
        
        for j in range(len(fila_objetivo) - 1):
            if tipo_objetivo == 'max':
                if fila_objetivo[j] < mejor_valor:
                    mejor_valor = fila_objetivo[j]
                    col_pivote = j
            else:
                if fila_objetivo[j] > mejor_valor:
                    mejor_valor = fila_objetivo[j]
                    col_pivote = j
        
        return col_pivote

    def encontrar_fila_pivote(self, tableau, col_pivote):
        """Encontrar fila pivote (variable que sale) usando razón mínima"""
        fila_pivote = -1
        menor_ratio = float('inf')
        
        self.agregar_paso(f"\n🔍 Calculando razones para variable entrante x{col_pivote + 1}:")
        
        for i in range(len(tableau) - 1):
            if tableau[i][col_pivote] > self.tolerancia:
                ratio = tableau[i][-1] / tableau[i][col_pivote]
                self.agregar_paso(f"  Fila {i + 1}: {tableau[i][-1]:.3f} / {tableau[i][col_pivote]:.3f} = {ratio:.3f}")
                if ratio >= 0 and ratio < menor_ratio:
                    menor_ratio = ratio
                    fila_pivote = i
            else:
                self.agregar_paso(f"  Fila {i + 1}: No válida (coeficiente ≤ 0)")
        
        if fila_pivote != -1:
            self.agregar_paso(f"🎯 Razón mínima: {menor_ratio:.3f} en fila {fila_pivote + 1}")
        
        return fila_pivote

    def pivotear(self, tableau, fila_pivote, col_pivote):
        """Realizar operaciones de pivoteo"""
        pivot = tableau[fila_pivote][col_pivote]
        self.agregar_paso(f"\n⚙️ Operaciones de pivoteo:")
        self.agregar_paso(f"Normalizando fila pivote (dividiendo por {pivot:.4f})")
        
        # Normalizar fila pivote
        for j in range(len(tableau[0])):
            tableau[fila_pivote][j] /= pivot
        
        # Eliminar en otras filas
        self.agregar_paso("Eliminando en otras filas:")
        for i in range(len(tableau)):
            if i != fila_pivote:
                factor = tableau[i][col_pivote]
                if abs(factor) > self.tolerancia:
                    self.agregar_paso(f"  Fila {i + 1}: R{i + 1} - ({factor:.3f}) * R{fila_pivote + 1}")
                    for j in range(len(tableau[0])):
                        tableau[i][j] -= factor * tableau[fila_pivote][j]

    def extraer_solucion(self, tableau, base_vars, num_vars_originales):
        """Extraer la solución final"""
        solucion = [0.0] * num_vars_originales
        
        for i in range(len(base_vars)):
            if base_vars[i] < num_vars_originales:
                solucion[base_vars[i]] = tableau[i][-1]
        
        return solucion

    def mostrar_tableau(self, tableau, base_vars, iteracion):
        """Mostrar el tableau en formato tabular"""
        self.agregar_paso(f"\n📊 TABLEAU - ITERACIÓN {iteracion}")
        self.agregar_paso("=" * 60)
        
        # Encabezados
        encabezado = "Base\t\t"
        for j in range(len(tableau[0]) - 1):
            encabezado += f"x{j + 1}\t"
        encabezado += "RHS"
        self.agregar_paso(encabezado)
        self.agregar_paso("-" * 60)
        
        # Filas de restricciones
        for i in range(len(tableau) - 1):
            if base_vars[i] < len(tableau[0]) - 1:
                fila = f"x{base_vars[i] + 1}\t\t"
            else:
                fila = f"s{base_vars[i] - len(tableau[0]) + 2}\t\t"
            
            for j in range(len(tableau[0])):
                fila += f"{tableau[i][j]:.3f}\t"
            self.agregar_paso(fila)
        
        # Fila objetivo
        fila_obj = "Z\t\t"
        for j in range(len(tableau[0])):
            fila_obj += f"{tableau[-1][j]:.3f}\t"
        self.agregar_paso(fila_obj)


# Paso 1: Leer función objetivo (manteniendo tu estructura)
def leer_funcion_objetivo():
    entrada = input("Introduce la función objetivo: ").strip()

    if entrada.lower().startswith("max"):
        tipo = "max"
        expr_str = entrada[3:].strip()
    elif entrada.lower().startswith("min"):
        tipo = "min"
        expr_str = entrada[3:].strip()
    else:
        expr_str = entrada
        tipo = input("¿El problema es de Maximización o Minimización? (Escribe 'max' o 'min'): ").strip().lower()

    try:
        expr = sympify(expr_str)
    except Exception as e:
        print("Error al analizar la función objetivo:", e)
        return None, None, None, None

    variables = sorted(expr.free_symbols, key=lambda x: x.name)
    coeficientes = [float(expr.coeff(var)) for var in variables]

    return tipo, expr, variables, coeficientes


# Paso 2: Leer restricciones (mejorado para manejar <=, >= y =)
def leer_restricciones(variables):
    num_restricciones = int(input("¿Cuántas restricciones deseas ingresar?: "))
    restricciones = []
    resultados = []
    relaciones = []

    print("\n💡 Formatos aceptados:")
    print("  • Para ≤: usar '<='  (ej: 2*x1 + 3*x2 <= 10)")
    print("  • Para ≥: usar '>='  (ej: x1 + x2 >= 5)")
    print("  • Para =: usar '='   (ej: x1 + 2*x2 = 8)")
    print()

    for i in range(num_restricciones):
        restr = input(f"Restricción {i + 1}: ").strip()

        # Determinar el tipo de relación
        if "<=" in restr:
            izquierda_str, derecha_str = restr.split("<=")
            relacion = "<="
        elif ">=" in restr:
            izquierda_str, derecha_str = restr.split(">=")
            relacion = ">="
        elif "=" in restr and "<=" not in restr and ">=" not in restr:
            izquierda_str, derecha_str = restr.split("=")
            relacion = "="
        else:
            print("❌ Error: Formato de restricción no válido. Use '<=', '>=' o '='")
            return None, None, None

        try:
            izquierda = sympify(izquierda_str.strip())
            derecha = sympify(derecha_str.strip())
        except Exception as e:
            print(f"❌ Error al procesar la restricción {i+1}:", e)
            return None, None, None

        # Extraer coeficientes
        coef_restriccion = []
        for var in variables:
            coef = float(izquierda.coeff(var))
            coef_restriccion.append(coef)

        restricciones.append(coef_restriccion)
        resultados.append(float(derecha))
        relaciones.append(relacion)

    # Convertir a matrices (manteniendo compatibilidad con tu código)
    matriz_coef = Matrix(restricciones)
    vector_resultados = Matrix([[r] for r in resultados])

    return matriz_coef, vector_resultados, relaciones


# Paso 3: Mostrar resumen (mejorado)
def mostrar_resumen(tipo, funcion_objetivo, variables, coef_objetivo,
                    matriz_restricciones, vector_resultados, relaciones):
    print("\n" + "="*60)
    print("📋 RESUMEN DEL PROBLEMA DE PROGRAMACIÓN LINEAL")
    print("="*60)
    print(f"\n🎯 Función objetivo: {funcion_objetivo}")
    print(f"📊 Tipo de problema: {tipo.upper()}")
    print(f"🔢 Variables detectadas: {variables}")
    print(f"📈 Coeficientes de la función objetivo: {coef_objetivo}")
    
    print("\n📋 Restricciones:")
    for i, rel in enumerate(relaciones):
        restriccion_str = " + ".join([f"{coef}*{var}" for coef, var in zip(matriz_restricciones.row(i), variables) if coef != 0])
        print(f"  {i+1}. {restriccion_str} {rel} {vector_resultados.row(i)[0]}")
    
    print(f"\n📐 Matriz de coeficientes de las restricciones:")
    print(matriz_restricciones)
    print(f"\n📊 Vector de resultados:")
    print(vector_resultados)
    
    # Verificar compatibilidad con Simplex tradicional
    tiene_no_estandar = any(rel in ['>=', '='] for rel in relaciones)
    if tiene_no_estandar:
        print("\n⚠️  ADVERTENCIA:")
        print("   Este problema contiene restricciones >= o =")
        print("   El método Simplex tradicional solo maneja restricciones <=")
        print("   💡 Considere usar el método de Gran M o Dos Fases")


# Ejecución del programa mejorado
def ejecutar_programa_mejorado():
    print("🚀 MÉTODO SIMPLEX TRADICIONAL MEJORADO")
    print("="*50)
    
    # Leer función objetivo
    tipo, funcion_objetivo, variables, coef_objetivo = leer_funcion_objetivo()
    if funcion_objetivo is None:
        return

    # Leer restricciones
    matriz_restricciones, vector_resultados, relaciones = leer_restricciones(variables)
    if matriz_restricciones is None:
        return

    # Mostrar resumen
    mostrar_resumen(tipo, funcion_objetivo, variables, coef_objetivo,
                    matriz_restricciones, vector_resultados, relaciones)

    # Preguntar si desea continuar
    continuar = input("\n¿Desea resolver este problema? (s/n): ").strip().lower()
    if continuar != 's':
        print("👋 Programa terminado.")
        return

    # Convertir datos para el solver
    A_lista = [[float(matriz_restricciones[i, j]) for j in range(len(variables))] 
               for i in range(matriz_restricciones.rows)]
    b_lista = [float(vector_resultados[i, 0]) for i in range(vector_resultados.rows)]

    # Resolver con Simplex
    print("\n" + "="*60)
    print("🔧 RESOLVIENDO CON MÉTODO SIMPLEX")
    print("="*60)
    
    simplex = SimplexTradicional()
    resultado = simplex.resolver(coef_objetivo, A_lista, b_lista, relaciones, tipo)

    # Mostrar resultado final
    print("\n" + "="*60)
    print("🏆 RESULTADO FINAL")
    print("="*60)
    
    if resultado['factible']:
        if 'mensaje' in resultado:
            print(f"📝 Mensaje: {resultado['mensaje']}")
        else:
            print("✅ PROBLEMA RESUELTO EXITOSAMENTE")
            print(f"🎯 Valor óptimo: {resultado['valor_optimo']:.4f}")
            print("\n📍 Solución óptima:")
            for i, valor in enumerate(resultado['solucion']):
                print(f"  {variables[i]} = {valor:.4f}")
    elif resultado.get('ilimitado'):
        print("❌ PROBLEMA ILIMITADO")
        print("📈 La función objetivo puede crecer indefinidamente")
    else:
        print("❌ PROBLEMA NO FACTIBLE O NO RESUELTO")
        if 'mensaje' in resultado:
            print(f"📝 Razón: {resultado['mensaje']}")


# Ejecutar el programa
if __name__ == "__main__":
    ejecutar_programa_mejorado()