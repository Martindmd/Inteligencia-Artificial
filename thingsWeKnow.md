# Orden de tareas

## A.1.1: Generación del árbol de juego (search.py)

Rellenar los "YOUR CODE HERE" de search.py empleando las funciones de reversi.py

- [x] legalMoves()
- [x] result()
- [ ] Implementar la función build_game_tree en search.py <- M

Probar vuestro código (basta con lanzarlo como “python search.py”) utilizando las profundidades 1, 2, 3 y 4 sobre el tablero inicial de Reversi

## A.1.2: Exploración mediante búsqueda clásica (search.py)

Es útil usar util.py
Estas funciones deben devolver: 
1. La lista de movimientos legales que llevan al agente desde la situación inicial hasta la objetivo. Si el algoritmo no encuentra solución debe devolver None.
2. La lista de nodos visitados

Se aplican sobre tableros iniciales y el código debe además medir:
1. Nº de nodos visitados
2. Orden de exploración de los nodos [Una pila / cola y ya??]

> Completa el fichero search.py para que se obtenga esta información simplemente haciendo “python search.py”.

- [ ] Complementar la Búsqueda en profundidad (depthFirstSearch()) <- A
- [ ] Crear la función para la Búsqueda en anchura (breadthFirstSearch()) creando un estado de búsqueda que incluya: <- M
   1. Info sobre etapa actual en la búsqueda
   2. Info suficiente para poder acceder a la trayectoria desde el principio hasta el final

## A.2: Aplicando búsqueda informada (search.py)

- [ ] aStarSearch() <- A

Toma dos argumentos:
1. Un estado del problema de búsqueda
2. El problema en sí (info de referencia)

- [ ] heuristic1() <- AM
- [ ] heuristic2() <- None
- [ ] heuristic3() <- None