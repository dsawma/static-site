import re
from textnode import TextNode, TextType

class HTMLNode():
    def __init__(self, tag= None, value = None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        else:
            str = f''
            for key, value in self.props.items():
                str += f' {key}="{value}"'

            return str 
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag,value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError()
        if self.tag is None:
            return f"{self.value}"
        elif self.props is not None:
            return f"<{self.tag}>{self.props_to_html()}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props= None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError()
        if self.children is None:
            raise ValueError()
        html = ""
        for child in self.children:
            html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{html}</{self.tag}>"

def text_node_to_html_node(text_node):
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        if text_node.text_type == TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        if text_node.text_type == TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        if text_node.text_type == TextType.CODE:
            return LeafNode("code", text_node.text, None)
        if text_node.text_type == TextType.LINKS:
            return ParentNode("a", [LeafNode(None, text_node.text)],{"href": text_node.url})
        if text_node.text_type == TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url,"alt": text_node.text})
        else:
            raise Exception()
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    ret = []
    for i in old_nodes:
        if i.text_type == TextType.TEXT:
            split = i.text.split(delimiter)
            if len(split) % 2 == 0:
                raise Exception()
            for j in range(len(split)):
                if j % 2 == 0:
                    if split[j] != "":
                        ret.append(TextNode(split[j], TextType.TEXT))
                else:
                     if split[j] != "":
                        ret.append(TextNode(split[j], text_type))
        else:
            ret.append(TextNode(i.text, i.text_type))

    return ret

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_images(old_nodes):
    ret = []
    for i in old_nodes:
        if i.text_type == TextType.TEXT:
            remaining = i.text
            extract = extract_markdown_images(remaining)
            for img,link in extract:
                parts = remaining.split(f"![{img}]({link})",1)
                if parts[0] != "":
                    ret.append(TextNode(parts[0], TextType.TEXT))
                ret.append(TextNode(img,TextType.IMAGE, link))
                remaining= parts[1]
            if remaining != "":
                ret.append(TextNode(remaining, TextType.TEXT))
        else:
            ret.append(i)
        
    return ret


def split_nodes_link(old_nodes):
    ret = []
    for i in old_nodes:
        if i.text_type == TextType.TEXT:
            remaining = i.text
            extract = extract_markdown_links(i.text)
            for alt,link in extract:
            
                parts = remaining.split(f"[{alt}]({link})",1)
               
                if parts[0] != "":
                    ret.append(TextNode(parts[0], TextType.TEXT))
                ret.append(TextNode(alt,TextType.LINKS, link))
                
                remaining= parts[1]
            if remaining != "":
                ret.append(TextNode(remaining, TextType.TEXT))
        else:
            ret.append(i)
    return ret
                
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def markdown_to_blocks(markdown):
    list = markdown.split("\n\n")
    filtered = []
    for i in list:
        if i != "":
            block = i.strip()
            filtered.append(block)
    return filtered 

    


        