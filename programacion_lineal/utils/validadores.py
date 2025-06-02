from sympy import sympify

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
        tipo = input("¿Maximización o Minimización? (max/min): ").strip().lower()

    try:
        expr = sympify(expr_str)
        variables = sorted(expr.free_symbols, key=lambda x: x.name)
        coeficientes = [float(expr.coeff(var)) for var in variables]
        return tipo, expr, variables, coeficientes
    except Exception as e:
        print("Error al analizar la función objetivo:", e)
        return None, None, None, None

def leer_restricciones(variables):
    """Leer y procesar las restricciones"""
    num_restricciones = int(input("¿Cuántas restricciones?: "))
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
        
        # Procesar restricción
        if "<=" in restr:
            izq, der = restr.split("<=")
            relacion = "<="
        elif ">=" in restr:
            izq, der = restr.split(">=")
            relacion = ">="
        elif "=" in restr and "<=" not in restr and ">=" not in restr:
            izq, der = restr.split("=")
            relacion = "="
        else:
            print("❌ Formato inválido. Use '<=', '>=' o '='")
            return None, None, None

        try:
            izquierda = sympify(izq.strip())
            derecha = float(sympify(der.strip()))
            
            coefs = [float(izquierda.coeff(var)) for var in variables]
            restricciones.append(coefs)
            resultados.append(derecha)
            relaciones.append(relacion)
        except Exception as e:
            print(f"❌ Error en restricción {i+1}:", e)
            return None, None, None

    return restricciones, resultados, relaciones

def mostrar_resumen(tipo, funcion_objetivo, variables, coef_objetivo,
                    matriz_restricciones, vector_resultados, relaciones):
    """Mostrar resumen del problema"""
    print("\n" + "="*60)
    print("📋 RESUMEN DEL PROBLEMA DE PROGRAMACIÓN LINEAL")
    print("="*60)
    print(f"\n🎯 Función objetivo: {funcion_objetivo}")
    print(f"📊 Tipo de problema: {tipo.upper()}")
    print(f"🔢 Variables detectadas: {variables}")
    print(f"📈 Coeficientes: {coef_objetivo}")
    
    print("\n📋 Restricciones:")
    for i, (coefs, rel, result) in enumerate(zip(matriz_restricciones, relaciones, vector_resultados)):
        restriccion_str = " + ".join([f"{coef}*{var}" for coef, var in zip(coefs, variables) if coef != 0])
        print(f"  {i+1}. {restriccion_str} {rel} {result}")
    
    # Verificar compatibilidad con métodos
    tiene_no_estandar = any(rel in ['>=', '='] for rel in relaciones)
    if tiene_no_estandar:
        print("\n⚠️  ADVERTENCIA: Restricciones >= o = detectadas")
        print("   💡 Recomendado: Método Gran M o Dos Fases")
    else:
        print("\n✅ Problema en forma estándar - Compatible con todos los métodos")

def validar_entrada_numerica(prompt, min_val=None, max_val=None):
    """Validar entrada numérica con rango opcional"""
    while True:
        try:
            valor = float(input(prompt))
            if min_val is not None and valor < min_val:
                print(f"❌ El valor debe ser >= {min_val}")
                continue
            if max_val is not None and valor > max_val:
                print(f"❌ El valor debe ser <= {max_val}")
                continue
            return valor
        except ValueError:
            print("❌ Por favor ingrese un número válido")