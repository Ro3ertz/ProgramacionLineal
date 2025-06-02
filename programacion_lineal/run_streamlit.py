#!/usr/bin/env python3
"""
Ejecutar la interfaz web con Streamlit
"""

import subprocess
import sys
import os

def verificar_streamlit():
    """Verificar si Streamlit está instalado"""
    try:
        import streamlit
        return True
    except ImportError:
        return False

def instalar_dependencias():
    """Instalar dependencias necesarias"""
    dependencias = [
        'streamlit',
        'plotly',
        'pandas',
        'matplotlib'
    ]
    
    print("📦 Instalando dependencias para la interfaz web...")
    for dep in dependencias:
        print(f"Instalando {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
    
    print("✅ Dependencias instaladas correctamente")

def main():
    """Función principal"""
    print("🚀 INICIANDO INTERFAZ WEB DE PROGRAMACIÓN LINEAL")
    print("=" * 50)
    
    # Verificar dependencias
    if not verificar_streamlit():
        print("⚠️  Streamlit no está instalado")
        respuesta = input("¿Desea instalarlo automáticamente? (s/n): ").strip().lower()
        
        if respuesta == 's':
            try:
                instalar_dependencias()
            except Exception as e:
                print(f"❌ Error al instalar dependencias: {e}")
                print("💡 Instale manualmente con: pip install streamlit plotly pandas matplotlib")
                return
        else:
            print("👋 Instale las dependencias y vuelva a ejecutar")
            return
    
    # Ejecutar Streamlit
    print("🌐 Iniciando servidor web...")
    print("📱 La aplicación se abrirá en su navegador")
    print("🔗 URL: http://localhost:8501")
    print("\n💡 Para detener el servidor: Ctrl+C")
    print("=" * 50)
    
    # Ruta al archivo de la app
    app_path = os.path.join("interfaz", "streamlit_app.py")
    
    try:
        # Ejecutar streamlit
        subprocess.run([
            sys.executable, 
            '-m', 
            'streamlit', 
            'run', 
            app_path,
            '--server.address', 
            'localhost',
            '--server.port', 
            '8501',
            '--theme.base', 
            'light'
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error al ejecutar Streamlit: {e}")
        print("💡 Ejecute manualmente: streamlit run interfaz/streamlit_app.py")

if __name__ == "__main__":
    main()