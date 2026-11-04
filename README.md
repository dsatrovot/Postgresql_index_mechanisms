# Postgresql_index_mechanisms
Мой анализ механизмов postgresql индексации через python код(разбор алгоритмов и структур данных использующихся там).

Примерная работа индексов по файлам:
  -  BRIN -> brin.py
  -  GIN -> gin.py
  -  SP-GIST -> raddix_tree.py(может когда-то посмотрю как реализуется Quadtree и k-d tree для координат)
  -  Hash - hash_index.py
