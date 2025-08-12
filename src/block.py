import enum
from htmlnode import HTMLNode, ParentNode, markdown_to_blocks, text_node_to_html_node, text_to_textnodes
from textnode import TextNode, TextType

class BlockType(enum.Enum):
    PARAGRAPH= "paragraph"
    HEADING = "heading"
    CODE="code"
    QUOTE="quote"
    UNORDERED_LIST="unordered_list"
    ORDERED_LIST="ordered_list"

def block_to_block_type(markdown):
    lines = markdown.split("\n")
    n =0 
    while n < len(lines[0]) and lines[0][n] == "#" :
        n += 1
    
    if markdown.startswith(("#" * n) + " ") and n <= 6 and n != 0:
        return BlockType.HEADING
    
    if lines[0].strip().startswith("```") and lines[-1].strip().startswith("```"):
        return BlockType.CODE
    
    q_count= 0
    u_count= 0
    o_count= 0
    num= 1
    for i in lines:
        if len(i) > 0 and i[0] == ">":
            q_count += 1
        if len(i) >= 2 and i[0:2] == "- ":
            u_count += 1
        if len(i) >= len(f"{num}. ") and f"{num}. " == i[0:len(f"{num}. ")]:
            o_count += 1
        num += 1

    if q_count == len(lines):
        return BlockType.QUOTE
    if u_count == len(lines):
        return BlockType.UNORDERED_LIST
    if o_count == num -1:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    all_nodes = []
    for b in blocks:
        if not b.strip():
            continue
        type = block_to_block_type(b)
        if type == BlockType.QUOTE:
            sp = b.split("\n")
            for i in range(len(sp)):
                sp[i] = sp[i][2:]
            b= "\n".join(sp)
            all_nodes.append(ParentNode("blockquote", text_to_children(b)))
        elif type == BlockType.UNORDERED_LIST:
            all_nodes.append(ParentNode("ul", list_element(b)))
        elif type == BlockType.ORDERED_LIST:
            all_nodes.append(ParentNode("ol",list_element(b)))
        elif type == BlockType.PARAGRAPH:
            pt = " ".join(b.split())
            all_nodes.append(ParentNode("p",text_to_children(pt) ))
        elif type == BlockType.HEADING:
            n =0 
            while n < len(b) and b[n] == "#" :
                n += 1

            all_nodes.append(ParentNode(f"h{n}", text_to_children(b[n:].strip())))
        elif type == BlockType.CODE:
            sp =b.split("\n")
            sp = sp[1:-1]
            sp = [line.lstrip() for line in sp]
            b="\n".join(sp) + "\n"

            cn = TextNode(b,TextType.TEXT)
            code_tag_node = ParentNode("code",[text_node_to_html_node(cn)])
            all_nodes.append(ParentNode("pre", [code_tag_node]))
    return ParentNode("div", all_nodes)
        
def text_to_children(text):
    ret =[]
    text = text_to_textnodes(text)
    for t in text:
        ret.append(text_node_to_html_node(t))
    return ret

def list_element(b):
    lines = b.split("\n")
    ret=[]
    for i in lines:
        new= i.split(" ",1)
        ret.append(ParentNode("li", text_to_children(new[1])))
    return ret

def extract_title(markdown):
    sp = markdown.split("\n")
    for i in sp:
        if i.startswith("# "):
            return i[2:].strip()
    raise Exception("Error: no heading")