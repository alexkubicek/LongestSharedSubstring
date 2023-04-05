import sys


def trie_construction(Patterns):
    root = TrieNode("", 0)
    for pattern in Patterns:
        current_node = root
        for c in pattern:
            if c not in current_node.children.keys():
                current_node.children[c] = TrieNode(c, 1)
            current_node = current_node.children.get(c)
        current_node.children['$'] = TrieNode('$', 1)
    return root


def add_second_string_to_tree(other_suffixes, cur_suffix_tree):
    root = cur_suffix_tree
    for pattern in other_suffixes:
        current_node = root
        for c in pattern:
            if c not in current_node.children.keys():
                current_node.children[c] = TrieNode(c, 2)
            current_node = current_node.children.get(c)
            if current_node.string_source == 1:
                current_node.string_source = 0
        current_node.children['$'] = TrieNode('$', 2)
    return root


# class from github
class TrieNode:
    """A node in the trie structure"""

    def __init__(self, char, ss):
        # the character stored in this node
        self.char = char

        # a dictionary of child nodes
        # keys are characters, values are nodes
        self.children = {}

        self.string_source = ss

    def print(self):
        print(self.char)
        for n in self.children.values():
            n.print()


def get_suffixes(text):
    suffixes = []
    while len(text) > 0:
        suffixes.append(text)
        text = text[1:]
    return suffixes


def condense_tree(tree):
    for child_key in tree.children.keys():
        condense_tree(tree.children[child_key])
    if len(tree.children) == 1:
        key = ''
        for k in tree.children.keys():
            key = k
        child = tree.children[key]
        if tree.string_source != child.string_source:
            return
        tree.char += child.char
        tree.children = child.children


def get_longest_shared_sub(tree_to_search, longest_found):
    if tree_to_search.string_source > 0:
        return str()
    longest_in_node = str()
    for key in tree_to_search.children.keys():
        each_node = tree_to_search.children[key]
        # print(each_node.char)
        cur_longest = get_longest_shared_sub(each_node, longest_found)
        if each_node.string_source == 0:
            cur_longest = each_node.char + cur_longest
        if len(cur_longest) > len(longest_in_node):
            # print("replaced " + longest_found + " with " + cur_longest)
            longest_in_node = cur_longest
    if len(longest_in_node) > len(longest_found):
        longest_found = longest_in_node
    if tree_to_search.char == '':
        return longest_found
    return longest_in_node


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    filePath = input()
    inFile = open(filePath)
    input_text = []
    for line in inFile:
        if line.endswith("\n"):
            line = line[0:(len(line) - 1)]
        input_text.append(line)
    inFile.close()

    patterns = get_suffixes(input_text[0])
    trie = trie_construction(patterns)
    patterns = get_suffixes(input_text[1])
    trie = add_second_string_to_tree(patterns, trie)
    sys.setrecursionlimit(len(patterns) * len(input_text))
    condense_tree(trie)
    # trie.print()
    f = open("output.txt", 'w')
    sys.stdout = f
    print(get_longest_shared_sub(trie, ''))
    f.close()
