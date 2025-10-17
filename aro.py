#!/usr/bin/env python3
"""
ring_gen.py

Gera um arquivo .obj contendo um aro (anel completo 360°) horizontal.
Entrada: W (diâmetro)
Saída: ring_<W>.obj
"""

import math

def generate_ring_obj(diameter: float,
                      divisions: int = 24,
                      thickness_fraction: float = 0.05,
                      filename: str | None = None) -> str:
    """
    Gera o conteúdo .obj para um aro circular completo (360°).
    - diameter: diâmetro do aro (W)
    - divisions: número de subdivisões (padrão 24)
    - thickness_fraction: espessura relativa ao diâmetro (padrão 5%)
    - filename: nome do ficheiro a gravar; se None, gera ring_<diameter>.obj
    Retorna o nome do ficheiro gravado.
    """
    r = diameter / 2.0
    thickness = max(0.0001, diameter * thickness_fraction)

    if filename is None:
        safe_w = str(diameter).replace('.', '_')
        filename = f"ring_{safe_w}.obj"

    verts = []
    faces = []

    # 360° em radianos
    full_rad = 2 * math.pi

    # Gerar vértices (topo e base)
    for i in range(divisions):
        t = i / divisions
        angle = t * full_rad
        x = math.cos(angle) * r
        z = math.sin(angle) * r
        y_top = thickness / 2.0
        y_bot = -thickness / 2.0
        verts.append((x, y_top, z))
        verts.append((x, y_bot, z))

    # Construir faces (quad entre pares consecutivos)
    for i in range(divisions):
        v0 = i * 2 + 1
        v1 = i * 2 + 2
        v2 = ((i + 1) % divisions) * 2 + 1
        v3 = ((i + 1) % divisions) * 2 + 2

        # duas faces triangulares por segmento
        faces.append((v0, v2, v3))
        faces.append((v0, v3, v1))

    with open(filename, 'w') as f:
        f.write("# OBJ gerado por ring_gen.py\n")
        f.write(f"# diameter={diameter} divisions={divisions} thickness={thickness}\n")
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

    out = generate_ring_obj(diameter=w,
                            divisions=24,
                            thickness_fraction=0.05,
                            filename=None)
    print(f"OK — ficheiro gerado: {out}")

print("\033c\033[43;30m\n\n")
if __name__ == "__main__":
    main()

