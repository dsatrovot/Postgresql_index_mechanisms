from bisect import bisect_left, bisect_right



from bisect import bisect_left, bisect_right


class Leaf:
    """Лист B+ дерева."""

    def __init__(self):
        self.keys = []
        self.values = []
        self.next = None


class Internal:
    """Внутренний узел B+ дерева."""

    def __init__(self):
        self.keys = []
        self.children = []


class BPlusTree:

    def __init__(self, max_keys=3):
        if max_keys < 3:
            raise ValueError("max_keys должен быть не меньше 3")

        self.max_keys = max_keys

        # Минимальное количество ключей в листе.
        self.min_leaf_keys = (max_keys + 1) // 2

        # Максимум детей = max_keys + 1.
        # Минимум детей = ceil((max_keys + 1) / 2).
        self.min_children = (max_keys + 2) // 2

        self.root = Leaf()

    # ==================================================
    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ
    # ==================================================

    def _min_key(self, node):
        """Возвращает минимальный ключ поддерева."""

        while isinstance(node, Internal):
            node = node.children[0]

        if not node.keys:
            raise RuntimeError("Обнаружен пустой лист внутри дерева")

        return node.keys[0]

    def _refresh_keys(self, node):
        """
        Пересчитывает ключи-разделители.

        Каждый разделитель равен минимальному ключу
        соответствующего правого дочернего поддерева.
        """

        if isinstance(node, Internal):
            node.keys = [
                self._min_key(child)
                for child in node.children[1:]
            ]

    # ==================================================
    # ПОИСК
    # ==================================================

    def search(self, key):

        node = self.root

        # Спускаемся по внутренним узлам.
        while isinstance(node, Internal):
            index = bisect_right(node.keys, key)
            node = node.children[index]

        # Ищем ключ в листе.
        index = bisect_left(node.keys, key)

        if index < len(node.keys) and node.keys[index] == key:
            return node.values[index]

        return None

    # ==================================================
    # ВСТАВКА
    # ==================================================

    def insert(self, key, value):

        split = self._insert_recursive(
            self.root,
            key,
            value
        )

        # Если корень разделился,
        # создаём новый корень.
        if split is not None:

            new_root = Internal()

            new_root.children = [
                self.root,
                split
            ]

            self._refresh_keys(new_root)

            self.root = new_root

    def _insert_recursive(self, node, key, value):

        # ----------------------------------------------
        # Вставка в лист
        # ----------------------------------------------

        if isinstance(node, Leaf):

            index = bisect_left(node.keys, key)

            # Если ключ существует — обновляем значение.
            if (
                index < len(node.keys)
                and node.keys[index] == key
            ):
                node.values[index] = value
                return None

            node.keys.insert(index, key)
            node.values.insert(index, value)

            # Переполнения нет.
            if len(node.keys) <= self.max_keys:
                return None

            # Разделяем переполненный лист.
            middle = len(node.keys) // 2

            right = Leaf()

            right.keys = node.keys[middle:]
            right.values = node.values[middle:]

            node.keys = node.keys[:middle]
            node.values = node.values[:middle]

            # Поддерживаем связанный список листьев.
            right.next = node.next
            node.next = right

            return right

        # ----------------------------------------------
        # Вставка во внутренний узел
        # ----------------------------------------------

        index = bisect_right(node.keys, key)

        split = self._insert_recursive(
            node.children[index],
            key,
            value
        )

        # Если ребёнок разделился,
        # добавляем ссылку на новый правый узел.
        if split is not None:
            node.children.insert(index + 1, split)

        self._refresh_keys(node)

        # Переполнения нет.
        if len(node.children) <= self.max_keys + 1:
            return None

        # Разделяем внутренний узел.
        middle = len(node.children) // 2

        right = Internal()

        right.children = node.children[middle:]
        node.children = node.children[:middle]

        self._refresh_keys(node)
        self._refresh_keys(right)

        return right

    # ==================================================
    # УДАЛЕНИЕ
    # ==================================================

    def delete(self, key):

        deleted = self._delete_recursive(
            self.root,
            key
        )

        # Если у корня остался один ребёнок,
        # этот ребёнок становится новым корнем.
        if isinstance(self.root, Internal):

            if len(self.root.children) == 1:
                self.root = self.root.children[0]

        return deleted

    def _delete_recursive(self, node, key):

        # ----------------------------------------------
        # Удаление из листа
        # ----------------------------------------------

        if isinstance(node, Leaf):

            index = bisect_left(node.keys, key)
            print(f"{key} -> {index} -> {node.keys}")
            if (
                index >= len(node.keys)
                or node.keys[index] != key
            ):
                return False

            node.keys.pop(index)
            node.values.pop(index)

            return True

        # ----------------------------------------------
        # Удаление из внутреннего узла
        # ----------------------------------------------

        index = bisect_right(node.keys, key)

        child = node.children[index]

        deleted = self._delete_recursive(child, key)

        if not deleted:
            return False

        # Проверяем минимальную заполненность ребёнка.
        if isinstance(child, Leaf):
            print(f"underflow -> {len(child.keys)}")
            underflow = (
                len(child.keys) < self.min_leaf_keys
            )

        else:

            underflow = (
                len(child.children) < self.min_children
            )

        # Если возник underflow — балансируем.
        if underflow:
            print(f"underflow -> {node.keys}")
            print(f"node index keys -> {index}, {node.keys} ")
            self._rebalance(node, index)

        # Обязательно пересчитываем разделители.
        print(f"{node.keys} -> check root recur")
        self._refresh_keys(node)
        print(f"{node.keys} -> check root recur2 -> {node.children[0].keys}")

        return True

    # ==================================================
    # БАЛАНСИРОВКА ПОСЛЕ УДАЛЕНИЯ
    # ==================================================

    def _rebalance(self, parent, index):

        child = parent.children[index]

        left = (
            parent.children[index - 1]
            if index > 0
            else None
        )
        for i in parent.children:
            print(f"rebalance -> {i.keys} ")

        right = (
            parent.children[index + 1]
            if index + 1 < len(parent.children)
            else None
        )

        is_leaf = isinstance(child, Leaf)

        if is_leaf:
            min_size = self.min_leaf_keys
        else:
            min_size = self.min_children

        # ----------------------------------------------
        # 1. Заимствование у левого соседа
        # ----------------------------------------------

        if left is not None:

            if is_leaf:
                can_borrow = len(left.keys) > min_size
            else:
                can_borrow = (
                    len(left.children) > min_size
                )

            if can_borrow:

                if is_leaf:

                    # Перемещаем последний ключ
                    # левого листа в начало текущего.
                    child.keys.insert(
                        0,
                        left.keys.pop()
                    )

                    child.values.insert(
                        0,
                        left.values.pop()
                    )

                else:

                    # Перемещаем последнего ребёнка
                    # левого внутреннего узла.
                    child.children.insert(
                        0,
                        left.children.pop()
                    )

                    # ВАЖНО: обновляем оба узла.
                    self._refresh_keys(left)
                    self._refresh_keys(child)

                self._refresh_keys(parent)
                return

        # ----------------------------------------------
        # 2. Заимствование у правого соседа
        # ----------------------------------------------

        if right is not None:

            if is_leaf:
                can_borrow = len(right.keys) > min_size
            else:
                can_borrow = (
                    len(right.children) > min_size
                )

            if can_borrow:

                if is_leaf:

                    # Перемещаем первый ключ
                    # правого листа в конец текущего.
                    child.keys.append(
                        right.keys.pop(0)
                    )

                    child.values.append(
                        right.values.pop(0)
                    )

                else:

                    # Перемещаем первого ребёнка
                    # правого внутреннего узла.
                    child.children.append(
                        right.children.pop(0)
                    )

                    # ВАЖНО: обновляем оба узла.
                    self._refresh_keys(child)
                    self._refresh_keys(right)

                self._refresh_keys(parent)
                return

        # ----------------------------------------------
        # 3. Слияние с левым соседом
        # ----------------------------------------------

        if left is not None:

            if is_leaf:

                left.keys.extend(child.keys)
                left.values.extend(child.values)

                # Обновляем связанный список листьев.
                left.next = child.next

            else:

                left.children.extend(child.children)

                self._refresh_keys(left)

            # Удаляем ссылку на объединённый узел.
            for i in parent.children:
                print(i.keys, index)
            parent.children.pop(index)
            for i in parent.children:
                print(i.keys, index)
            print(f"{parent.keys} _debug_rebalance 0")
            self._refresh_keys(parent)
            print(f"{parent.keys} _debug rebalance")
            return

        # ----------------------------------------------
        # 4. Слияние с правым соседом
        # ----------------------------------------------

        if right is not None:

            if is_leaf:

                child.keys.extend(right.keys)
                child.values.extend(right.values)

                child.next = right.next

            else:

                child.children.extend(right.children)

                self._refresh_keys(child)

            parent.children.pop(index + 1)

            self._refresh_keys(parent)

    # ==================================================
    # ПОИСК ПО ДИАПАЗОНУ
    # ==================================================

    def range_search(self, start, end):

        result = []

        node = self.root

        # Находим лист, где может находиться start.
        while isinstance(node, Internal):

            index = bisect_right(node.keys, start)
            node = node.children[index]

        # Идём по связанным листьям.
        while node is not None:

            for key, value in zip(
                node.keys,
                node.values
            ):

                if key < start:
                    continue

                if key > end:
                    return result

                result.append((key, value))

            node = node.next

        return result

    # ==================================================
    # ВЫВОД ДЕРЕВА
    # ==================================================

    def print_tree(self):

        queue = [(self.root, 0)]

        current_level = 0

        print("B+ TREE")

        while queue:

            node, level = queue.pop(0)

            if level != current_level:

                print()
                current_level = level

                print(f"LEVEL {level}:")

            if isinstance(node, Leaf):

                print(
                    f"  LEAF {node.keys}",
                    end=""
                )

            else:

                print(
                    f"  INTERNAL {node.keys}",
                    end=""
                )

                for child in node.children:
                    queue.append((child, level + 1))

        print()

    # ==================================================
    # ПРОВЕРКА СТРУКТУРНЫХ ИНВАРИАНТОВ
    # ==================================================

    def validate(self):

        leaves = []

        def check(node, is_root=True):

            if isinstance(node, Leaf):

                assert len(node.keys) == len(node.values)
                assert node.keys == sorted(node.keys)

                if not is_root:
                    assert (
                        self.min_leaf_keys
                        <= len(node.keys)
                        <= self.max_keys
                    )

                leaves.append(node)

                if node.keys:
                    return node.keys[0], node.keys[-1]

                return None, None

            assert len(node.children) == len(node.keys) + 1

            expected_keys = [
                self._min_key(child)
                for child in node.children[1:]
            ]

            assert node.keys == expected_keys

            if is_root:
                assert len(node.children) >= 2
            else:
                assert (
                    self.min_children
                    <= len(node.children)
                    <= self.max_keys + 1
                )

            ranges = [
                check(child, False)
                for child in node.children
            ]

            for i in range(1, len(ranges)):
                assert ranges[i - 1][1] < ranges[i][0]

            return ranges[0][0], ranges[-1][1]

        check(self.root)

        # Проверяем цепочку листьев.
        for left, right in zip(leaves, leaves[1:]):
            assert left.next is right

        assert leaves[-1].next is None

        return True


