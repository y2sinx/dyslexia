import os

ROOT = "F:\\Git\\" if os.path.exists("F:\\Git\\") else "Y:\\Git\\"  ##PC1,PC2

def get_needed_path(root=ROOT, extensions=[".ht", ".txt"]):
    """构建文件名-文件路径字典.
    便于后面的子模块引用常用的文件("dt_words.pkl", "dt_phrase.pkl")"""
    out = {}
    for root, _, files in os.walk(root):
        for file in files:
            path = os.path.join(root, file)
            _, ext = os.path.splitext(path)
            if ext in extensions:
                out[file] = path
    return out
NEEDED_PATH = get_needed_path(ROOT)
