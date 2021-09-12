import sys
import typing
from typing import Optional


sys.setrecursionlimit(100000)
inf = 10**20
AvlNodeT = typing.TypeVar('T', bound='AvlNode')


class AvlTreeException(Exception):
    pass


class AvlTreeDuplicatedKeyFoundException(Exception):
    pass


class AvlNode(object):
    '''
    平衡二分木の1実装である、AVL木のノードです。
    '''

    def __init__(self, key, data=None):
        """ AVL木のノードを得る。 """
        self._key = key
        self._data = data
        self._left: Optional[AvlNodeT] = None
        self._right: Optional[AvlNodeT] = None
        self._height: int = 1

    def update_node_height(self):
        """ 左右のノードの高さをもとに、このノードの高さを更新する。 """
        self._height = 1 + max(
                self._get_left_height(), self._get_right_height())

    def _get_node_height_from_node_or_none(
            self, node_or_none: Optional[AvlNodeT]):
        return 0 if node_or_none is None else node_or_none.height

    def _get_left_height(self) -> int:
        return self._get_node_height_from_node_or_none(self._left)

    def _get_right_height(self) -> int:
        return self._get_node_height_from_node_or_none(self._right)

    def _get_bias(self) -> int:
        return self._get_left_height() - self._get_right_height()

    def is_balanced(self) -> bool:
        """ このノードのバイアスが平衡か判定する。 """
        return abs(self._get_bias()) <= 1

    def is_left_high_unbalanced(self) -> bool:
        """ 平衡でなく、かつ、左が高すぎるなら True を返す。 """
        return self._get_bias() == 2

    def is_right_high_unbalanced(self) -> bool:
        """ 平衡でなく、かつ、右が高すぎるなら True を返す。 """
        return self._get_bias() == -2

    def is_left_child_higher_or_equal(self) -> bool:
        return self._get_bias() >= 0

    def is_right_child_higher_or_equal(self) -> bool:
        return self._get_bias() <= 0

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def left(self) -> AvlNodeT:
        return self._left

    @left.setter
    def left(self, node: AvlNodeT):
        self._left = node

    @property
    def right(self) -> AvlNodeT:
        return self._right

    @right.setter
    def right(self, node: AvlNodeT):
        self._right = node

    @property
    def height(self) -> int:
        ''' 葉のノードの高さを1とする高さ。 '''
        return self._height

    @height.setter
    def height(self, height: int):
        self._height = height

    def __repr__(self):
        dic = {
                "key": self._key,
                "data": self._data,
                "has_left": self._left is not None,
                "has_right": self._right is not None,
                "height": self._height,
                "bias": self._get_bias(),
                }
        return "<AvlNode " + str(dic) + ">"


