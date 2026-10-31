class Node:
    def __init__(self, key, value=None):
        """
        Crea un nodo del árbol binario de búsqueda.

        Parámetros:
        ----------
        key : any
            Clave del nodo. Se usa para ordenar dentro del árbol.
        value : any, opcional
            Dato adicional asociado al nodo.
        """
        self._parent = None
        self._left = None
        self._right = None
        self.key = key
        self.data = value

    def get_left(self) -> 'Node':
        """Devuelve el hijo izquierdo."""
        return self._left

    def get_right(self) -> 'Node':
        """Devuelve el hijo derecho."""
        return self._right

    def set_left(self, node) -> None:
        """
        Asigna el hijo izquierdo y actualiza su padre.
        """
        self._left = node
        if node is not None:
            node._parent = self

    def set_right(self, node) -> None:
        """
        Asigna el hijo derecho y actualiza su padre.
        """
        self._right = node
        if node is not None:
            node._parent = self

    def min(self):
        """
        Devuelve el nodo con la clave mínima del subárbol actual.
        """
        current = self
        while current is not None and current._left is not None:
            current = current._left
        return current

    def max(self):
        """
        Devuelve el nodo con la clave máxima del subárbol actual.
        """
        current = self
        while current is not None and current._right is not None:
            current = current._right
        return current

    def successor(self):
        """
        Devuelve el sucesor in-order del nodo actual.
        Es el siguiente nodo en un recorrido in-order.
        """
        node = self

        if node is None:
            return None

        # Si tiene subárbol derecho, el sucesor es el mínimo de ese subárbol
        if node._right is not None:
            return node._right.min()

        # Si no tiene subárbol derecho, subimos hasta encontrar
        # un ancestro del que este nodo esté en la rama izquierda
        current = node
        parent = node._parent
        while parent is not None and current == parent._right:
            current = parent
            parent = parent._parent

        return parent

    def predecessor(self):
        """
        Devuelve el predecesor in-order del nodo actual.
        Es el nodo anterior en un recorrido in-order.
        """
        node = self

        if node is None:
            return None


        # Si tiene subárbol izquierdo, el predecesor es el máximo de ese subárbol
        if node._left is not None:
            return node._left.max()

        # Si no tiene subárbol izquierdo, subimos hasta encontrar
        # un ancestro del que este nodo esté en la rama derecha
        current = node
        parent = current._parent
        while parent is not None and current == parent._left:
            current = parent
            parent = parent._parent

        return parent

    def leaf(self):
        """
        Devuelve True si el nodo es hoja, False en caso contrario.
        """
        return self._left is None and self._right is None

    def show(self, level=0, prefix="Root: ") -> None:
        """
        Muestra el árbol de forma jerárquica por pantalla.
        """
        indent = "    " * level
        print(f"{indent}{prefix}{self.key}")

        if self.get_left() is not None:
            self.get_left().show(level + 1, prefix="L--- ")
        if self.get_right() is not None:
            self.get_right().show(level + 1, prefix="R--- ")

    def height(self):
        """
        Devuelve la altura del subárbol cuya raíz es este nodo.
        Convención:
        - Un nodo hoja tiene altura 0
        - Un árbol vacío tendría altura -1
        """
        if self._left is not None:
            height_left = self._left.height()
        else:
            height_left = -1

        if self._right is not None:
            height_right = self._right.height()
        else:
            height_right = -1

        return 1 + max(height_left, height_right)

    def inorder(self):
        """
        Recorrido in-order:
        izquierda -> raíz -> derecha
        """
        if self._left is not None:
            self._left.inorder()
        print(self.key)
        if self._right is not None:
            self._right.inorder()

    def preorder(self):
        """
        Recorrido pre-order:
        raíz -> izquierda -> derecha
        """
        print(self.key)
        if self._left is not None:
            self._left.preorder()
        if self._right is not None:
            self._right.preorder()

    def postorder(self):
        """
        Recorrido post-order:
        izquierda -> derecha -> raíz
        """
        if self._left is not None:
            self._left.postorder()
        if self._right is not None:
            self._right.postorder()
        print(self.key)


def node_clone(node: Node):
    """
    Crea una copia superficial del nodo:
    copia clave y dato, pero no hijos ni padre.
    """
    return Node(node.key, node.data)


def swap_contents(node1, node2):
    """
    Intercambia la clave y el dato de dos nodos.
    """
    node1.key, node2.key = node2.key, node1.key
    node1.data, node2.data = node2.data, node1.data