# ======================================================
# ПРИМЕР ИСПОЛЬЗОВАНИЯ
# ======================================================

if __name__ == "__main__":

    tree = BPlusTree(max_keys=3)

    # Вставляем ключи.
    for key in range(10, 101, 10):
        tree.insert(key, f"value-{key}")

    print("ДО УДАЛЕНИЯ:")
    tree.print_tree()

    # Удаляем ключ 30.
    print("\nУДАЛЯЕМ 30:")
    print("Deleted:", tree.delete(30))

    print("\nПОСЛЕ УДАЛЕНИЯ:")
    tree.print_tree()

    print("\nУДАЛЯЕМ 60:")
    print("Deleted:", tree.delete(60))
    tree.print_tree()

    # print("\nУДАЛЯЕМ 40:")
    # print("Deleted:", tree.delete(40))
    # tree.print_tree()

    # Проверяем поиск.
    print("\nПРОВЕРКА ПОИСКА:")

    for key in range(10, 101, 10):
        print(key, "->", tree.search(key))

    # Проверяем диапазон.
    print("\nПОИСК ПО ДИАПАЗОНУ 40-80:")
    print(tree.range_search(40, 80))

    # Проверяем структуру дерева.
    print("\nVALIDATE:", tree.validate())



# tree = BPlusTree(max_keys=3)

