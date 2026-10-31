import sys

sys.setrecursionlimit(15000)

RED = "RED"
BLACK = "BLACK"


class Queue:
    """
    Cola circular con capacidad fija.
    """

    def __init__(self, length: int):
        """
        Inicializa una cola vacía de tamaño máximo 'length'.
        """
        self.array = [None] * length
        self.head = -1
        self.tail = -1
        self.length = length

    def is_full(self) -> bool:
        """
        Devuelve True si la cola está llena.
        """
        if self.is_empty():
            return False
        return (self.tail + 1) % self.length == self.head

    def is_empty(self) -> bool:
        """
        Devuelve True si la cola está vacía.
        """
        return self.head == -1 and self.tail == -1

    def enqueue(self, item):
        """
        Inserta un elemento al final de la cola.
        """
        if self.is_full():
            print("Queue is full")
            return

        if self.head == -1:
            self.head = self.tail = 0
            self.array[self.tail] = item
        else:
            self.tail = (self.tail + 1) % self.length
            self.array[self.tail] = item

    def dequeue(self):
        """
        Extrae y devuelve el elemento del frente de la cola.
        """
        if self.is_empty():
            print("Queue is empty")
            return None

        if self.head == self.tail:
            temp = self.array[self.head]
            self.array[self.head] = None
            self.head = self.tail = -1
            return temp

        temp = self.array[self.head]
        self.array[self.head] = None
        self.head = (self.head + 1) % self.length
        return temp


