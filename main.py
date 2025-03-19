#!/usr/bin/python3

import sudoku

data = [
 [None,6   ,None, 9   ,1   ,5   , None,4   ,None],
 [1   ,None,3   , 4   ,None,7   , None,6   ,None],
 [None,2   ,4   , None,None,None, None,None,None],

 [None,3   ,None, 8   ,None,None, 9   ,2   ,6   ],
 [None,None,6   , 3   ,None,None, None,None,None],
 [None,None,1   , None,None,None, None,7   ,None],

 [7   ,4   ,9   , None,None,None, 6   ,None,5   ],
 [6   ,None,None, None,None,8   , 7   ,3   ,4   ],
 [3   ,5   ,None, 7   ,6   ,None, 2   ,1   ,9   ],
]

sudoku.print_field(data)

try:
  solution = sudoku.solve(data)
  print('')
  print(f'\33[32mSolved:\33[0m')
  sudoku.print_field(solution)

  # if not sudoku.check_field(solution):
  #   print('')
  #   print(f'\33[31mSolution is incorrect!\33[0m')

except sudoku.SolverException as e:
  print('')
  print(f'\33[31m{e}:\33[0m')
  sudoku.print_field(e.field)
print('')