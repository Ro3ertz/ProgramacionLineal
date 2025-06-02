# 🚀 Suite de Programación Lineal

**Implementación completa de métodos de resolución para problemas de programación lineal**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Descripción

Este proyecto implementa los tres métodos principales para resolver problemas de programación lineal:

- **🔧 Método Simplex Tradicional** - Para problemas en forma estándar
- **🎯 Método de la Gran M** - Maneja restricciones >= y =
- **🚀 Método de Dos Fases** - Más estable numéricamente

Incluye manejo completo de casos especiales y dos interfaces: consola y web moderna.

## ✨ Características

### 🛠️ Métodos Implementados
- ✅ **Simplex Tradicional** - Optimizado para problemas estándar
- ✅ **Gran M** - Penalización de variables artificiales
- ✅ **Dos Fases** - Separación de factibilidad y optimización

### 📊 Casos Especiales Manejados
- 🔍 **Degeneración** - Variables básicas con valor cero
- 🔄 **Soluciones múltiples** - Infinitas soluciones óptimas
- 📈 **Problemas ilimitados** - Sin cota en función objetivo
- 🚫 **Problemas infactibles** - Sin solución posible

### 🎨 Interfaces de Usuario
- 💻 **Consola** - Interfaz tradicional completa
- 🌐 **Web (Streamlit)** - Interfaz moderna e interactiva

## 🚀 Instalación y Uso

### Prerequisitos
```bash
Python 3.8 o superior
```

### 1. Clonar/Descargar el proyecto
```bash
# Si tienes git
git clone [url-del-proyecto]
cd programacion_lineal

# O simplemente descarga y extrae los archivos
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar

#### 🖥️ Interfaz de Consola
```bash
python main.py
```

#### 🌐 Interfaz Web (Recomendada)
```bash
python run_streamlit.py
```
O directamente:
```bash
streamlit run interfaz/streamlit_app.py
```

## 📁 Estructura del Proyecto

```
programacion_lineal/
├── main.py                     # Interfaz principal de consola
├── run_streamlit.py           # Ejecutar interfaz web
├── requirements.txt           # Dependencias
├── README.md                  # Documentación
│
├── metodos/                   # Algoritmos de resolución
│   ├── __init__.py
│   ├── simplex.py            # Método Simplex tradicional
│   ├── gran_m.py             # Método Gran M
│   └── dos_fases.py          # Método Dos Fases
│
├── utils/                     # Utilidades y validadores
│   ├── __init__.py
│   ├── validadores.py        # Lectura y validación de datos
│   └── casos_especiales.py   # Manejo de casos especiales
│
├── interfaz/                  # Interfaces de usuario
│   ├── __init__.py
│   └── streamlit_app.py      # Interfaz web moderna
│
└── ejemplos/                  # Problemas de prueba
    ├── __init__.py
    └── problemas_test.py     # Suite de 7 problemas ejemplo
```

## 🎯 Ejemplos de Uso

### Problema Simple (Consola)
```
Función objetivo: max 3*x1 + 2*x2
Restricción 1: 2*x1 + x2 <= 6
Restricción 2: x1 + 2*x2 <= 8
```

### Problema con Gran M
```
Función objetivo: max 3*x1 + 2*x2
Restricción 1: x1 + x2 >= 1    # Requiere Gran M
Restricción 2: 2*x1 + x2 <= 6
```

## 📊 Casos de Prueba Incluidos

1. **Problema Estándar** - Simplex tradicional
2. **Problema Gran M** - Restricciones >= 
3. **Problema Dos Fases** - Restricciones mixtas
4. **Caso Degenerado** - Variables básicas = 0
5. **Problema Ilimitado** - Sin cota superior
6. **Problema Infactible** - Sin solución
7. **Soluciones Múltiples** - Infinitas soluciones óptimas

## 🎨 Capturas de la Interfaz Web

La interfaz de Streamlit incluye:
- 📝 **Configuración visual** de problemas
- 📊 **Gráficos interactivos** de soluciones
- 🔍 **Comparación** de métodos
- 📋 **Análisis paso a paso**
- 🎛️ **Controles intuitivos**

## 🛠️ Desarrollo

### Estructura Modular
```python
# Importar métodos
from metodos import SimplexTradicional, GranMSimplex, DosFasesSimplex

# Usar validadores
from utils.validadores import leer_funcion_objetivo

# Detectar casos especiales
from utils.casos_especiales import detectar_degeneracion
```

### Ejemplo de Uso Programático
```python
from metodos import DosFasesSimplex

# Definir problema
c = [3, 2]                    # Función objetivo
A = [[1, 1], [2, 1]]         # Matriz de restricciones
b = [1, 6]                   # Vector RHS
tipos = ['>=', '<=']         # Tipos de restricciones
tipo_objetivo = 'max'        # Maximizar

# Resolver
solver = DosFasesSimplex()
resultado = solver.resolver(c, A, b, tipos, tipo_objetivo)

# Mostrar resultado
if resultado['factible']:
    print(f"Solución: {resultado['solucion']}")
    print(f"Valor óptimo: {resultado['valor_optimo']}")
```

## 📚 Documentación Técnica

### Algoritmo Simplex
1. **Forma estándar**: Convertir restricciones a ≤
2. **Tableau inicial**: Matriz aumentada con variables de holgura
3. **Iteraciones**: Pivoteo hasta alcanzar optimalidad
4. **Verificación**: Casos especiales y solución final

### Método Gran M
1. **Variables artificiales**: Para restricciones >= y =
2. **Penalización**: Coeficiente M grande en función objetivo
3. **Resolución**: Simplex tradicional
4. **Verificación**: Variables artificiales = 0

### Método Dos Fases
1. **Fase I**: Minimizar suma de variables artificiales
2. **Verificación**: Si = 0, problema factible
3. **Fase II**: Resolver problema original
4. **Limpieza**: Eliminar variables artificiales

## 🤝 Contribuciones

Este proyecto fue desarrollado como parte del curso de Investigación de Operaciones. 

### Rúbrica Cubierta
- ✅ **Interfaz Gráfica (20 pts)** - Streamlit moderna
- ✅ **Métodos de Resolución (30 pts)** - Los 3 implementados
- ✅ **Casos Especiales (20 pts)** - Todos cubiertos
- ✅ **Problemas de Ejemplo (15 pts)** - 7 casos completos
- ✅ **Explicación y Análisis (10 pts)** - Documentado
- ✅ **Comprensión (5 pts)** - Comentarios detallados

## 📞 Soporte

Para problemas o preguntas:
1. Revisa la documentación en el código
2. Ejecuta los ejemplos incluidos
3. Usa la interfaz web para casos simples

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

---

**Desarrollado con ❤️ para el curso de Investigación de Operaciones**