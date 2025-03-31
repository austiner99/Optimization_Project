import pstats
p = pstats.Stats('output.prof')
p.sort_stats('time').print_stats(10)
