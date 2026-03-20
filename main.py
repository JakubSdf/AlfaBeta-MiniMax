import math
from graphviz import Digraph

structure_seq = [4, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, -1, 2, 1, 2, 2, -1, 3, -1, 1, 3, 3, 2, 3, 3, 1, 4, 3, 3, -1, 2, 2, 1, 2]
# Modify this array according to your assignment:
terminals_seq = [math.inf, 0, -math.inf, 0, -12, -4, 11, -1, 4, 2, -6, -4, 10, -3, math.inf, -11, -6, -5, -4, 6, -9, 5, 1, -6, -5, 5, -3, 0, -9, -9, 1, 3, 4, 7, 10, -6, 12, -3, 4, 2]

class Node:
    def __init__(self, id, is_max):
        self.id = id
        self.is_max = is_max
        self.children = []
        self.value = None 
        self.minimax_value = None
        self.alpha_history = []
        self.beta_history = []
        self.pruned = False
        self.is_terminal = False

def build_tree():
    root = Node("root", True)
    levels = [[root]]
    struct_idx = 0
    term_idx = 0

    for depth in range(5):
        next_level = []
        for node in levels[depth]:
            b = structure_seq[struct_idx] if struct_idx < len(structure_seq) else -1
            struct_idx += 1

            if b == -1:
                node.is_terminal = True
                node.value = terminals_seq[term_idx]
                term_idx += 1
            else:
                for i in range(b):
                    child = Node(f"{node.id}_{i}", not node.is_max)
                    node.children.append(child)
                    next_level.append(child)
        levels.append(next_level)

    for node in levels[5]:
        node.is_terminal = True
        node.value = terminals_seq[term_idx]
        term_idx += 1
        
    return root

def minimax(node, is_max):
    if node.is_terminal:
        node.minimax_value = node.value
        return node.value

    if is_max:
        best = -math.inf
        for child in node.children:
            val = minimax(child, False)
            if val > best:
                best = val
        node.minimax_value = best
        return best
    else:
        best = math.inf
        for child in node.children:
            val = minimax(child, True)
            if val < best:
                best = val
        node.minimax_value = best
        return best

def mark_pruned(node):
    node.pruned = True
    for child in node.children:
        mark_pruned(child)

def alphabeta(node, alpha, beta, is_max):
    node.alpha_history = [alpha]
    node.beta_history = [beta]

    if node.is_terminal:
        return node.value

    if is_max:
        for child in node.children:
            if child.pruned: continue
            
            temp = alphabeta(child, alpha, beta, False)
            if temp > alpha:
                alpha = temp
                node.alpha_history.append(alpha)
                
            if alpha >= beta:
                prune_start = node.children.index(child) + 1
                for c in node.children[prune_start:]:
                    mark_pruned(c)
                break
                
        return alpha
        
    else:
        for child in node.children:
            if child.pruned: continue
            
            temp = alphabeta(child, alpha, beta, True)
            if temp < beta:
                beta = temp
                node.beta_history.append(beta)
                
            if alpha >= beta:
                prune_start = node.children.index(child) + 1
                for c in node.children[prune_start:]:
                    mark_pruned(c)
                break
                
        return beta

def format_inf(val):
    if val == math.inf: return 'inf'
    if val == -math.inf: return '-inf'
    return str(val)

def generate_graph(root):
    dot = Digraph(comment='AlphaBeta Tree', format='png')
    dot.attr(rankdir='TB', nodesep='0.3', ranksep='0.6')
    dot.attr(dpi='600')
    
    def traverse(node):
        val_str = format_inf(node.minimax_value) if node.minimax_value is not None else ""
        
        if not node.is_terminal:
            a_str = ", ".join(format_inf(x) for x in node.alpha_history)
            b_str = ", ".join(format_inf(x) for x in node.beta_history)
            
            label = f'''<<TABLE BORDER="0" CELLPADDING="1">
            <TR><TD ALIGN="left"><FONT COLOR="red" POINT-SIZE="10">a = {a_str}<BR/>b = {b_str}</FONT></TD></TR>
            <TR><TD BORDER="1" ALIGN="center" WIDTH="25" HEIGHT="25" BGCOLOR="white">{val_str}</TD></TR>
            </TABLE>>'''
            dot.node(node.id, label=label, shape='none')
        else:
            color = "gray" if node.pruned else "black"
            fontcolor = "gray" if node.pruned else "black"
            label = f'''<<TABLE BORDER="0" CELLPADDING="1">
            <TR><TD BORDER="1" ALIGN="center" WIDTH="25" HEIGHT="25" COLOR="{color}"><FONT COLOR="{fontcolor}">{val_str}</FONT></TD></TR>
            </TABLE>>'''
            dot.node(node.id, label=label, shape='none')

        for child in node.children:
            traverse(child)
            edge_color = "red" if child.pruned else "black"
            edge_style = "dashed" if child.pruned else "solid"
            dot.edge(node.id, child.id, color=edge_color, style=edge_style)

    traverse(root)
    dot.render('result', view=False)
    print("result.png has been generated.")

tree = build_tree()

minimax(tree, True)
alphabeta(tree, -math.inf, math.inf, True)
generate_graph(tree)