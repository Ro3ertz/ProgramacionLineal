import numpy as np
from sympy import symbols, sympify
from sympy.parsing.sympy_parser import parse_expr

class GranMSimplex:
    def __init__(self):
        self.M = 1000000  # Valor grande para M
        self.tolerancia = 1e-10
        self.max_iteraciones = 100
        self.pasos = []

    def agregar_paso(self, texto):
        """Agregar un paso al proceso de solución"""
        self.pasos.append(texto)
        print(texto)

    def resolver(self, c, A, b, tipos, tipo_objetivo):
        """Método principal para resolver con Gran M"""
        self.pasos = []
        self.agregar_paso("🎯 INICIANDO MÉTODO DE LA GRAN M")
        self.agregar_paso(f"Tipo de problema: {tipo_objetivo.upper()}")
        
        # Convertir a forma estándar con variables artificiales
        resultado = self.convertir_forma_estandar(c, A, b, tipos, tipo_objetivo)
        
        if not resultado['factible']:
            return {
                'solucion': None,
                'valor_optimo': None,
                'factible': False,
                'pasos': self.pasos
            }
        
        tableau = resultado['tableau']
        base_vars = resultado['base_vars']
        var_artificiales = resultado['var_artificiales']
        
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
            self.agregar_paso(f"Elemento pivote: Fila {fila_pivote + 1}, Columna {col_pivote + 1} = {tableau[fila_pivote][col_pivote]:.4f}")
            
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
        
        # Verificar si hay variables artificiales en la base
        tiene_var_artificiales = False
        for i in range(len(base_vars)):
            if base_vars[i] in var_artificiales and abs(tableau[i][-1]) > self.tolerancia:
                tiene_var_artificiales = True
                break
        
        if tiene_var_artificiales:
            self.agregar_paso("❌ PROBLEMA INFACTIBLE - Variables artificiales en la base con valor > 0")
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

    def convertir_forma_estandar(self, c, A, b, tipos, tipo_objetivo):
        """Convertir a forma estándar con variables artificiales"""
        m = len(A)
        n = len(c)
        
        self.agregar_paso("\n📋 CONVERSIÓN A FORMA ESTÁNDAR CON VARIABLES ARTIFICIALES")
        
        # Verificar factibilidad básica (b >= 0)
        for i in range(m):
            if b[i] < 0:
                self.agregar_paso(f"❌ b[{i}] = {b[i]} < 0. Multiplicando restricción por -1")
                b[i] = -b[i]
                for j in range(n):
                    A[i][j] = -A[i][j]
                tipos[i] = '>=' if tipos[i] == '<=' else '<=' if tipos[i] == '>=' else '='
        
        # Contar variables necesarias
        num_var_holgura = sum(1 for tipo in tipos if tipo == '<=')
        num_var_exceso = sum(1 for tipo in tipos if tipo == '>=')
        num_var_artificiales = sum(1 for tipo in tipos if tipo in ['>=', '='])
        
        self.agregar_paso(f"Variables de holgura necesarias: {num_var_holgura}")
        self.agregar_paso(f"Variables de exceso necesarias: {num_var_exceso}")
        self.agregar_paso(f"Variables artificiales necesarias: {num_var_artificiales}")
        
        # Construir tableau extendido
        total_cols = n + num_var_holgura + num_var_exceso + num_var_artificiales + 1  # +1 para RHS
        tableau = []
        base_vars = []
        var_artificiales = []
        
        # Construir matriz A extendida
        for i in range(m):
            fila = [0.0] * total_cols
            # Variables originales
            for j in range(n):
                fila[j] = float(A[i][j])
            # RHS
            fila[-1] = float(b[i])
            tableau.append(fila)
        
        # Agregar variables de holgura, exceso y artificiales
        col_index = n
        
        for i in range(m):
            if tipos[i] == '<=':
                tableau[i][col_index] = 1.0  # Variable de holgura
                base_vars.append(col_index)
                col_index += 1
            elif tipos[i] == '>=':
                tableau[i][col_index] = -1.0  # Variable de exceso
                col_index += 1
                tableau[i][col_index] = 1.0  # Variable artificial
                base_vars.append(col_index)
                var_artificiales.append(col_index)
                col_index += 1
            elif tipos[i] == '=':
                tableau[i][col_index] = 1.0  # Variable artificial
                base_vars.append(col_index)
                var_artificiales.append(col_index)
                col_index += 1
        
        # Construir función objetivo con penalización Gran M
        fila_objetivo = [0.0] * total_cols
        
        # Coeficientes originales
        for j in range(n):
            fila_objetivo[j] = -float(c[j]) if tipo_objetivo == 'max' else float(c[j])
        
        # Penalizar variables artificiales
        for var_art in var_artificiales:
            fila_objetivo[var_art] = self.M if tipo_objetivo == 'max' else -self.M
        
        tableau.append(fila_objetivo)
        
        # Eliminar coeficientes M de las variables artificiales básicas
        for i in range(len(base_vars)):
            if base_vars[i] in var_artificiales:
                factor = fila_objetivo[base_vars[i]]
                for j in range(total_cols):
                    fila_objetivo[j] -= factor * tableau[i][j]
        
        self.agregar_paso(f"Variables artificiales en posiciones: {var_artificiales}")
        
        return {
            'tableau': tableau,
            'base_vars': base_vars,
            'var_artificiales': var_artificiales,
            'factible': True
        }

    def encontrar_columna_pivote(self, tableau, tipo_objetivo):
        """Encontrar columna pivote según la regla de entrada"""
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
        """Encontrar fila pivote usando la razón mínima"""
        fila_pivote = -1
        menor_ratio = float('inf')
        
        for i in range(len(tableau) - 1):
            if tableau[i][col_pivote] > self.tolerancia:
                ratio = tableau[i][-1] / tableau[i][col_pivote]
                if ratio >= 0 and ratio < menor_ratio:
                    menor_ratio = ratio
                    fila_pivote = i
        
        return fila_pivote

    def pivotear(self, tableau, fila_pivote, col_pivote):
        """Realizar operaciones de pivoteo"""
        pivot = tableau[fila_pivote][col_pivote]
        
        # Normalizar fila pivote
        for j in range(len(tableau[0])):
            tableau[fila_pivote][j] /= pivot
        
        # Eliminar en otras filas
        for i in range(len(tableau)):
            if i != fila_pivote:
                factor = tableau[i][col_pivote]
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
        self.agregar_paso("=" * 50)
        
        # Encabezados
        encabezado = "Base\t"
        for j in range(len(tableau[0]) - 1):
            encabezado += f"x{j + 1}\t"
        encabezado += "RHS"
        self.agregar_paso(encabezado)
        self.agregar_paso("-" * 50)
        
        # Filas de restricciones
        for i in range(len(tableau) - 1):
            fila = f"x{base_vars[i] + 1}\t"
            for j in range(len(tableau[0])):
                fila += f"{tableau[i][j]:.3f}\t"
            self.agregar_paso(fila)
        
        # Fila objetivo
        fila_obj = "Z\t"
        for j in range(len(tableau[0])):
            fila_obj += f"{tableau[-1][j]:.3f}\t"
        self.agregar_paso(fila_obj)