class RBNode:
    """
    Nodo de un árbol rojo-negro.
    """

    def __init__(self, key=None, value=None, color=BLACK):
        self.key = key
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    """
    Árbol rojo-negro.
    Usa un nodo centinela NIL negro para simplificar la implementación.
    """

    def __init__(self):
        self.NIL = RBNode(color=BLACK)
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL
        self.root = self.NIL

    def is_empty(self):
        return self.root == self.NIL

    def insert(self, key, value=None):
        """
        Inserta una clave y su valor en el árbol.
        Si la clave ya existe, actualiza el valor.
        """
        new_node = RBNode(key, value, RED)
        new_node.left = self.NIL
        new_node.right = self.NIL
        new_node.parent = self.NIL

        parent = self.NIL
        current = self.root

        while current != self.NIL:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                current.value = value
                return

        new_node.parent = parent

        if parent == self.NIL:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self.insert_fixup(new_node)

    def insert_fixup(self, z):
        """
        Repara el árbol tras una inserción.
        """
        while z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right

                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)

                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left

                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)

                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.left_rotate(z.parent.parent)

        self.root.color = BLACK

    def left_rotate(self, x):
        """
        Rotación simple a la izquierda.
        """
        y = x.right
        x.right = y.left

        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, y):
        """
        Rotación simple a la derecha.
        """
        x = y.left
        y.left = x.right

        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent

        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

    def show(self):
        """
        Imprime el árbol girado 90 grados.
        """
        def _show(node, level):
            if node == self.NIL:
                return
            _show(node.right, level + 1)
            print("    " * level + str(node.key) + " (" + node.color + ")")
            _show(node.left, level + 1)

        if self.root == self.NIL:
            print("(árbol vacío)")
        else:
            _show(self.root, 0)

    def height(self):
        """
        Devuelve la altura del árbol.
        Árbol vacío -> -1
        """
        def _height(node):
            if node == self.NIL:
                return -1
            left_height = _height(node.left)
            right_height = _height(node.right)
            return 1 + max(left_height, right_height)

        return _height(self.root)

    def _search_node(self, key):
        """
        Busca y devuelve el nodo interno.
        """
        current = self.root

        while current != self.NIL:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        return self.NIL

    def find_node(self, key):
        """
        Busca una clave y devuelve (key, value) o None.
        """
        node = self._search_node(key)
        if node == self.NIL:
            return None
        return (node.key, node.value)

    def minimum(self, node):
        """
        Devuelve el nodo mínimo a partir de un nodo dado.
        """
        current = node
        while current.left != self.NIL:
            current = current.left
        return current

    def transplant(self, u, v):
        """
        Sustituye el subárbol de u por el de v.
        """
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        v.parent = u.parent

    def delete(self, key):
        """
        Elimina un nodo por clave.
        """
        z = self._search_node(key)

        if z == self.NIL:
            return

        y = z
        y_original_color = y.color

        if z.left == self.NIL:
            x = z.right
            self.transplant(z, z.right)

        elif z.right == self.NIL:
            x = z.left
            self.transplant(z, z.left)

        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right

            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == BLACK:
            self.delete_fixup(x)

    def delete_fixup(self, x):
        """
        Repara el árbol tras una eliminación.
        """
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right

                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.left_rotate(x.parent)
                    w = x.parent.right

                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.right_rotate(w)
                        w = x.parent.right

                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left

                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.right_rotate(x.parent)
                    w = x.parent.left

                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.left_rotate(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.right_rotate(x.parent)
                    x = self.root

        x.color = BLACK

    def skew(self):
        """
        Devuelve True si existe algún nodo inclinado.
        Un nodo está inclinado si su balance no es -1, 0 o 1.
        """
        def _check(node):
            if node == self.NIL:
                return False, -1

            left_skewed, left_height = _check(node.left)
            right_skewed, right_height = _check(node.right)

            balance = left_height - right_height
            current_skewed = balance not in (-1, 0, 1)
            current_height = 1 + max(left_height, right_height)

            return left_skewed or right_skewed or current_skewed, current_height

        skewed, _ = _check(self.root)
        return skewed

    def count_nodes_tree(self):
        """
        Cuenta el número total de nodos.
        """
        def _count(node):
            if node == self.NIL:
                return 0
            return 1 + _count(node.left) + _count(node.right)

        return _count(self.root)

    def count_leafs(self):
        """
        Cuenta el número de hojas.
        """
        def _count(node):
            if node == self.NIL:
                return 0
            if node.left == self.NIL and node.right == self.NIL:
                return 1
            return _count(node.left) + _count(node.right)

        return _count(self.root)

    def longest_path(self):
        """
        Devuelve la ruta más larga desde la raíz hasta una hoja.
        """
        def _longest(node):
            if node == self.NIL:
                return []

            left_path = _longest(node.left)
            right_path = _longest(node.right)

            if len(left_path) >= len(right_path):
                return [node.key] + left_path
            else:
                return [node.key] + right_path

        return _longest(self.root)

    def root_key(self):
        if self.root == self.NIL:
            return None
        return self.root.key

    def left_of_root(self):
        if self.root == self.NIL:
            return None
        if self.root.left == self.NIL:
            return None
        return self.root.left.key

    def right_of_root(self):
        if self.root == self.NIL:
            return None
        if self.root.right == self.NIL:
            return None
        return self.root.right.key


def paths_to_leaf_with_length(node, nil_node, remaining_edges, current_path=None, results=None):
    """
    Devuelve todos los caminos raíz->hoja con longitud exacta
    igual a remaining_edges al comenzar la llamada.
    """
    if current_path is None:
        current_path = []

    if results is None:
        results = []

    if node == nil_node:
        return results

    current_path.append(str(node.key))

    left_is_empty = node.left == nil_node
    right_is_empty = node.right == nil_node
    is_leaf = left_is_empty and right_is_empty

    if is_leaf:
        if remaining_edges == 0:
            results.append(current_path.copy())
    else:
        if remaining_edges > 0:
            if not left_is_empty:
                paths_to_leaf_with_length(node.left, nil_node, remaining_edges - 1, current_path, results)
            if not right_is_empty:
                paths_to_leaf_with_length(node.right, nil_node, remaining_edges - 1, current_path, results)

    current_path.pop()
    return results


def in_order(tree):
    _in_order(tree.root, tree.NIL)


def _in_order(node, NIL):
    if node == NIL:
        return
    _in_order(node.left, NIL)
    print(node.key)
    _in_order(node.right, NIL)


def pre_order(tree):
    _pre_order(tree.root, tree.NIL)


def _pre_order(node, NIL):
    if node == NIL:
        return
    print(node.key)
    _pre_order(node.left, NIL)
    _pre_order(node.right, NIL)


def post_order(tree):
    _post_order(tree.root, tree.NIL)


def _post_order(node, NIL):
    if node == NIL:
        return
    _post_order(node.left, NIL)
    _post_order(node.right, NIL)
    print(node.key)


def level_order(tree):
    if tree.root == tree.NIL:
        return

    cola = Queue(1000)
    cola.enqueue(tree.root)

    while not cola.is_empty():
        nodo = cola.dequeue()
        print(nodo.key)

        if nodo.left != tree.NIL:
            cola.enqueue(nodo.left)

        if nodo.right != tree.NIL:
            cola.enqueue(nodo.right)


if __name__ == "__main__":
    print("==========================================")
    print(" PRUEBAS ÁRBOL ROJO-NEGRO DESDE CERO ")
    print("==========================================")

    tree = RedBlackTree()

    tree.insert(8, "valor_8")
    tree.insert(3, "valor_3")
    tree.insert(10, "valor_10")
    tree.insert(1, "valor_1")
    tree.insert(6, "valor_6")
    tree.insert(14, "valor_14")
    tree.insert(4, "valor_4")
    tree.insert(7, "valor_7")
    tree.insert(13, "valor_13")

    print("\n1) Mostrar árbol:")
    tree.show()

    print("\n2) Buscar nodos:")
    print("Buscar 6 ->", tree.find_node(6))
    print("Buscar 20 ->", tree.find_node(20))

    print("\n3) Altura del árbol:")
    print(tree.height())

    print("\n4) Número de nodos:")
    print(tree.count_nodes_tree())

    print("\n5) Número de hojas:")
    print(tree.count_leafs())

    print("\n6) Ruta más larga:")
    print(tree.longest_path())

    print("\n7) ¿Está inclinado?:")
    print(tree.skew())

    print("\n8) Raíz e hijos de la raíz:")
    print("Raíz:", tree.root_key())
    print("Izquierda de raíz:", tree.left_of_root())
    print("Derecha de raíz:", tree.right_of_root())

    print("\n9) Caminos raíz-hoja con 3 aristas:")
    print(paths_to_leaf_with_length(tree.root, tree.NIL, 3))

    print("\n10) In-order:")
    in_order(tree)

    print("\n11) Pre-order:")
    pre_order(tree)

    print("\n12) Post-order:")
    post_order(tree)

    print("\n13) Level-order:")
    level_order(tree)

    print("\n14) Borrar 10:")
    tree.delete(10)
    tree.show()

    print("\n15) In-order final:")
    in_order(tree)
