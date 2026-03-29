# ME5413_HW3
-- by Mai Jingyang, please contact maijy1010@163.com for any questions.

## What we do

Task1, 
- Try 3 heuristic functions in A*: 
    - Manhattan
    - Euclidean
    - Chebyshev
- Degenerate the A* to:
    - Dijkstra’s Algorithm
    - Greedy Best First Search (GBFS) Algorithm
- Visualtion

Task2,

- Model the problem as a Traveling Salesman Problem (TSP) problem
- Use two method to solve it:
    - Floyd
    - Dijkstra

---

Make sure you have the following folder structure:

Project-Root/ 
├── README.md
├── homework3.ipynd
├── E1373698_Homework3.pdf
├── src/...
├── map/ 
|   ├── vivocity_freespace_raw.png 
|   └── ...
└── res/ 
    ├── 8-ngb_Manhattan_res.txt
    ├── 8-ngb_Dij_res.txt
    └── ...


## How to use

- Simply run the `homework3.ipynb` block by block (without miising any folded one).
- In Task1, 
    - you can change the `h_MODE` and `g_MODE` to change the cost-to-go h(x) and cost-so-far g(x) that you want to use,
    - you can also change `ngb_MODE` to choose 4 neighbour exploration region or 8 neighbour.
- In Task2, 
    - you can change the same parameters mentioned above to form the distance cost between each two locations.