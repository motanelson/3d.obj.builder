#!/usr/bin/env python3
"""
arc_gen.py

Gera um arquivo .obj contendo um arco horizontal (plano X-Z) com 24 divisões.
Entrada: W (diâmetro)
Saída: arc_<W>.obj
"""

import math

def generate_arc_obj(diameter: float,
                     divisions: int = 24,
                     thickness_fraction: float = 0.05,
                     arc_degrees: float = 180.0,
                     filename: str | None = None) -> str:
    """
    Gera o conteúdo .obj para um arco semicircular horizontal.
    - diameter: diâmetro do arco (W)
    - divisions: número de subdivisões ao longo do arco (padrão 24)
    - thickness_fraction: espessura relativa ao diâmetro (padrão 5%)
    - arc_degrees: ângulo total do arco em graus (padrão 180 -> semicirculo)
    - filename: nome do ficheiro a gravar; se None, gera arc_<diameter>.obj
    Retorna o nome do ficheiro gravado.
    """
    r = diameter / 2.0
    # thickness em Y (altura do "rib" do arco)
    thickness = max(0.0001, diameter * thickness_fraction)

    if filename is None:
        # remove possíveis pontos do float para filename
        safe_w = str(diameter).replace('.', '_')
        filename = f"arc_{safe_w}.obj"

    # calcular vértices: para cada divisão geramos 2 vértices (top e bottom)
    verts = []
    faces = []

    # converter arco para radianos
    arc_rad = math.radians(arc_degrees)

    for i in range(divisions + 1):  # +1 para incluir a extremidade final
        t = i / divisions
        angle = -arc_rad/2 + t * arc_rad  # centra o arco em frente do eixo Z
        x = math.cos(angle) * r
        z = math.sin(angle) * r
        y_top = thickness / 2.0
        y_bot = -thickness / 2.0
        verts.append((x, y_top, z))
        verts.append((x, y_bot, z))

    # construir faces (quad entre pares de vértices consecutivos)
    # índice OBJ é 1-based
    for i in range(divisions):
        # cada 'coluna' tem dois vértices: top=v0, bottom=v1
        v0 = i * 2 + 1       # top current (OBJ index)
        v1 = i * 2 + 2       # bottom current
        v2 = (i + 1) * 2 + 1 # top next
        v3 = (i + 1) * 2 + 2 # bottom next

        # dividir o quad v0-v2-v3-v1 em duas faces triangulares
        faces.append((v0, v2, v3))
        faces.append((v0, v3, v1))

    # opcional: fechar as extremidades com triângulos (cantos)
    # cria um vértice central no inicio e fim para "tapar" a face
    # se desejar manter o arco vazio, comentar o bloco abaixo
    start_center_top = len(verts) + 1
    start_center_bottom = len(verts) + 2
    verts.append((math.cos(-arc_rad/2) * r * 0.98, thickness/2.0, math.sin(-arc_rad/2) * r * 0.98))
    verts.append((math.cos(-arc_rad/2) * r * 0.98, -thickness/2.0, math.sin(-arc_rad/2) * r * 0.98))
    end_center_top = len(verts) + 1
    end_center_bottom = len(verts) + 2
    verts.append((math.cos(arc_rad/2) * r * 0.98, thickness/2.0, math.sin(arc_rad/2) * r * 0.98))
    verts.append((math.cos(arc_rad/2) * r * 0.98, -thickness/2.0, math.sin(arc_rad/2) * r * 0.98))

    # faces para tapar as extremidades (pequeno "cap")
    # inicio
    faces.append((1, start_center_top, 2))   # tri entre top0, start_center_top, bottom0
    # fim
    last_top = (divisions) * 2 + 1
    last_bottom = last_top + 1
    faces.append((last_top, last_bottom, end_center_top))

    # escrever arquivo .obj
    with open(filename, 'w') as f:
        f.write("# OBJ gerado por arc_gen.py\n")
        f.write(f"# diameter={diameter} divisions={divisions} thickness={thickness}\n")
        for vx, vy, vz in verts:
            f.write(f"v {vx:.6f} {vy:.6f} {vz:.6f}\n")
        f.write("\n")
        # sem normals/uvs para simplicidade
        for a, b, c in faces:
            f.write(f"f {a} {b} {c}\n")

    return filename

def main():
    try:
        w_str = input("W?-> ").strip()
        w = float(w_str)
    except Exception as e:
        print("Entrada inválida. Introduz um número para W (diâmetro).")
        return

    # podes alterar divisions ou espessura aqui se quiseres
    out = generate_arc_obj(diameter=w,
                           divisions=24,
                           thickness_fraction=0.05,
                           arc_degrees=180.0,
                           filename=None)
    print(f"OK — ficheiro gerado: {out}")
print("\033c\033[43;30m\n\n")
if __name__ == "__main__":
    main()

