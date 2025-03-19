def solve(data):
  graph = create_graph(data)
  field = data

  remaining = {}
  all_colors = set(range(1,10))

  for id in graph.get_nodes():
    # Field is already solved
    if graph.get_value(id) != None:
      continue

    values = set(map(lambda i: graph.get_value(i), graph.neighbors(id)))
    values.remove(None)

    if len(values) > 8:
      raise SolverException('Overconstrained - Not solvable', field)
    
    remaining[id] = values
  
  while len(remaining.keys()) > 0:
    id = next((id for id in remaining.keys() if len(remaining[id]) >= 8), None)

    if not id:
      raise SolverException('Not solvable', field)

    neighbors = set(graph.neighbors(id))
    difference = all_colors.difference(remaining[id])

    if len(difference) != 1:
      raise SolverException('Unexpected', field)
    
    value = difference.pop()
    graph.set_value(id, value)
    field[id[0]][id[1]] = value

    for nid in neighbors:
      if nid in remaining:
        remaining[nid].add(value)

    del remaining[id]

    # Uncomment to see steps
    print_field(field, selected=id, highlighted=neighbors)

  return field


def create_graph(data):
  graph = Graph()
  length = len(data)

  for i in range(0, length):
    for j in range(0, length):
      graph.add_node((i, j), data[i][j])
  
  for i in range(0, length):
    origin_i = i - i % 3
    for j in range(0, length):
      origin_j = j - j % 3

      for k in range(0, length):
        # Row constraints
        if k != i: 
          graph.add_edge((i, j),(k, j))

        # Column constraints
        if k != j:
          graph.add_edge((i, j),(i, k))

      # Subfield constraints
      for k in range(0, 3):
        target_i = origin_i + k
        for l in range(0, 3):
          target_j = origin_j + l
          if target_i != i or target_j != j:
            graph.add_edge((i, j), (target_i, target_j))

  return graph

def check_field(field):
  length = len(field)
  for k in range(0, length):
    row = set(field[k])
    col = set(field[l][k] for l in range(0, length))
    if len(row) != 9 or len(col) != 9:
      return False
  
  for i in range(0, 3):
    for j in range(0, 3):
      values = set(field[i * 3 + k][j * 3 + l] for k in range(0,3) for l in range(0,3))
      if len(values) != 9:
        return False
  
  return True

def print_field(field, selected=None, highlighted=[]):
  print('')

  field_len = len(field)
  for i in range(0,field_len):
    for j in range(0,field_len):
      value = field[i][j]
      if (i,j) == selected:
        print(f'\33[32m{value or '.'}\33[0m  ', end='')
      elif (i,j) in highlighted:
        print(f'\33[34m{value or '.'}\33[0m  ', end='')
      else:
        print(f'{value or '\33[90m.\33[0m'}  ', end='')
    print('')


class Graph:
  def __init__(self):
    self.nodes = {}
    self.adjeceny = {}

  def add_node(self, id, value = None):
    if id in self.nodes:
      raise Exception(f'Node {id} already exists!')
    
    self.adjeceny[id] = []
    self.set_value(id, value)

  def get_nodes(self):
    return self.nodes.keys()

  def set_value(self, id, value):
    self.nodes[id] = value

  def get_value(self, id):
    return self.nodes[id]

  def add_edge(self, id_from, id_to):
    self.adjeceny[id_from].append(id_to)

  def neighbors(self, id):
    return self.adjeceny[id]


class SolverException(Exception):
  def __init__(self, message, field):
    super().__init__(message)
    self.field = field