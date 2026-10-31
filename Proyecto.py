"""
Proyecto.py
Versión adaptada para usar BinaryTree4.py como árbol binario del proyecto.
"""

import os
import random
import sys
from BinaryTree import BinaryTree,Node

sys.setrecursionlimit(150000)
# Devuelve el hijo izquierdo de un nodo
def get_left(node):
    if node is None:
        return None  # Si el nodo no existe, no hay hijo
    return node._left  # Devuelve el hijo izquierdo


# Devuelve el hijo derecho de un nodo
def get_right(node):
    if node is None:
        return None  # Si el nodo no existe, no hay hijo
    return node._right  # Devuelve el hijo derecho


# Devuelve la clave de la raíz del árbol
def root_key(tree):
    if tree.root is None:
        return None  # Árbol vacío
    return tree.root.key  # Clave de la raíz


# Devuelve la clave del hijo izquierdo de la raíz
def left_of_root(tree):
    if tree.root is None:
        return None  # Árbol vacío

    if tree.root._left is None:
        return None  # No tiene hijo izquierdo

    return tree.root._left.key  # Clave del hijo izquierdo


# Devuelve la clave del hijo derecho de la raíz
def right_of_root(tree):
    if tree.root is None:
        return None  # Árbol vacío

    if tree.root._right is None:
        return None  # No tiene hijo derecho

    return tree.root._right.key  # Clave del hijo derecho


# Cuenta el número total de nodos del árbol
def count_nodes_tree(node) -> int:
    if node is None:
        return 0  # Caso base: no hay nodo

    # Cuenta el nodo actual + nodos del subárbol izquierdo + derecho
    return 1 + count_nodes_tree(get_left(node)) + count_nodes_tree(get_right(node))


# Cuenta el número de hojas (nodos sin hijos)
def count_leafs(node) -> int:
    if node is None:
        return 0  # Caso base

    # Si no tiene hijos, es una hoja
    if get_left(node) is None and get_right(node) is None:
        return 1

    # Suma hojas del subárbol izquierdo y derecho
    return count_leafs(get_left(node)) + count_leafs(get_right(node))


# Devuelve el camino más largo desde un nodo hasta una hoja
def longest_path(node) -> list[str]:
    if node is None:
        return []  # Caso base: camino vacío

    # Calcula caminos izquierdo y derecho
    left = longest_path(get_left(node))
    right = longest_path(get_right(node))

    # Devuelve el nodo actual + el camino más largo
    return [node.key] + (left if len(left) > len(right) else right)



# Devuelve todos los caminos desde la raíz hasta una hoja
# que tengan exactamente el número de aristas indicado
def paths_to_leaf_with_length(node: Node, remaining_edges: int,
                              current_path: list[str] = None,
                              results: list[list[str]] = None) -> list[list[str]]:

    """
    Devuelve todos los caminos raíz->hoja con longitud exacta
    (en aristas) igual a remaining_edges al comienzo de la llamada.

    Uso típico:
    paths = paths_to_leaf_with_length(tree.root, 3)

    Parámetros:
    - node: nodo actual (se empieza normalmente en la raíz)
    - remaining_edges: número de aristas que faltan para completar la longitud buscada
    - current_path: lista interna con el camino actual
    - results: lista interna donde se guardan los caminos válidos

    Retorna:
    - Una lista de caminos; cada camino es una lista de strings
      con las claves de los nodos.
    """

    # Si current_path no existe todavía, se crea una lista vacía
    if current_path is None:
        current_path = []

    # Si results no existe todavía, se crea una lista vacía
    if results is None:
        results = []

    # Si el nodo no existe, no hay nada que recorrer
    if node is None:
        return results

    # Añade la clave del nodo actual al camino
    current_path.append(str(node.key))

    # Si ya no quedan aristas y además estamos en una hoja,
    # el camino actual es válido y se guarda en results
    if remaining_edges == 0 and node.get_left() is None and node.get_right() is None:
        results.append(current_path.copy())
        current_path.pop()  # backtracking: deshacer el último paso
        return results

    # Si ya no quedan aristas pero no estamos en una hoja,
    # este camino no sirve
    elif remaining_edges == 0:
        current_path.pop()  # backtracking
        return results

    # Recorre el hijo izquierdo si existe
    if node.get_left() is not None:
        paths_to_leaf_with_length(node.get_left(), remaining_edges - 1, current_path, results)

    # Recorre el hijo derecho si existe
    if node.get_right() is not None:
        paths_to_leaf_with_length(node.get_right(), remaining_edges - 1, current_path, results)

    # Elimina el nodo actual del camino antes de volver atrás
    current_path.pop()
    return results


# Pide al usuario hasta un máximo de letras
def pedir_letras(max_letras: int = 3) -> list[str]:
    letras: list[str] = []

    # Mensaje inicial
    print(f"Introduce hasta {max_letras} letras. Deja vacío para terminar antes.")

    # Se repite como máximo max_letras veces
    for i in range(max_letras):
        while True:
            letra = input(f"Letra {i + 1}: ").strip().lower()

            # Si el usuario no escribe nada, se termina antes
            if letra == "":
                return letras

            # Solo se acepta una única letra alfabética
            if len(letra) == 1 and letra.isalpha():
                letras.append(letra)
                break

            # Si el dato no es válido, se vuelve a pedir
            print("Error: debes introducir exactamente una letra.")

    return letras