class BinaryTree:
    def __init__(self, root=None):
        """
        Inicializa el árbol binario de búsqueda.

        Parámetros:
        ----------
        root : Node, opcional
            Nodo raíz inicial del árbol.
        """
        self.root = root

    def find_min(self):
        """
        Devuelve el nodo mínimo del árbol.
        """
        if self.root is None:
            return None
        return self.root.min()

    def find_max(self):
        """
        Devuelve el nodo máximo del árbol.
        """
        if self.root is None:
            return None
        return self.root.max()

    def insert(self, key, value=None):
        """
        Inserta un nuevo nodo en el árbol siguiendo
        la propiedad del BST.
        """
        newnode = Node(key, value)

        if self.root is None:
            self.root = newnode
            return

        node = self.root
        parent = None

        while node is not None:
            parent = node
            if key < node.key:
                node = node._left
            else:
                node = node._right

        if key < parent.key:
            parent.set_left(newnode)
        else:
            parent.set_right(newnode)

    def show(self):
        """
        Muestra el árbol por pantalla.
        """
        if self.root is None:
            print("(árbol vacío)")
        else:
            self.root.show()

    def height(self):
        """
        Devuelve la altura del árbol.
        Si está vacío, devuelve -1.
        """
        if self.root is None:
            return -1
        return self.root.height()

    def find_node(self, key):
        """
        Busca un nodo por su clave y lo devuelve.
        Si no existe, devuelve None.
        """
        node = self.root
        while node is not None:
            if key < node.key:
                node = node._left
            elif key > node.key:
                node = node._right
            else:
                return node
        return None

    def _transplant(self, u, v):
        """
        Sustituye el subárbol con raíz en u
        por el subárbol con raíz en v.
        """
        if u._parent is None:
            self.root = v
        elif u == u._parent._left:
            u._parent._left = v
        else:
            u._parent._right = v

        if v is not None:
            v._parent = u._parent

    def delete(self, key):
        """
        Elimina el nodo con la clave indicada.
        Maneja los tres casos:
        - nodo hoja
        - nodo con un hijo
        - nodo con dos hijos
        """
        node = self.find_node(key)

        if node is None:
            return False

        # Caso 1: no tiene hijo izquierdo
        if node._left is None:
            self._transplant(node, node._right)

        # Caso 2: no tiene hijo derecho
        elif node._right is None:
            self._transplant(node, node._left)

        # Caso 3: tiene dos hijos
        else:
            successor = node._right.min()

            # Si el sucesor no es el hijo derecho directo,
            # primero reubicamos el subárbol del sucesor
            if successor._parent != node:
                self._transplant(successor, successor._right)
                successor._right = node._right
                if successor._right is not None:
                    successor._right._parent = successor

            self._transplant(node, successor)
            successor._left = node._left
            if successor._left is not None:
                successor._left._parent = successor

        return True

    def skew(self) -> bool:
        """
        Comprueba si la diferencia de alturas entre el subárbol izquierdo
        y derecho de la raíz es como máximo 1.

        Ojo: esto NO comprueba si TODO el árbol está balanceado,
        solo compara la raíz.
        """
        if self.root is None:
            return True

        left = self.root._left
        right = self.root._right

        alt_left = left.height() if left is not None else -1
        alt_right = right.height() if right is not None else -1

        return abs(alt_right - alt_left) <= 1


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


def in_order(tree: BinaryTree) -> None:
    """
    Ejecuta el recorrido in-order del árbol.
    """
    if tree.root is not None:
        tree.root.inorder()


def pre_order(tree: BinaryTree) -> None:
    """
    Ejecuta el recorrido pre-order del árbol.
    """
    if tree.root is not None:
        tree.root.preorder()


def post_order(tree: BinaryTree) -> None:
    """
    Ejecuta el recorrido post-order del árbol.
    """
    if tree.root is not None:
        tree.root.postorder()


def level_order(tree: BinaryTree) -> None:
    """
    Recorre el árbol por niveles usando una cola.
    """
    if tree.root is not None:
        cola = Queue(100)
        cola.enqueue(tree.root)

        while not cola.is_empty():
            nodo = cola.dequeue()
            print(nodo.key)

            if nodo._left is not None:
                cola.enqueue(nodo._left)

            if nodo._right is not None:
                cola.enqueue(nodo._right)


if __name__ == "__main__":
    print("=" * 50)
    print("PRUEBAS DEL ÁRBOL BINARIO DE BÚSQUEDA")
    print("=" * 50)

    # Crear árbol
    tree = BinaryTree()

    # Insertar nodos
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)
    tree.insert(2)
    tree.insert(7)
    tree.insert(12)
    tree.insert(20)


    print("\n1) Mostrar árbol:")
    tree.show()

    print("\n2) Buscar mínimo y máximo:")
    nodo_min = tree.find_min()
    nodo_max = tree.find_max()
    print("Mínimo:", nodo_min.key)
    print("Máximo:", nodo_max.key) 

    print("\n3) Buscar nodos:")
    buscado = tree.find_node(7)
    print("Nodo 7 encontrado:", buscado.key)


    print("\n4) Altura del árbol:")
    print("Altura:", tree.height())


    print("\n5) Recorridos:")
    print("In-order:")
    in_order(tree)

    print("\nPre-order:")
    pre_order(tree)

    print("\nPost-order:")
    post_order(tree)

    print("\nLevel-order:")
    level_order(tree)

    print("\n===== SKEW =====")
    print("¿Balanceado raíz?:", tree.skew())

    print("\n9) Borrado de nodo hoja (8):")
    tree.delete(8)
    tree.show()

    print("\n10) Borrado de nodo con un hijo (7):")
    tree.delete(7)
    tree.show()

    print("\n11) Borrado de nodo con dos hijos (15):")
    tree.delete(15)
    tree.show()

    print("\n12) Borrado de la raíz (10):")
    tree.delete(10)
    tree.show()

