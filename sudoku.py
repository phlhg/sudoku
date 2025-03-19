def solve(data):
  graph = create_graph(data)
  field = data

  remaining = set()
  all_colors = set(range(1,10))

  for id in graph.get_nodes():
    if graph.get_value(id) == None:
      remaining.add(id)
  
  while len(remaining) > 0:
    id = next((id for id in remaining if len(graph.neighbor_values(id)) >= 8), None)

    if not id:
      raise SolverException('Not solvable', field)

    colors = graph.neighbor_values(id)
    difference = all_colors.difference(colors)

    if len(difference) != 1:
      raise SolverException('Unexpected', field)
    
    value = difference.pop()
    graph.set_value(id, value)
    field[id[0]][id[1]] = value

    remaining.remove(id)

    # Uncomment to see steps
    print_field(field, selected=id, highlighted=graph.neighbors(id))

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
    
    self.adjeceny[id] = set()
    self.set_value(id, value)

  def get_nodes(self):
    return self.nodes.keys()

  def set_value(self, id, value):
    self.nodes[id] = value

  def get_value(self, id):
    return self.nodes[id]

  def add_edge(self, id_from, id_to):
    self.adjeceny[id_from].add(id_to)

  def neighbors(self, id):
    return self.adjeceny[id]
  
  def neighbor_values(self, id):
    values = set(map(lambda id: self.get_value(id), self.neighbors(id)))
    values.discard(None)
    return values


class SolverException(Exception):
  def __init__(self, message, field):
    super().__init__(message)
    self.field = field