import sys
import platform

def main():
    print("Versión de Python:", sys.version)
    print("Ejecutable:", sys.executable)
    print("Sistema:", platform.system(), platform.release())

if __name__ == "__main__":
    main()