class AvlTree(object):
    def __init__(self):
        """ AVL木を得る。 """
        self._root: Optional[AvlNode] = None
        self._changes_needed: bool = False
        self._max_left_key = None
        self._max_left_data = None

    def _rotate_to_right(self, node1: AvlNode) -> AvlNode:
        ''' 右に回転する。 '''

        '''
                |       ->        |
             .node1.           .node2.
            |       |         |       |
         .node2.    |         |    .node1.
        |       |   |         |   |       |
        |       |   t3        t1  |       |
        t1      t2                t2      t3
        '''
        node2 = node1.left
        t2 = node2.right
        node2.right = node1
        node1.left = t2
        node2.right.update_node_height()
        node2.update_node_height()
        return node2

    def _rotate_to_left(self, node1: AvlNode) -> AvlNode:
        ''' 左に回転する。 '''

        '''
            |           ->            |
         .node1.                   .node2.
        |       |                 |       |
        |    .node2.           .node1.    |
        |   |       |         |       |   |
        t1  |       |         |       |   t3
            t2      t3        t1      t2
        '''
        node2 = node1.right
        t2 = node2.left
        node2.left = node1
        node1.right = t2
        node2.left.update_node_height()
        node2.update_node_height()
        return node2

    def _rotate_to_left_right(self, node1: AvlNode) -> AvlNode:
        """ 左回転後、右回転する。 """

        """
                  |                   |                |
          .-------f-.   ->        .---f-.   ->     .---d---.
          |         |             |     |          |       |
        .-b---.     g         .---d-.   g        .-b-.   .-f-.
        |     |               |     |            |   |   |   |
        a   .-d-.           .-b-.   e            a   c   e   g
            |   |           |   |
            c   e           a   c
        """
        node1.left = self._rotate_to_left(node1.left)
        return self._rotate_to_right(node1)

    def _rotate_to_right_left(self, node: AvlNode) -> AvlNode:
        node.right = self._rotate_to_right(node.right)
        return self._rotate_to_left(node)

    def _rebalance_left(self, node1: AvlNode) -> AvlNode:
        if not self._changes_needed:
            return node1

        height = node1.height
        if node1.is_left_high_unbalanced():
            node2: AvlNode = node1.left
            if node2.is_left_child_higher_or_equal():
                '''
                        |
                    .-node1-.
                    |       |
                .-node2-.   t2   -+-
                |       |         | bias == 2
                |       t12       |
                t11              -+-

                または

                        |
                    .-node1-.
                    |       |
                .-node2-.   t2   -+-
                |       |         | bias == 2
                t11     t12      -+-
                '''
                node1 = self._rotate_to_right(node1)
            else:
                '''
                          |
                    .-node1-.
                    |       |
                .-node2-.   t2   -+-
                |       |         | bias == 2
                t11     |         |
                        t12      -+-
                '''
                node1 = self._rotate_to_left_right(node1)
        else:
            node1.update_node_height()

        self._changes_needed = (height != node1.height)

        return node1

    def _rebalance_right(self, node1: AvlNode) -> AvlNode:
        if not self._changes_needed:
            return node1

        height = node1.height
        if node1.is_right_high_unbalanced():
            node2: AvlNode = node1.right
            if node2.is_right_child_higher_or_equal():
                '''
                      |
                  .-node1-.
                  |       |
                 t1   .-node2-.      -+-
                      |       |       | bias == 2
                      t21     |       |
                              |       |
                              t22    -+-

                または

                      |
                  .-node1-.
                  |       |
                 t1   .-node2-.      -+-
                      |       |       | bias == 2
                      t21     t22    -+-
                '''
                node1 = self._rotate_to_left(node1)
            else:
                '''
                      |
                  .-node1-.
                  |       |
                 t1   .-node2-.    -+-
                      |       |     | bias == 2
                      |       t21   |
                      |             |
                      t21          -+-
                '''
                node1 = self._rotate_to_right_left(node1)
        else:
            node1.update_node_height()

        self._changes_needed = (height != node1.height)

        return node1

    def _rebalance_when_insert_to_left(self, node: AvlNode):
        return self._rebalance_left(node)

    def _rebalance_when_insert_to_right(self, node: AvlNode):
        return self._rebalance_right(node)

    def _upsert(
            self, node: AvlNode, key, data=None, disable_update: bool = False):
        if node is None:
            self._changes_needed = True
            return AvlNode(key, data)
        elif key < node.key:
            node.left = self._upsert(node.left, key, data, disable_update)
            return self._rebalance_when_insert_to_left(node)
        elif key > node.key:
            node.right = self._upsert(node.right, key, data, disable_update)
            return self._rebalance_when_insert_to_right(node)
        else:
            if disable_update:
                raise AvlTreeDuplicatedKeyFoundException()
            self._changes_needed = False
            node.data = data
            return node

    def upsert(self, key, data=None):
        """ ノードがあれば更新、なければ、加える。 """
        self._root = self._upsert(self._root, key, data)

    def insert(self, key, data=None):
        """ ノードを加える。 """
        self._root = self._upsert(self._root, key, data, disable_update=True)

    def _rebalance_when_delete_from_left(self, node: AvlNode):
        return self._rebalance_right(node)

    def _rebalance_when_delete_from_right(self, node: AvlNode):
        return self._rebalance_left(node)

    def _delete_max(self, node):
        if node.right is None:
            # このノードのキーが最大である。

            # 最大のキーとデータを更新する。
            self._changes_needed = True
            self._max_left_key = node.key
            self._max_left_data = node.data

            # 削除後のサブツリーを返すことで、このノードを消す。
            return node.left
        else:
            node.right = self._delete_max(node.right)
            return self._rebalance_when_delete_from_right(node)

    def _delete(self, node: AvlNode, key):
        if node is None:
            self._changes_needed = False
            return None
        elif key < node.key:
            node.left = self._delete(node.left, key)
            return self._rebalance_when_delete_from_left(node)
        elif key > node.key:
            node.right = self._delete(node.right, key)
            return self._rebalance_when_delete_from_right(node)
        else:
            if node.left is None:
                self._changes_needed = True
                return node.right
            else:
                node.left = self._delete_max(node.left)
                node.key = self._max_left_key
                node.data = self._max_left_data
                return self._rebalance_when_delete_from_left(node)

    def delete(self, key):
        self._root = self._delete(self._root, key)

    def _find_node(self, key, node: AvlNode):
        if key < node.key:
            if node.left is None:
                return None
            return self._find_node(key, node.left)
        elif key > node.key:
            if node.right is None:
                return None
            return self._find_node(key, node.right)
        else:
            return node

    def find_node(self, key) -> AvlNode:
        """ ノードを探す。 """
        if self._root is None:
            return None
        return self._find_node(key, self._root)

    def _is_balanced(self, node: AvlNode):
        if node.left is not None:
            if not self._is_balanced(node.left):
                return False
        if not node.is_balanced():
            return False
        if node.right is not None:
            if not self._is_balanced(node.right):
                return False
        return True

    def is_balanced(self) -> bool:
        """ AVL木が平衡であるか確認する。 """
        if self._root is None:
            return True
        return self._is_balanced(self._root)

    def _get_list(
            self, node: AvlNode, repr_print_none: bool = False,
            repr_print_object: bool = False):
        repr_list = []

        if node is None:
            return None

        if node.left is not None or repr_print_none:
            repr_list.append(self._get_list(
                node.left, repr_print_none=repr_print_none,
                repr_print_object=repr_print_object))

        if repr_print_object:
            repr_list.append(str(node))
        else:
            repr_list.append(node.key)

        if node.right is not None or repr_print_none:
            repr_list.append(self._get_list(
                node.right, repr_print_none=repr_print_none,
                repr_print_object=repr_print_object))

        return repr_list

    def get_list(
            self, repr_print_none: bool = False,
            repr_print_object: bool = False) -> list:
        """ グラフを表現するリストを得る。 """
        return self._get_list(
                self._root, repr_print_none=repr_print_none,
                repr_print_object=repr_print_object)

    def _print(self, repr_list: list, depth: int = 0):
        if len(repr_list) != 3:
            raise AvlTreeException()

        index_label_dic = {0: "left ", 1: "value", 2: "right"}

        indent = " " * depth
        for index, elem in enumerate(repr_list):
            indent_label = indent + index_label_dic[index] + ": "
            if isinstance(elem, list):
                print(indent_label)
                self._print(elem, depth+1)
            elif isinstance(elem, str) or \
                    isinstance(elem, int) or \
                    elem is None:
                print(indent_label + str(elem))
            else:
                raise AvlTreeException()

    def print(self, repr_print_object: bool = False):
        """ グラフを出力する。 """
        repr_list = self._get_list(
                self._root, repr_print_none=True,
                repr_print_object=repr_print_object)
        self._print(repr_list)

    def __repr__(self):
        return "<AvlTree " + str(self._get_list(self._root)) + ">"


if __name__ == '__main__':
    pass
