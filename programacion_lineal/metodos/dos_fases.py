import numpy as np

class DosFasesSimplex:
    def __init__(self):
        self.tolerancia = 1e-10
        self.max_iteraciones = 100
        self.pasos = []

    def agregar_paso(self, texto):
        """Agregar un paso al proceso de solución"""
        self.pasos.append(texto)
        print(texto)

    def resolver(self, c, A, b, tipos, tipo_objetivo):
        """Método principal para resolver con Dos Fases"""
        self.pasos = []
        self.agregar_paso("🎯 INICIANDO MÉTODO DE DOS FASES")
        self.agregar_paso(f"Tipo de problema: {tipo_objetivo.upper()}")
        
        # FASE I: Encontrar solución factible básica
        self.agregar_paso("\n" + "="*60)
        self.agregar_paso("📋 FASE I: BÚSQUEDA DE SOLUCIÓN FACTIBLE")
        self.agregar_paso("="*60)
        
        resultado_fase1 = self.fase_1(c, A, b, tipos)
        
        if not resultado_fase1['factible']:
            return {
                'solucion': None,
                'valor_optimo': None,
                'factible': False,
                'pasos': self.pasos
            }
        
        # FASE II: Resolver problema original
        self.agregar_paso("\n" + "="*60)
        self.agregar_paso("🚀 FASE II: OPTIMIZACIÓN DEL PROBLEMA ORIGINAL")
        self.agregar_paso("="*60)
        
        resultado_fase2 = self.fase_2(c, resultado_fase1['tableau'], 
                                     resultado_fase1['base_vars'], 
                                     resultado_fase1['var_artificiales'], 
                                     tipo_objetivo)
        
        return resultado_fase2

    def fase_1(self, c, A, b, tipos):
        """Fase I: Minimizar suma de variables artificiales"""
        m = len(A)
        n = len(c)
        
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
        
        if num_var_artificiales == 0:
            self.agregar_paso("✅ No se necesitan variables artificiales - Problema ya factible")
            return self.construir_tableau_fase2_directo(c, A, b, tipos)
        
        # Construir tableau para Fase I
        total_cols = n + num_var_holgura + num_var_exceso + num_var_artificiales + 1
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
        
        # Función objetivo Fase I: minimizar suma de variables artificiales
        fila_objetivo_fase1 = [0.0] * total_cols
        for var_art in var_artificiales:
            fila_objetivo_fase1[var_art] = 1.0  # Minimizar suma de artificiales
        
        tableau.append(fila_objetivo_fase1)
        
        # Eliminar variables artificiales básicas de la función objetivo
        for i in range(len(base_vars)):
            if base_vars[i] in var_artificiales:
                factor = fila_objetivo_fase1[base_vars[i]]
                for j in range(total_cols):
                    fila_objetivo_fase1[j] -= factor * tableau[i][j]
        
        self.agregar_paso(f"Variables artificiales en posiciones: {var_artificiales}")
        self.agregar_paso("\n🔍 Resolviendo Fase I (minimizar suma de variables artificiales)")
        
        # Resolver Fase I con método simplex
        resultado_simplex = self.aplicar_simplex(tableau, base_vars, 'min', 1)
        
        if not resultado_simplex['convergido']:
            return {'factible': False}
        
        # Verificar factibilidad
        valor_objetivo_fase1 = tableau[-1][-1]
        self.agregar_paso(f"\n📊 Valor objetivo Fase I: {valor_objetivo_fase1:.6f}")
        
        if valor_objetivo_fase1 > self.tolerancia:
            self.agregar_paso("❌ PROBLEMA INFACTIBLE - Suma de variables artificiales > 0")
            return {'factible': False}
        
        self.agregar_paso("✅ PROBLEMA FACTIBLE - Solución básica factible encontrada")
        
        return {
            'factible': True,
            'tableau': tableau,
            'base_vars': base_vars,
            'var_artificiales': var_artificiales
        }

    def fase_2(self, c_original, tableau_fase1, base_vars, var_artificiales, tipo_objetivo):
        """Fase II: Resolver problema original"""
        
        # Eliminar variables artificiales del tableau
        self.agregar_paso("🔧 Eliminando variables artificiales del tableau")
        
        # Encontrar columnas a eliminar (variables artificiales no básicas)
        cols_a_eliminar = []
        for var_art in var_artificiales:
            if var_art not in base_vars:
                cols_a_eliminar.append(var_art)
        
        # Si hay variables artificiales básicas, verificar degeneración
        vars_art_basicas = []
        for i, var_base in enumerate(base_vars):
            if var_base in var_artificiales:
                if abs(tableau_fase1[i][-1]) < self.tolerancia:
                    vars_art_basicas.append((i, var_base))
                else:
                    self.agregar_paso("❌ Variable artificial básica con valor no cero")
                    return {'factible': False}
        
        # Eliminar columnas de variables artificiales
        tableau_fase2 = []
        for i in range(len(tableau_fase1) - 1):  # Excluir fila objetivo de Fase I
            nueva_fila = []
            for j in range(len(tableau_fase1[i])):
                if j not in var_artificiales:
                    nueva_fila.append(tableau_fase1[i][j])
            tableau_fase2.append(nueva_fila)
        
        # Ajustar índices de variables base
        nuevo_base_vars = []
        for var_base in base_vars:
            if var_base not in var_artificiales:
                # Calcular nuevo índice
                nuevo_indice = var_base
                for var_art in var_artificiales:
                    if var_art < var_base:
                        nuevo_indice -= 1
                nuevo_base_vars.append(nuevo_indice)
            else:
                # Variable artificial básica - necesita ser reemplazada
                nuevo_base_vars.append(-1)  # Marcador temporal
        
        # Manejar variables artificiales básicas degeneradas
        for i, var_base in enumerate(base_vars):
            if var_base in var_artificiales:
                # Buscar variable no básica para hacer pivoteo
                fila_actual = tableau_fase2[i]
                col_pivote = -1
                for j in range(len(fila_actual) - 1):
                    if abs(fila_actual[j]) > self.tolerancia and j not in nuevo_base_vars:
                        col_pivote = j
                        break
                
                if col_pivote != -1:
                    nuevo_base_vars[i] = col_pivote
                    self.agregar_paso(f"Reemplazando variable artificial básica con x{col_pivote + 1}")
                else:
                    # Eliminar fila redundante
                    del tableau_fase2[i]
                    del nuevo_base_vars[i]
                    self.agregar_paso(f"Eliminando restricción redundante {i + 1}")
        
        # Construir nueva función objetivo para Fase II
        num_vars_originales = len(c_original)
        nueva_fila_objetivo = [0.0] * len(tableau_fase2[0])
        
        # Coeficientes de variables originales
        for j in range(min(num_vars_originales, len(nueva_fila_objetivo) - 1)):
            nueva_fila_objetivo[j] = -float(c_original[j]) if tipo_objetivo == 'max' else float(c_original[j])
        
        tableau_fase2.append(nueva_fila_objetivo)
        
        # Eliminar variables básicas de la función objetivo
        for i in range(len(nuevo_base_vars)):
            if nuevo_base_vars[i] != -1:
                factor = nueva_fila_objetivo[nuevo_base_vars[i]]
                if abs(factor) > self.tolerancia:
                    for j in range(len(nueva_fila_objetivo)):
                        nueva_fila_objetivo[j] -= factor * tableau_fase2[i][j]
        
        self.agregar_paso("🔍 Resolviendo Fase II (problema original)")
        
        # Resolver Fase II
        resultado_simplex = self.aplicar_simplex(tableau_fase2, nuevo_base_vars, tipo_objetivo, 2)
        
        if not resultado_simplex['convergido']:
            if resultado_simplex.get('ilimitado'):
                return {
                    'solucion': None,
                    'valor_optimo': None,
                    'factible': False,
                    'ilimitado': True,
                    'pasos': self.pasos
                }
            else:
                return {'factible': False, 'pasos': self.pasos}
        
        # Extraer solución final
        solucion = self.extraer_solucion(tableau_fase2, nuevo_base_vars, num_vars_originales)
        valor_optimo = tableau_fase2[-1][-1] if tipo_objetivo == 'max' else -tableau_fase2[-1][-1]
        
        self.agregar_paso("\n🎊 SOLUCIÓN ÓPTIMA ENCONTRADA")
        self.agregar_paso(f"Valor óptimo: {valor_optimo:.4f}")
        
        return {
            'solucion': solucion,
            'valor_optimo': valor_optimo,
            'factible': True,
            'pasos': self.pasos
        }

    def aplicar_simplex(self, tableau, base_vars, tipo_objetivo, fase):
        """Aplicar algoritmo simplex estándar"""
        iteracion = 1
        
        self.mostrar_tableau(tableau, base_vars, 0, fase)
        
        while iteracion <= self.max_iteraciones:
            # Verificar optimalidad
            col_pivote = self.encontrar_columna_pivote(tableau, tipo_objetivo)
            
            if col_pivote == -1:
                self.agregar_paso("✅ CONDICIÓN DE OPTIMALIDAD ALCANZADA")
                return {'convergido': True}
            
            # Encontrar fila pivote
            fila_pivote = self.encontrar_fila_pivote(tableau, col_pivote)
            
            if fila_pivote == -1:
                self.agregar_paso("❌ PROBLEMA ILIMITADO - No hay solución acotada")
                return {'convergido': False, 'ilimitado': True}
            
            self.agregar_paso(f"\n🔄 ITERACIÓN {iteracion} - FASE {fase}")
            self.agregar_paso(f"Elemento pivote: Fila {fila_pivote + 1}, Columna {col_pivote + 1} = {tableau[fila_pivote][col_pivote]:.4f}")
            
            # Actualizar variable base
            base_vars[fila_pivote] = col_pivote
            
            # Operaciones de pivoteo
            self.pivotear(tableau, fila_pivote, col_pivote)
            self.mostrar_tableau(tableau, base_vars, iteracion, fase)
            
            iteracion += 1
        
        self.agregar_paso("❌ MÁXIMO NÚMERO DE ITERACIONES ALCANZADO")
        return {'convergido': False}

    def construir_tableau_fase2_directo(self, c, A, b, tipos):
        """Construir tableau directamente para Fase II cuando no hay variables artificiales"""
        m = len(A)
        n = len(c)
        
        # Solo variables de holgura
        tableau = []
        base_vars = []
        
        # Construir matriz extendida
        for i in range(m):
            fila = [0.0] * (n + m + 1)  # n vars originales + m vars holgura + RHS
            for j in range(n):
                fila[j] = float(A[i][j])
            fila[n + i] = 1.0  # Variable de holgura
            fila[-1] = float(b[i])
            tableau.append(fila)
            base_vars.append(n + i)
        
        # Función objetivo
        fila_objetivo = [0.0] * (n + m + 1)
        for j in range(n):
            fila_objetivo[j] = -float(c[j])  # Asumiendo maximización
        tableau.append(fila_objetivo)
        
        return {
            'factible': True,
            'tableau': tableau,
            'base_vars': base_vars,
            'var_artificiales': []
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
            else:  # minimización
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
            if base_vars[i] < num_vars_originales and base_vars[i] != -1:
                solucion[base_vars[i]] = tableau[i][-1]
        
        return solucion

    def mostrar_tableau(self, tableau, base_vars, iteracion, fase):
        """Mostrar el tableau en formato tabular"""
        self.agregar_paso(f"\n📊 TABLEAU FASE {fase} - ITERACIÓN {iteracion}")
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
            if i < len(base_vars) and base_vars[i] != -1:
                fila = f"x{base_vars[i] + 1}\t"
            else:
                fila = f"?\t"
            for j in range(len(tableau[0])):
                fila += f"{tableau[i][j]:.3f}\t"
            self.agregar_paso(fila)
        
        # Fila objetivo
        fila_obj = "Z\t"
        for j in range(len(tableau[0])):
            fila_obj += f"{tableau[-1][j]:.3f}\t"
        self.agregar_paso(fila_obj)