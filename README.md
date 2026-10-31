# Word Search Trees

A Python university project that builds binary search trees from a Spanish word dataset and explores their structure using recursive algorithms.

## Features

- Filter words by their initial letter.
- Build trees using the dataset order or a randomized insertion order.
- Count nodes and leaves.
- Inspect the root and its children.
- Calculate tree height.
- Find the longest root-to-leaf path.
- Find root-to-leaf paths with a specified number of edges.

## Requirements

Python 3.9 or later. No external dependencies are required.

## How to run

Keep all project files in the same folder. Open a terminal in that folder and run:

```bash
python Proyecto.py
```

The interface is in Spanish:

1. Enter up to three initial letters, one at a time.
2. Submit an empty line to finish entering letters early.
3. Choose an insertion mode:
   - `d`: original dataset order.
   - `a`: randomized order.
4. Read the tree analysis for each selected letter.

## Project structure

- `Proyecto.py`: interactive interface, word loading, and recursive tree analysis.
- `BinaryTree.py`: binary search tree implementation used by the main program.
- `RedBlackTree.py`: additional red-black tree implementation, not used by the main program.
- `palabras_RAE_cleaned_noaccents.txt`: word dataset used as input.

## Academic context

This project explores data structures, recursion, tree traversal, and the relationship between insertion order and binary search tree structure.
