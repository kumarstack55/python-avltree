from avltree import AvlTree
from avltree import AvlTreeDuplicatedKeyFoundException
import pytest
import random


def test_init():
    tree = AvlTree()
    assert tree


def test_insert():
    """ キーを1件挿入する。 """
    tree = AvlTree()
    tree.insert(10)
    assert tree.get_list() == [10]


def test_inserting_dup_key_raises_exception():
    """ 重複したキーを挿入すると例外を発生する。 """
    tree = AvlTree()
    tree.insert(10, data={"a": 1})
    with pytest.raises(AvlTreeDuplicatedKeyFoundException):
        tree.insert(10, data={"a": 2})


def test_upserting_dup_key_raises_exception():
    """ 重複したキーをupsertすると例外を発生しない。 """
    tree = AvlTree()
    tree.insert(10, data={"a": 1})
    tree.upsert(10, data={"a": 2})
    assert tree.find_node(10).data["a"] == 2


def test_insert_right():
    """ 右に挿入する。 """
    tree = AvlTree()
    tree.insert(10)
    tree.insert(20)
    assert tree.get_list() == [10, [20]]


def test_insert_left():
    """ 左に挿入する。 """
    tree = AvlTree()
    tree.insert(20)
    tree.insert(10)
    assert tree.get_list() == [[10], 20]


def test_insert_root_left_left():
    """ root, 左, 左の順で挿入する。 """
    tree = AvlTree()
    tree.insert(30)
    tree.insert(20)
    tree.insert(10)
    assert tree.get_list() == [[10], 20, [30]]


def test_insert_root_left_right():
    """ root, 左, 右の順で挿入する。 """
    tree = AvlTree()
    tree.insert(20)
    tree.insert(10)
    tree.insert(30)
    assert tree.get_list() == [[10], 20, [30]]


def test_insert_root_right_left():
    """ root, 右, 左の順で挿入する。 """
    tree = AvlTree()
    tree.insert(10)
    tree.insert(30)
    tree.insert(20)
    assert tree.get_list() == [[10], 20, [30]]


def test_insert_root_right_right():
    """ root, 右, 右の順で挿入する。 """
    tree = AvlTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    assert tree.get_list() == [[10], 20, [30]]


def test_insert_random():
    """ ランダムに挿入しても平衡木であることを確かめる。 """
    N = 100000
    keys = list(range(N))
    random.shuffle(keys)
    tree = AvlTree()
    for key in keys:
        tree.insert(key)
    assert tree.is_balanced()


def test_insert_random_find():
    """ ランダムに挿入した平衡木からノードを探索する。 """
    N = 100000
    keys = list(range(N))
    random.shuffle(keys)
    tree = AvlTree()
    for key in keys:
        tree.insert(key)
    assert tree.find_node(keys[0]) is not None


def test_insert_random_strings():
    """ キーとして文字列を挿入する。 """
    keys = list("abcdefghijklmnopqrstuvwxyz")
    random.shuffle(keys)
    tree = AvlTree()
    for key in keys:
        tree.insert(key)
    assert tree.is_balanced()


def test_there_is_no_nodes_get_list_returns_none():
    tree = AvlTree()
    assert tree.get_list() is None


def test_delete():
    """ ノードを消す。 """
    tree = AvlTree()
    tree.insert(10)
    tree.delete(10)
    assert tree.get_list() is None


def test_insert_random_and_delete():
    """ ランダムに挿入した平衡木からノードを消す。 """
    N = 100000
    keys = list(range(N))
    random.shuffle(keys)
    tree = AvlTree()
    for key in keys:
        tree.insert(key)
    for key in keys[:N//10]:
        tree.delete(key)
    assert tree.is_balanced()
