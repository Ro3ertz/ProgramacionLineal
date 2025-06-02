import numpy as np

class ManejadorCasosEspeciales:
    def __init__(self, tolerancia=1e-10):
        self.tolerancia = tolerancia
        self.casos_detectados = []

    def detectar_degeneracion(self, tableau, base_vars):
        """
        Detectar degeneración: Variable básica con valor cero
        
        Args:
            tableau: Matriz del tableau simplex
            base_vars: Lista de variables básicas
            
        Returns:
            dict: Información sobre degeneración detectada
        """
        degenerado = False
        variables_degeneradas = []
        
        for i, var_base in enumerate(base_vars):
            valor_rhs = tableau[i][-1]  # Valor RHS
            if abs(valor_rhs) < self.tolerancia:
                degenerado = True
                variables_degeneradas.append(var_base)
                mensaje = f"⚠️  DEGENERACIÓN: Variable básica x{var_base+1} = {valor_rhs:.6f} ≈ 0"
                print(mensaje)
                self.casos_detectados.append(mensaje)
        
        if degenerado:
            print(f"📋 Total de variables degeneradas: {len(variables_degeneradas)}")
            print("💡 Esto puede causar ciclado en el algoritmo simplex")
        
        return {
            'degenerado': degenerado,
            'variables_degeneradas': variables_degeneradas,
            'num_degeneradas': len(variables_degeneradas)
        }

    def detectar_soluciones_multiples(self, tableau, num_vars_originales, base_vars):
        """
        Detectar soluciones óptimas múltiples
        
        Args:
            tableau: Matriz del tableau simplex
            num_vars_originales: Número de variables originales del problema
            base_vars: Variables básicas actuales
            
        Returns:
            dict: Información sobre soluciones múltiples
        """
        fila_objetivo = tableau[-1]
        variables_multiples = []
        tiene_multiples = False
        
        # Revisar variables no básicas con coeficiente cero en función objetivo
        for j in range(num_vars_originales):
            if j not in base_vars and abs(fila_objetivo[j]) < self.tolerancia:
                tiene_multiples = True
                variables_multiples.append(j)
                mensaje = f"⚠️  SOLUCIONES MÚLTIPLES: Variable x{j+1} tiene coeficiente {fila_objetivo[j]:.6f} ≈ 0"
                print(mensaje)
                self.casos_detectados.append(mensaje)
        
        if tiene_multiples:
            print("📋 Se detectaron posibles soluciones óptimas múltiples")
            print("💡 Puede haber infinitas soluciones óptimas")
            print("🔍 Para encontrar otra solución, haga pivoteo con una variable de coeficiente 0")
        
        return {
            'tiene_multiples': tiene_multiples,
            'variables_multiples': variables_multiples,
            'num_variables_multiples': len(variables_multiples)
        }

    def verificar_problema_ilimitado(self, tableau, col_pivote):
        """
        Verificar si el problema es ilimitado (no acotado)
        
        Args:
            tableau: Matriz del tableau simplex
            col_pivote: Columna de la variable que entra
            
        Returns:
            dict: Información sobre ilimitación
        """
        ilimitado = True
        coeficientes_positivos = []
        
        # Verificar si todos los coeficientes de la columna pivote son ≤ 0
        for i in range(len(tableau) - 1):
            coef = tableau[i][col_pivote]
            if coef > self.tolerancia:
                ilimitado = False
                coeficientes_positivos.append((i, coef))
        
        if ilimitado:
            mensaje = "❌ PROBLEMA ILIMITADO DETECTADO"
            print(mensaje)
            print(f"🔍 Variable x{col_pivote+1} puede crecer indefinidamente")
            print("📈 La función objetivo no tiene cota superior/inferior")
            self.casos_detectados.append(mensaje)
        
        return {
            'ilimitado': ilimitado,
            'variable_ilimitada': col_pivote if ilimitado else None,
            'coeficientes_positivos': coeficientes_positivos
        }

    def detectar_problema_infactible(self, tableau, var_artificiales, base_vars):
        """
        Detectar si el problema es infactible
        
        Args:
            tableau: Matriz del tableau simplex
            var_artificiales: Lista de variables artificiales
            base_vars: Variables básicas actuales
            
        Returns:
            dict: Información sobre infactibilidad
        """
        infactible = False
        vars_art_positivas = []
        
        # Verificar si hay variables artificiales básicas con valor > 0
        for i, var_base in enumerate(base_vars):
            if var_base in var_artificiales:
                valor = tableau[i][-1]
                if valor > self.tolerancia:
                    infactible = True
                    vars_art_positivas.append((var_base, valor))
                    mensaje = f"❌ Variable artificial x{var_base+1} = {valor:.6f} > 0"
                    print(mensaje)
                    self.casos_detectados.append(mensaje)
        
        if infactible:
            print("❌ PROBLEMA INFACTIBLE DETECTADO")
            print("🚫 No existe solución que satisfaga todas las restricciones")
        
        return {
            'infactible': infactible,
            'vars_artificiales_positivas': vars_art_positivas,
            'num_vars_art_positivas': len(vars_art_positivas)
        }

    def analizar_sensibilidad_basica(self, tableau, base_vars, num_vars_originales):
        """
        Análisis básico de sensibilidad de la solución
        
        Args:
            tableau: Matriz del tableau final
            base_vars: Variables básicas
            num_vars_originales: Número de variables originales
            
        Returns:
            dict: Información de sensibilidad
        """
        analisis = {
            'precios_sombra': [],
            'rangos_rhs': [],
            'costos_reducidos': []
        }
        
        # Precios sombra (valores duales)
        fila_objetivo = tableau[-1]
        num_restricciones = len(tableau) - 1
        
        for i in range(num_vars_originales, num_vars_originales + num_restricciones):
            if i < len(fila_objetivo) - 1:
                precio_sombra = -fila_objetivo[i]  # Negativo por convención
                analisis['precios_sombra'].append(precio_sombra)
        
        # Costos reducidos para variables no básicas
        for j in range(num_vars_originales):
            if j not in base_vars:
                costo_reducido = fila_objetivo[j]
                analisis['costos_reducidos'].append((j, costo_reducido))
        
        print("\n📊 ANÁLISIS DE SENSIBILIDAD BÁSICO:")
        print("=" * 40)
        if analisis['precios_sombra']:
            print("💰 Precios sombra (valores duales):")
            for i, precio in enumerate(analisis['precios_sombra']):
                print(f"  Restricción {i+1}: {precio:.4f}")
        
        if analisis['costos_reducidos']:
            print("📉 Costos reducidos (variables no básicas):")
            for var, costo in analisis['costos_reducidos']:
                print(f"  x{var+1}: {costo:.4f}")
        
        return analisis

    def generar_reporte_casos_especiales(self):
        """
        Generar reporte completo de casos especiales detectados
        
        Returns:
            str: Reporte formateado
        """
        if not self.casos_detectados:
            return "✅ No se detectaron casos especiales"
        
        reporte = "\n" + "="*50 + "\n"
        reporte += "📋 REPORTE DE CASOS ESPECIALES DETECTADOS\n"
        reporte += "="*50 + "\n"
        
        for i, caso in enumerate(self.casos_detectados, 1):
            reporte += f"{i}. {caso}\n"
        
        reporte += f"\nTotal de casos detectados: {len(self.casos_detectados)}\n"
        reporte += "="*50
        
        return reporte

    def aplicar_regla_bland(self, tableau, tipo_objetivo):
        """
        Aplicar regla de Bland para evitar ciclado en casos degenerados
        
        Args:
            tableau: Matriz del tableau
            tipo_objetivo: 'max' o 'min'
            
        Returns:
            int: Índice de columna pivote según regla de Bland
        """
        fila_objetivo = tableau[-1]
        
        # Regla de Bland: Elegir la variable con menor índice que mejore
        for j in range(len(fila_objetivo) - 1):
            if tipo_objetivo == 'max':
                if fila_objetivo[j] < -self.tolerancia:
                    print(f"🔄 Regla de Bland aplicada: Variable x{j+1} seleccionada")
                    return j
            else:
                if fila_objetivo[j] > self.tolerancia:
                    print(f"🔄 Regla de Bland aplicada: Variable x{j+1} seleccionada")
                    return j
        
        return -1  # Óptimo alcanzado

# Funciones auxiliares para facilitar el uso
def detectar_degeneracion(tableau, base_vars, tolerancia=1e-10):
    """Función auxiliar para detectar degeneración"""
    manejador = ManejadorCasosEspeciales(tolerancia)
    return manejador.detectar_degeneracion(tableau, base_vars)

def detectar_soluciones_multiples(tableau, num_vars_originales, base_vars, tolerancia=1e-10):
    """Función auxiliar para detectar soluciones múltiples"""
    manejador = ManejadorCasosEspeciales(tolerancia)
    return manejador.detectar_soluciones_multiples(tableau, num_vars_originales, base_vars)

def verificar_problema_ilimitado(tableau, col_pivote, tolerancia=1e-10):
    """Función auxiliar para verificar problema ilimitado"""
    manejador = ManejadorCasosEspeciales(tolerancia)
    return manejador.verificar_problema_ilimitado(tableau, col_pivote)

def detectar_problema_infactible(tableau, var_artificiales, base_vars, tolerancia=1e-10):
    """Función auxiliar para detectar problema infactible"""
    manejador = ManejadorCasosEspeciales(tolerancia)
    return manejador.detectar_problema_infactible(tableau, var_artificiales, base_vars)