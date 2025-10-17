#!/usr/bin/env python3
"""
full_ring_vertical.py

Gera um arquivo .obj contendo um aro (anel completo 360°) vertical no plano Y–Z.
Entrada: W (diâmetro exterior)
Saída: ring_<W>.obj
"""

import math

def generate_vertical_ring_obj(diameter: float,
                               divisions: int = 48,
                               ring_thickness_fraction: float = 0.1,
                               thickness_x_fraction: float = 0.05,
                               filename: str | None = None) -> str:
    """
    Gera um anel completo vertical (como uma roda).
    - diameter: diâmetro exterior (W)
    - divisions: número de divisões do círculo
    - ring_thickness_fraction: fração da espessura radial (interior)
    - thickness_x_fraction: fração da espessura horizontal (profundidade)
    """
    outer_r = diameter / 2.0
    inner_r = outer_r * (1.0 - ring_thickness_fraction)
    thickness_x = diameter * thickness_x_fraction

    if filename is None:
        safe_w = str(diameter).replace('.', '_')
        filename = f"ring_{safe_w}.obj"

    verts = []
    faces = []
    full_rad = 2 * math.pi

    # Gera vértices: 4 por divisão (frente/trás × inner/outer)
    for i in range(divisions):
        t = i / divisions
        angle = t * full_rad
        ca, sa = math.cos(angle), math.sin(angle)
        x_front = thickness_x / 2.0
        x_back = -thickness_x / 2.0

        # plano YZ: outer_front, outer_back, inner_front, inner_back
        verts.append((x_front, ca * outer_r, sa * outer_r))
        verts.append((x_back,  ca * outer_r, sa * outer_r))
        verts.append((x_front, ca * inner_r, sa * inner_r))
        verts.append((x_back,  ca * inner_r, sa * inner_r))

    # cria faces entre divisões (fechando o anel)
    for i in range(divisions):
        next_i = (i + 1) % divisions
        a = i * 4
        b = next_i * 4

        # lados exteriores
        faces.append((a + 1, b + 1, b + 2))
        faces.append((a + 1, b + 2, a + 2))

        # lados interiores
        faces.append((a + 4, b + 4, b + 3))
        faces.append((a + 4, b + 3, a + 3))

        # face frontal (x positivo)
        faces.append((a + 1, a + 4, b + 4))
        faces.append((a + 1, b + 4, b + 1))

        # face traseira (x negativo)
        faces.append((a + 2, b + 2, b + 3))
        faces.append((a + 2, b + 3, a + 3))

    # escreve o ficheiro .obj
    with open(filename, 'w') as f:
        f.write("# OBJ gerado por full_ring_vertical.py\n")
        f.write(f"# diameter={diameter} divisions={divisions}\n")
        for vx, vy, vz in verts:
            f.write(f"v {vx:.6f} {vy:.6f} {vz:.6f}\n")
        f.write("\n")
        for a, b, c in faces:
            f.write(f"f {a} {b} {c}\n")

    return filename


def main():
    try:
        w_str = input("W?-> ").strip()
        w = float(w_str)
    except Exception:
        print("Entrada inválida. Introduz um número para W (diâmetro).")
        return

    out = generate_vertical_ring_obj(
        diameter=w,
        divisions=48,                 # mais divisões → anel mais liso
        ring_thickness_fraction=0.15, # espessura radial
        thickness_x_fraction=0.05,    # espessura horizontal
    )
    print(f"OK — ficheiro gerado: {out}")

print("\033c\033[43;30m\n\n")
if __name__ == "__main__":
    main()