# Pide al usuario el modo de inserción:
# d = defecto
# a = aleatoria
def pedir_modo_insercion() -> bool:
    while True:
        opcion = input("Modo de inserción ('d' = defecto, 'a' = aleatoria): ").strip().lower()

        # Si la opción es válida, devuelve True si es aleatoria y False si es por defecto
        if opcion in ("d", "a"):
            return opcion == "a"

        # Si la opción no es válida, vuelve a pedirla
        print("Opción no válida. Escribe 'd' o 'a'.")



# Carga del fichero todas las palabras que empiezan por una letra dada
def cargar_palabras_por_letra(ruta_fichero: str, letra: str, insercion_aleatoria: bool) -> list[str]:
    # Comprueba si el fichero existe
    if not os.path.exists(ruta_fichero):
        raise FileNotFoundError(
            f"No se ha encontrado el fichero de palabras: {ruta_fichero}\n"
            "Pon palabras_RAE_cleaned_noaccents.txt en la misma carpeta que Proyecto.py."
        )

    # Lista donde se guardarán las palabras encontradas
    palabras: list[str] = []

    # Abre el fichero en modo lectura
    with open(ruta_fichero, "r", encoding="utf-8") as f:
        for linea in f:
            palabra = linea.strip()  # Elimina espacios y salto de línea

            # Si la palabra no está vacía y empieza por la letra indicada, se guarda
            if palabra and palabra.lower().startswith(letra.lower()):
                palabras.append(palabra)

    # Si se ha elegido inserción aleatoria, se mezclan las palabras
    if insercion_aleatoria:
        random.shuffle(palabras)

    # Devuelve la lista final de palabras
    return palabras


# Construye un árbol binario de búsqueda a partir de una lista de palabras
def construir_arbol_binario(palabras: list[str]) -> BinaryTree:
    # Crea un árbol vacío
    tree = BinaryTree()

    # Inserta cada palabra en el árbol
    for palabra in palabras:
        tree.insert(palabra, palabra)

    # Devuelve el árbol ya construido
    return tree


# Imprime por pantalla un resumen con la información principal de un árbol
def imprimir_resumen_arbol(nombre: str, tree: BinaryTree, paths_length: int = 6, nil_node=None) -> None:
    # Muestra el nombre del árbol
    print(f"\n--- {nombre} ---")

    # Muestra información básica de la raíz
    print("Raíz:", root_key(tree))
    print("Hijo izquierdo de la raíz:", left_of_root(tree))
    print("Hijo derecho de la raíz:", right_of_root(tree))

    # Muestra número total de nodos y número de hojas
    print("Número de nodos:", count_nodes_tree(tree.root))
    print("Número de hojas:", count_leafs(tree.root))

    # Calcula y muestra la ruta más larga desde la raíz a una hoja
    longest = longest_path(tree.root)
    print("Ruta más larga raíz->hoja:", longest)

    # Muestra esa misma ruta pero al revés, desde hoja hasta raíz
    print("Ruta más larga hoja->raíz:", list(reversed(longest)) if longest else [])

    # Calcula todos los caminos raíz->hoja con longitud exacta paths_length
    caminos = paths_to_leaf_with_length(tree.root, paths_length)
    print(f"Caminos raíz->hoja con longitud exacta {paths_length} aristas:", caminos)

    # Muestra la altura del árbol
    print("Altura:", tree.height())

    # Indica si el árbol está inclinado o no
    print("¿Está inclinado?:", tree.skew())


# Muestra la información de un árbol asociado a una letra concreta
def comparar_por_letra(letra: str, bst: BinaryTree) -> None:
    # Imprime un título indicando la letra que se está analizando
    print(f"\n================ ÁRBOL PARA LA LETRA '{letra}' ================")

    # Imprime el resumen del árbol binario de búsqueda
    imprimir_resumen_arbol("Árbol binario de búsqueda", bst)

if __name__ == "__main__":
    print("==========================================")
    print(" PROYECTO - ÁRBOLES BINARIOS")
    print("==========================================")

    letras = pedir_letras(3)

    if letras:
        insercion_aleatoria = pedir_modo_insercion()
        ruta_fichero = "palabras_RAE_cleaned_noaccents.txt"

        for letra in letras:
            try:
                palabras = cargar_palabras_por_letra(ruta_fichero, letra, insercion_aleatoria)

                print(f"\nLetra '{letra}': {len(palabras)} palabras encontradas.")

                if palabras:
                    bst = construir_arbol_binario(palabras)
                    comparar_por_letra(letra, bst)
                else:
                    print("No hay palabras para esa letra.")

            except FileNotFoundError as exc:
                print(exc)

    else:
        print("No se introdujo ninguna letra.")
