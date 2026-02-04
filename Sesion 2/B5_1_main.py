import math

def calcular_area_circulo(radio: float) -> float:
    area = math.pi * radio ** 2
    return area

def main():
    radios = [1, 2, 3]
    for r in radios:
        area = calcular_area_circulo(r)
        print(f"Radio={r} -> área={area:.2f}")

if __name__ == "__main__":
    main()