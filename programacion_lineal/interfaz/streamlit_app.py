import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from sympy import symbols, sympify
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metodos import SimplexTradicional, GranMSimplex, DosFasesSimplex
from utils.casos_especiales import ManejadorCasosEspeciales
from ejemplos.problemas_test import ProblemasTest

# Configuración de la página
st.set_page_config(
    page_title="🚀 Programación Lineal - Suite Completa",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

class StreamlitApp:
    def __init__(self):
        self.manejador_casos = ManejadorCasosEspeciales()
        self.problemas_test = ProblemasTest()

    def main(self):
        """Función principal de la aplicación"""
        
        # Título principal
        st.title("🚀 Suite de Programación Lineal")
        st.markdown("### Implementación completa de métodos Simplex")
        
        # Sidebar para navegación
        st.sidebar.title("📋 Navegación")
        modo = st.sidebar.selectbox(
            "Seleccione el modo:",
            [
                "🏠 Inicio",
                "📝 Resolver Problema",
                "📊 Problemas de Ejemplo", 
                "🔍 Comparar Métodos",
                "📚 Información",
                "🧪 Análisis Avanzado"
            ]
        )
        
        # Información en sidebar
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🛠️ Métodos Implementados")
        st.sidebar.markdown("✅ Simplex Tradicional")
        st.sidebar.markdown("✅ Método Gran M")
        st.sidebar.markdown("✅ Método Dos Fases")
        
        st.sidebar.markdown("### 📋 Casos Especiales")
        st.sidebar.markdown("🔍 Degeneración")
        st.sidebar.markdown("🔄 Soluciones múltiples")
        st.sidebar.markdown("📈 Problemas ilimitados")
        st.sidebar.markdown("🚫 Problemas infactibles")
        
        # Enrutar según la selección
        if modo == "🏠 Inicio":
            self.mostrar_inicio()
        elif modo == "📝 Resolver Problema":
            self.resolver_problema_personalizado()
        elif modo == "📊 Problemas de Ejemplo":
            self.mostrar_problemas_ejemplo()
        elif modo == "🔍 Comparar Métodos":
            self.comparar_metodos()
        elif modo == "📚 Información":
            self.mostrar_informacion()
        elif modo == "🧪 Análisis Avanzado":
            self.analisis_avanzado()

    def mostrar_inicio(self):
        """Página de inicio con información general"""
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ## 🎯 Bienvenido al Proyecto de Programación Lineal
            
            Esta aplicación implementa los tres métodos principales para resolver problemas 
            de programación lineal, con manejo completo de casos especiales.
            
            ### 🔧 Características principales:
            
            - **Métodos de resolución**: Simplex Tradicional, Gran M, y Dos Fases
            - **Casos especiales**: Detección automática de degeneración, soluciones múltiples, etc.
            - **Interfaz intuitiva**: Fácil configuración y visualización de resultados
            - **Ejemplos integrados**: Problemas predefinidos para pruebas
            - **Análisis completo**: Paso a paso del proceso de solución
            
            ### 🚀 ¿Cómo empezar?
            
            1. Selecciona **"Resolver Problema"** para introducir tu propio problema
            2. O explora los **"Problemas de Ejemplo"** para ver casos típicos
            3. Usa **"Comparar Métodos"** para ver diferencias entre algoritmos
            """)
        
        with col2:
            st.markdown("### 📊 Estadísticas")
            
            # Métricas de ejemplo
            st.metric("Métodos implementados", "3", "✅")
            st.metric("Casos especiales", "4", "🔍")
            st.metric("Problemas de ejemplo", "7", "📋")
            
            # Gráfico de ejemplo
            fig = px.pie(
                values=[30, 20, 15, 10, 5],
                names=["Métodos (30pts)", "Casos especiales (20pts)", "Ejemplos (15pts)", "Análisis (10pts)", "Comprensión (5pts)"],
                title="Distribución de puntos en la rúbrica"
            )
            st.plotly_chart(fig, use_container_width=True)

    def resolver_problema_personalizado(self):
        """Interfaz para resolver problema personalizado"""
        
        st.header("📝 Resolver Problema Personalizado")
        
        # Crear tabs
        tab1, tab2, tab3 = st.tabs(["⚙️ Configuración", "🔧 Resolución", "📊 Resultados"])
        
        with tab1:
            self.configurar_problema()
        
        with tab2:
            self.ejecutar_resolucion()
        
        with tab3:
            self.mostrar_resultados()

    def configurar_problema(self):
        """Configuración del problema"""
        
        st.subheader("⚙️ Configuración del Problema")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Configuración básica
            st.markdown("#### 📐 Dimensiones")
            num_vars = st.number_input("Número de variables", min_value=2, max_value=10, value=2)
            num_restr = st.number_input("Número de restricciones", min_value=1, max_value=10, value=2)
            tipo_obj = st.selectbox("Tipo de optimización", ["max", "min"])
            
            # Guardar en session state
            st.session_state.num_vars = num_vars
            st.session_state.num_restr = num_restr
            st.session_state.tipo_obj = tipo_obj
        
        with col2:
            # Método de resolución
            st.markdown("#### 🔧 Método de Resolución")
            metodo = st.selectbox(
                "Seleccionar método",
                [
                    "Selección automática",
                    "Simplex Tradicional",
                    "Método Gran M",
                    "Método Dos Fases"
                ]
            )
            st.session_state.metodo = metodo
            
            # Información sobre el método
            if metodo == "Simplex Tradicional":
                st.info("💡 Solo para problemas en forma estándar (≤)")
            elif metodo == "Método Gran M":
                st.info("💡 Maneja todos los tipos de restricciones")
            elif metodo == "Método Dos Fases":
                st.info("💡 Más estable numéricamente")
            else:
                st.info("💡 Se seleccionará automáticamente el mejor método")
        
        # Función objetivo
        st.markdown("#### 🎯 Función Objetivo")
        
        # Crear inputs para coeficientes
        coef_cols = st.columns(num_vars)
        coeficientes = []
        
        func_obj_str = f"{tipo_obj.upper()} Z = "
        for i in range(num_vars):
            with coef_cols[i]:
                coef = st.number_input(f"c{i+1}", value=1.0, key=f"coef_{i}")
                coeficientes.append(coef)
                if i > 0:
                    func_obj_str += " + "
                func_obj_str += f"{coef}*x{i+1}"
        
        st.latex(func_obj_str.replace("+ -", "- ").replace("*", ""))
        st.session_state.coeficientes = coeficientes
        
        # Restricciones
        st.markdown("#### 📋 Restricciones")
        
        restricciones = []
        tipos_restr = []
        rhs_values = []
        
        for i in range(num_restr):
            st.markdown(f"**Restricción {i+1}:**")
            
            # Coeficientes de la restricción
            restr_cols = st.columns(num_vars + 2)  # +2 para tipo y RHS
            
            coef_restr = []
            restr_str = ""
            
            for j in range(num_vars):
                with restr_cols[j]:
                    coef = st.number_input(f"a{i+1}{j+1}", value=1.0, key=f"restr_{i}_{j}")
                    coef_restr.append(coef)
                    if j > 0:
                        restr_str += " + "
                    restr_str += f"{coef}*x{j+1}"
            
            with restr_cols[num_vars]:
                tipo_rel = st.selectbox("Tipo", ["<=", ">=", "="], key=f"tipo_{i}")
                tipos_restr.append(tipo_rel)
            
            with restr_cols[num_vars + 1]:
                rhs = st.number_input("RHS", value=1.0, key=f"rhs_{i}")
                rhs_values.append(rhs)
            
            # Mostrar la restricción formateada
            st.latex(f"{restr_str.replace('+ -', '- ').replace('*', '')} {tipo_rel} {rhs}")
            
            restricciones.append(coef_restr)
        
        # Guardar restricciones en session state
        st.session_state.restricciones = restricciones
        st.session_state.tipos_restr = tipos_restr
        st.session_state.rhs_values = rhs_values
        
        # Resumen del problema
        with st.expander("📄 Resumen del Problema"):
            st.markdown(f"**Función objetivo:** {func_obj_str}")
            st.markdown("**Restricciones:**")
            for i, (coef_restr, tipo, rhs) in enumerate(zip(restricciones, tipos_restr, rhs_values)):
                restr_str = " + ".join([f"{c}*x{j+1}" for j, c in enumerate(coef_restr)])
                st.markdown(f"- {restr_str} {tipo} {rhs}")

    def ejecutar_resolucion(self):
        """Ejecutar la resolución del problema"""
        
        st.subheader("🔧 Resolución del Problema")
        
        if not hasattr(st.session_state, 'coeficientes'):
            st.warning("⚠️ Primero configure el problema en la pestaña 'Configuración'")
            return
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if st.button("🚀 Resolver Problema", type="primary"):
                with st.spinner("Resolviendo problema..."):
                    resultado = self.resolver_con_metodo_seleccionado()
                    st.session_state.resultado = resultado
                    st.success("✅ Problema resuelto!")
        
        with col2:
            # Mostrar advertencias si es necesario
            tipos = st.session_state.get('tipos_restr', [])
            tiene_no_estandar = any(rel in ['>=', '='] for rel in tipos)
            
            if tiene_no_estandar:
                st.warning("⚠️ El problema contiene restricciones >= o =")
                st.info("💡 Se recomienda usar Gran M o Dos Fases")
            else:
                st.success("✅ Problema en forma estándar")
        
        # Mostrar proceso paso a paso si está disponible
        if hasattr(st.session_state, 'resultado') and st.session_state.resultado:
            resultado = st.session_state.resultado
            
            if 'pasos' in resultado:
                with st.expander("📋 Ver Proceso Paso a Paso"):
                    total_pasos = len(resultado['pasos'])
                    st.info(f"📊 Total de pasos: {total_pasos}")
                    
                    # Opción para mostrar todos los pasos
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        mostrar_todos = st.checkbox("📜 Mostrar todos los pasos", value=False)
                    
                    with col2:
                        if not mostrar_todos:
                            num_pasos = st.slider("Número de pasos a mostrar:", 
                                                min_value=10, 
                                                max_value=min(100, total_pasos), 
                                                value=min(20, total_pasos))
                        else:
                            num_pasos = total_pasos
                    
                    st.markdown("---")
                    
                    # Mostrar pasos
                    pasos_a_mostrar = resultado['pasos'][:num_pasos] if not mostrar_todos else resultado['pasos']
                    
                    for i, paso in enumerate(pasos_a_mostrar, 1):
                        # Agregar números de paso para mejor navegación
                        if "ITERACIÓN" in paso or "FASE" in paso:
                            st.markdown(f"**{i}. {paso}**")
                        else:
                            st.text(f"{i}. {paso}")
                    
                    if not mostrar_todos and len(resultado['pasos']) > num_pasos:
                        st.info(f"... y {len(resultado['pasos']) - num_pasos} pasos más. Marca 'Mostrar todos los pasos' para verlos.")

    def resolver_con_metodo_seleccionado(self):
        """Resolver usando el método seleccionado"""
        
        # Obtener datos del session state
        coeficientes = st.session_state.coeficientes
        restricciones = st.session_state.restricciones
        rhs_values = st.session_state.rhs_values
        tipos_restr = st.session_state.tipos_restr
        tipo_obj = st.session_state.tipo_obj
        metodo_nombre = st.session_state.metodo
        
        # Seleccionar solver
        if metodo_nombre == "Simplex Tradicional":
            solver = SimplexTradicional()
        elif metodo_nombre == "Método Gran M":
            solver = GranMSimplex()
        elif metodo_nombre == "Método Dos Fases":
            solver = DosFasesSimplex()
        else:  # Selección automática
            tiene_no_estandar = any(rel in ['>=', '='] for rel in tipos_restr)
            if tiene_no_estandar:
                solver = DosFasesSimplex()
                st.info("🤖 Selección automática: Método Dos Fases")
            else:
                solver = SimplexTradicional()
                st.info("🤖 Selección automática: Simplex Tradicional")
        
        # Resolver
        try:
            resultado = solver.resolver(coeficientes, restricciones, rhs_values, tipos_restr, tipo_obj)
            resultado['metodo_usado'] = solver.__class__.__name__
            return resultado
        except Exception as e:
            st.error(f"❌ Error durante la resolución: {e}")
            return None

    def mostrar_resultados(self):
        """Mostrar los resultados de la resolución"""
        
        st.subheader("📊 Resultados")
        
        if not hasattr(st.session_state, 'resultado') or not st.session_state.resultado:
            st.info("ℹ️ Resuelva primero el problema para ver los resultados")
            return
        
        resultado = st.session_state.resultado
        
        # Mostrar resultado principal
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if resultado['factible']:
                st.success("✅ Problema Resuelto Exitosamente")
                
                # Métricas principales
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Valor Óptimo", f"{resultado['valor_optimo']:.6f}")
                with col_m2:
                    st.metric("Método Usado", resultado.get('metodo_usado', 'N/A'))
                with col_m3:
                    st.metric("Variables", len(resultado['solucion']))
                
                # Tabla de solución
                st.markdown("#### 📍 Solución Óptima")
                solucion_df = pd.DataFrame({
                    'Variable': [f'x{i+1}' for i in range(len(resultado['solucion']))],
                    'Valor': resultado['solucion']
                })
                st.dataframe(solucion_df, use_container_width=True)
                
            elif resultado.get('ilimitado'):
                st.error("❌ Problema Ilimitado")
                st.markdown("📈 La función objetivo puede crecer indefinidamente")
            else:
                st.error("❌ Problema No Factible")
                st.markdown("🚫 No existe solución que satisfaga todas las restricciones")
        
        with col2:
            # Gráfico de la solución (solo para 2 variables)
            if len(resultado.get('solucion', [])) == 2 and resultado['factible']:
                self.crear_grafico_solucion()
        
        # Análisis de casos especiales
        if resultado['factible']:
            with st.expander("🔍 Análisis de Casos Especiales"):
                # Aquí puedes agregar análisis más detallado
                st.markdown("### Casos especiales detectados:")
                casos = self.manejador_casos.generar_reporte_casos_especiales()
                if casos == "✅ No se detectaron casos especiales":
                    st.success(casos)
                else:
                    st.text(casos)

    def crear_grafico_solucion(self):
        """Crear gráfico de la solución para problemas de 2 variables"""
        
        if len(st.session_state.get('coeficientes', [])) != 2:
            return
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Obtener datos
        resultado = st.session_state.resultado
        x1_opt, x2_opt = resultado['solucion']
        
        # Crear grilla para graficar
        x1 = np.linspace(0, max(10, x1_opt * 2), 100)
        x2 = np.linspace(0, max(10, x2_opt * 2), 100)
        
        # Graficar restricciones
        restricciones = st.session_state.restricciones
        rhs_values = st.session_state.rhs_values
        tipos_restr = st.session_state.tipos_restr
        
        for i, (coef, rhs, tipo) in enumerate(zip(restricciones, rhs_values, tipos_restr)):
            if coef[1] != 0:  # Evitar división por cero
                x2_restr = (rhs - coef[0] * x1) / coef[1]
                ax.plot(x1, x2_restr, label=f'Restricción {i+1}')
        
        # Punto óptimo
        ax.plot(x1_opt, x2_opt, 'ro', markersize=10, label=f'Óptimo ({x1_opt:.2f}, {x2_opt:.2f})')
        
        # Configuración del gráfico
        ax.set_xlim(0, max(10, x1_opt * 1.5))
        ax.set_ylim(0, max(10, x2_opt * 1.5))
        ax.set_xlabel('x1')
        ax.set_ylabel('x2')
        ax.set_title('Solución Gráfica del Problema')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)

    def mostrar_problemas_ejemplo(self):
        """Mostrar problemas de ejemplo"""
        
        st.header("📊 Problemas de Ejemplo")
        
        ejemplos = {
            "Problema Estándar": "problema_1",
            "Problema Gran M": "problema_2", 
            "Problema Dos Fases": "problema_3",
            "Caso Degenerado": "problema_4",
            "Problema Ilimitado": "problema_5",
            "Problema Infactible": "problema_6",
            "Soluciones Múltiples": "problema_7"
        }
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            ejemplo_seleccionado = st.selectbox("Seleccionar ejemplo:", list(ejemplos.keys()))
            
            if st.button("🚀 Ejecutar Ejemplo"):
                with st.spinner("Ejecutando ejemplo..."):
                    # Capturar output del ejemplo
                    import io
                    from contextlib import redirect_stdout
                    
                    output = io.StringIO()
                    with redirect_stdout(output):
                        self.problemas_test.ejecutar_problema_especifico(ejemplos[ejemplo_seleccionado])
                    
                    st.session_state.ejemplo_output = output.getvalue()
        
        with col2:
            if hasattr(st.session_state, 'ejemplo_output'):
                st.markdown("### 📋 Resultado del Ejemplo")
                st.text(st.session_state.ejemplo_output)

    def comparar_metodos(self):
        """Comparar los diferentes métodos"""
        
        st.header("🔍 Comparación de Métodos")
        
        st.markdown("""
        ### Problema de Comparación
        **Maximizar** Z = 3x₁ + 2x₂  
        **Sujeto a:**
        - x₁ + x₂ ≥ 1
        - 2x₁ + x₂ ≤ 6
        - x₁ + 2x₂ ≤ 8
        - x₁, x₂ ≥ 0
        """)
        
        if st.button("🔄 Ejecutar Comparación"):
            with st.spinner("Comparando métodos..."):
                self.ejecutar_comparacion()

    def ejecutar_comparacion(self):
        """Ejecutar comparación entre métodos"""
        
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
        
        resultados = []
        
        for nombre, solver in metodos:
            try:
                resultado = solver.resolver(c, A, b, tipos, tipo_objetivo)
                resultados.append({
                    'Método': nombre,
                    'Factible': '✅' if resultado['factible'] else '❌',
                    'Valor Óptimo': f"{resultado['valor_optimo']:.4f}" if resultado['factible'] else 'N/A',
                    'x₁': f"{resultado['solucion'][0]:.4f}" if resultado['factible'] else 'N/A',
                    'x₂': f"{resultado['solucion'][1]:.4f}" if resultado['factible'] else 'N/A'
                })
            except Exception as e:
                resultados.append({
                    'Método': nombre,
                    'Factible': '❌',
                    'Valor Óptimo': f'Error: {str(e)}',
                    'x₁': 'N/A',
                    'x₂': 'N/A'
                })
        
        # Mostrar tabla de comparación
        df = pd.DataFrame(resultados)
        st.dataframe(df, use_container_width=True)

    def mostrar_informacion(self):
        """Mostrar información sobre los métodos"""
        
        st.header("📚 Información sobre Métodos")
        
        tabs = st.tabs(["🔧 Simplex", "🎯 Gran M", "🚀 Dos Fases", "📋 Casos Especiales"])
        
        with tabs[0]:
            st.markdown("""
            ## Método Simplex Tradicional
            
            ### ✅ Características:
            - **Aplicación**: Problemas en forma estándar (restricciones ≤)
            - **Ventajas**: Rápido y directo
            - **Limitaciones**: Solo problemas ya factibles
            
            ### 📐 Forma estándar:
            ```
            Maximizar/Minimizar: c^T x
            Sujeto a: Ax ≤ b, x ≥ 0
            ```
            
            ### ⚙️ Algoritmo:
            1. Convertir a forma tableau
            2. Encontrar variable que entra (columna pivote)
            3. Encontrar variable que sale (fila pivote)
            4. Realizar operaciones de pivoteo
            5. Repetir hasta alcanzar optimalidad
            """)
        
        with tabs[1]:
            st.markdown("""
            ## Método de la Gran M
            
            ### ✅ Características:
            - **Aplicación**: Cualquier tipo de restricción
            - **Ventajas**: Maneja restricciones ≥ y =
            - **Limitaciones**: Problemas numéricos con M grande
            
            ### 🎯 Concepto:
            - Introduce variables artificiales
            - Penaliza con coeficiente M muy grande
            - M → ∞ en teoría, valor grande en práctica
            
            ### ⚙️ Proceso:
            1. Agregar variables de holgura/exceso
            2. Introducir variables artificiales
            3. Penalizar variables artificiales en función objetivo
            4. Aplicar simplex tradicional
            5. Verificar que variables artificiales = 0
            """)
        
        with tabs[2]:
            st.markdown("""
            ## Método de Dos Fases
            
            ### ✅ Características:
            - **Aplicación**: Cualquier tipo de restricción
            - **Ventajas**: Más estable numéricamente
            - **Proceso**: Separa factibilidad de optimización
            
            ### 🔄 Fase I:
            - Minimizar suma de variables artificiales
            - Si resultado = 0 → problema factible
            - Si resultado > 0 → problema infactible
            
            ### 🎯 Fase II:
            - Eliminar variables artificiales
            - Resolver problema original
            - Usar solución factible de Fase I
            """)
        
        with tabs[3]:
            st.markdown("""
            ## Casos Especiales
            
            ### ⚠️ Degeneración:
            - Variable básica con valor cero
            - Puede causar ciclado
            - **Solución**: Regla de Bland
            
            ### 🔄 Soluciones Múltiples:
            - Variable no básica con coeficiente 0 en función objetivo
            - Infinitas soluciones óptimas
            - **Detección**: Revisar fila objetivo final
            
            ### 📈 Problemas Ilimitados:
            - Función objetivo puede crecer indefinidamente
            - **Detección**: Todos los coeficientes ≤ 0 en columna pivote
            
            ### 🚫 Problemas Infactibles:
            - No existe solución factible
            - **Detección**: Variables artificiales > 0 en solución final
            """)

    def analisis_avanzado(self):
        """Análisis avanzado y herramientas adicionales"""
        
        st.header("🧪 Análisis Avanzado")
        
        opciones = st.selectbox(
            "Seleccionar análisis:",
            [
                "📊 Análisis de Sensibilidad",
                "🔍 Detección Manual de Casos",
                "📈 Visualización de Convergencia",
                "🛠️ Herramientas de Debug"
            ]
        )
        
        if opciones == "📊 Análisis de Sensibilidad":
            st.markdown("""
            ### Análisis de Sensibilidad
            
            El análisis de sensibilidad estudia cómo cambia la solución óptima 
            ante variaciones en los parámetros del problema.
            
            **Conceptos clave:**
            - **Precios sombra**: Valor marginal de relajar una restricción
            - **Costos reducidos**: Cambio en función objetivo por unidad de variable no básica
            - **Rangos de validez**: Intervalos donde la base óptima no cambia
            """)
        
        elif opciones == "🔍 Detección Manual de Casos":
            st.markdown("""
            ### Detección Manual de Casos Especiales
            
            Introduzca un tableau manualmente para analizar casos especiales:
            """)
            
            # Aquí podrías agregar inputs para introducir tableau manualmente
            st.info("💡 Funcionalidad disponible en la resolución automática")
        
        elif opciones == "📈 Visualización de Convergencia":
            st.markdown("""
            ### Visualización del Proceso de Convergencia
            
            Gráficos que muestran cómo evoluciona la función objetivo
            y las variables a través de las iteraciones.
            """)
            
            # Ejemplo de gráfico de convergencia
            iteraciones = list(range(1, 6))
            valores_obj = [0, 4, 7, 9, 10]
            
            fig = px.line(x=iteraciones, y=valores_obj, 
                         title="Evolución de la Función Objetivo",
                         labels={'x': 'Iteración', 'y': 'Valor de Z'})
            st.plotly_chart(fig)
        
        elif opciones == "🛠️ Herramientas de Debug":
            st.markdown("""
            ### Herramientas de Debug
            
            - **Verificación de tableaux**: Validar operaciones de pivoteo
            - **Trazabilidad**: Seguir el camino de una variable específica
            - **Validación**: Comprobar factibilidad y optimalidad manualmente
            """)

def main():
    """Función principal para ejecutar la app de Streamlit"""
    app = StreamlitApp()
    app.main()

if __name__ == "__main__":
    main()