def leer_funcion_objetivo():
    """Leer y procesar la función objetivo"""
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


def leer_restricciones(variables):
    """Leer y procesar las restricciones"""
    num_restricciones = int(input("¿Cuántas restricciones deseas ingresar?: "))
    restricciones = []
    resultados = []
    relaciones = []

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
            print("Error: Formato de restricción no válido. Use '<=', '>=' o '='")
            return None, None, None

        try:
            izquierda = sympify(izquierda_str.strip())
            derecha = sympify(derecha_str.strip())
        except Exception as e:
            print(f"Error al procesar la restricción {i+1}:", e)
            return None, None, None

        # Extraer coeficientes
        coef_restriccion = []
        for var in variables:
            coef = float(izquierda.coeff(var))
            coef_restriccion.append(coef)

        restricciones.append(coef_restriccion)
        resultados.append(float(derecha))
        relaciones.append(relacion)

    return restricciones, resultados, relaciones


def mostrar_resumen(tipo, funcion_objetivo, variables, coef_objetivo,
                    matriz_restricciones, vector_resultados, relaciones):
    """Mostrar resumen del problema"""
    print("\n--- Resumen del Problema de Programación Lineal ---")
    print(f"\nFunción objetivo: {funcion_objetivo}")
    print(f"Tipo de problema: {tipo.upper()}")
    print(f"Variables detectadas: {variables}")
    print(f"Vector de coeficientes de la función objetivo: {coef_objetivo}")
    print("\nRestricciones:")
    for i, (coefs, rel, result) in enumerate(zip(matriz_restricciones, relaciones, vector_resultados)):
        restriccion_str = " + ".join([f"{coef}*{var}" for coef, var in zip(coefs, variables) if coef != 0])
        print(f"  {restriccion_str} {rel} {result}")


def ejecutar_gran_m():
    """Función principal para ejecutar el método de la Gran M"""
    print("🚀 MÉTODO DE LA GRAN M - PROGRAMACIÓN LINEAL")
    print("=" * 50)
    
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

    # Confirmar resolución
    confirmacion = input("\n¿Deseas resolver este problema con el método de la Gran M? (s/n): ").strip().lower()
    if confirmacion != 's':
        print("Programa terminado.")
        return

    # Resolver con Gran M
    print("\n" + "=" * 60)
    print("RESOLVIENDO CON MÉTODO DE LA GRAN M")
    print("=" * 60)
    
    simplex = GranMSimplex()
    resultado = simplex.resolver(coef_objetivo, matriz_restricciones, vector_resultados, relaciones, tipo)

    # Mostrar resultado final
    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    
    if resultado['factible']:
        print("✅ PROBLEMA RESUELTO EXITOSAMENTE")
        print(f"🎯 Valor óptimo: {resultado['valor_optimo']:.4f}")
        print("📍 Solución óptima:")
        for i, valor in enumerate(resultado['solucion']):
            print(f"  x{i+1} = {valor:.4f}")
    elif resultado.get('ilimitado'):
        print("❌ PROBLEMA ILIMITADO")
        print("El problema no tiene solución acotada.")
    else:
        print("❌ PROBLEMA INFACTIBLE")
        print("No existe solución que satisfaga todas las restricciones.")


# Ejecutar el programa
if __name__ == "__main__":
    ejecutar_gran_m()