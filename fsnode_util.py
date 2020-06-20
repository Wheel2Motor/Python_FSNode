# -*- coding: utf-8 -*-
"""
2020年6月15日.

@author: 李伟
@mail: 1462965949@qq.com

该脚本运行在Python3上

核心标准库：os, sys, string, random, time
非核心标注库：tkinter
第三方库：pillow
自开发库：fsnode

"""

import os
import sys

# 使用到的标准库
from os import makedirs
from os.path import join
from os.path import abspath
from os.path import exists
from random import randint
from random import choice
from string import ascii_letters as letters
from time import time


# 不写入__pycache__
sys.dont_write_bytecode = True


# 必须运行于Python3之上
if sys.version_info.major < 3:
    print("该脚本运行于Python3之上， 退出...")
    sys.exit()


# tkinter图形库，Python3自带
try:
    import tkinter as tk
    from tkinter.filedialog import askdirectory
    from tkinter.filedialog import askopenfilename
except Exception:
    print("tkinter缺失，退出...")
    sys.exit()


# pillow生成GIF
try:
    from PIL import Image
except Exception:
    print("缺失pillow，pip尝试从豆瓣镜像安装...")
    os.system("pip install pillow -i https://pypi.douban.com/simple")
    try:
        from PIL import Image
    except Exception:
        print("缺失pillow，pip尝试从官方镜像安装...")
        os.system("pip install pillow")
        try:
            from PIL import Image
        except Exception:
            print("缺失pillow，pip3尝试从豆瓣镜像安装...")
            os.system("pip3 install pillow  -i https://pypi.douban.com/simple")
            try:
                from PIL import Image
            except Exception:
                print("缺失pillow，pip3尝试从官方镜像安装...")
                os.system("pip3 install pillow")
                try:
                    from PIL import Image
                except Exception:
                    print("pillow安装失败，退出...")
                    sys.exit()


# FSNode模块
try:
    from fsnode import FSNode
except Exception:
    print("fsnode缺失，退出...")
    sys.exit()


# UI行数自动计数器
class AutoCounter():
    """自动计数器."""

    def __init__(self, start=0, step=1):
        assert isinstance(start, int)
        assert isinstance(step, int)
        self.__counter = start
        self.__step = step

    def __call__(self):
        """每次调用，自动计算计数器步进."""
        self.__counter += self.__step
        return self.__counter - self.__step

    @property
    def counter(self):
        """只读计数器当前值."""
        return self.__counter

    @property
    def step(self):
        """步长."""
        return self.__step

    @property
    def last(self):
        """上一步的值."""
        return self.counter - self.step


# 遍历所有可生成GIF的文件节点
class GifFSNode(FSNode):
    """自动生成GIF节点，继承自FSNode."""

    def __init__(
            self,
            dirname=".",
            suffix="",
            parent=None,
            level=0,
            sort=True,
            *argv,
            **kargv):
        super().__init__(
            dirname=dirname,
            suffix=suffix,
            parent=parent,
            level=level,
            sort=sort
            )

    def save_gif(self, fps=24, log=False, warning=True):
        """在序列帧上级目录保存GIF."""
        for i in self.subnode:
            i.save_gif(fps=fps, log=log, warning=warning)
        frames = [Image.open(i) for i in self.abs_content]
        if frames:
            try:
                fullname = self.abs_dirname + ".gif"
                frames[0].save(
                    fullname,
                    save_all=True,
                    append_images=frames,
                    duration=1.0/fps
                    )
                if log:
                    print("Saved".ljust(20, "-"), fullname)
            except Exception as e:
                if warning:
                    print(e)


if __name__ == "__main__":

    debug = True
    debug_std = True

    root = tk.Tk()
    root.title("FSNode")
    counter = AutoCounter()
    width = 50
    delimiter = "- "
    suffix_str_var = tk.StringVar()

    """
    UI FUNC
    """
    def gen_garbage():
        """生成一堆垃圾文件."""
        start_time = 0
        dirname = askdirectory(title="选择根目录")
        if dirname:
            start_time = time()
            try:
                dirname = join(dirname, "garbage")
                for i in range(randint(1, 10)):
                    dirname = join(dirname, "".join(
                        [choice(letters) for j in range(randint(1, 10))]
                        ))
                    if not exists(dirname):
                        try:
                            makedirs(dirname)
                        except Exception as err_makedirs:
                            print(err_makedirs)
                    for j in range(randint(0, 100)):
                        basename = "".join([
                            choice(letters) for l in range(randint(1, 10))
                                 ])
                        if not suffix_str_var.get():
                            basename += choice([
                                ".test1",
                                ".test2",
                                ".test3",
                                ".test4",
                                ".test5",
                                ".test6"
                                ])
                        else:
                            basename += suffix_str_var.get()
                        full_name = join(dirname, basename)
                        if not exists(full_name):
                            try:
                                open(full_name, "w").close()
                                print("Created".ljust(20, "-"), full_name)
                            except Exception as err_openfile:
                                print(err_openfile)
            except Exception as e:
                print(e)
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def cmp_node():
        """比较节点是否相同."""
        start_time = 0
        path1 = askdirectory(title="选择根目录")
        if path1:
            path2 = askdirectory(title="选择根目录")
            if path2:
                start_time = time()
                node1 = FSNode(path1, suffix="*")
                node2 = FSNode(path2, suffix="*")
                print("相同" if FSNode.equal(node1, node2) else "不同")
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def parse_super_dir():
        """推导上一个目录."""
        start_time = 0
        path = askdirectory(title="选择根目录")
        if path:
            start_time = time()
            path = os.path.abspath(path)
            result = FSNode.parse_super_dir(path)
            print("Parsed".ljust(20, "-"), path)
            print("To".ljust(20, "-"), result)
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def parse_super_dir_s():
        """推导上一个目录，安全版本."""
        start_time = 0
        path = askdirectory(title="选择根目录")
        if path:
            start_time = time()
            path = os.path.abspath(path)
            result = FSNode.parse_super_dir_s(path)
            print("Parsed".ljust(20, "-"), path)
            print("To".ljust(20, "-"), result)
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def parse_super_name():
        """推导上一个目录."""
        start_time = 0
        path = askopenfilename(title="选择根目录")
        if path:
            start_time = time()
            path = os.path.abspath(path)
            result = FSNode.parse_super_name(path)
            print("Parsed".ljust(20, "-"), path)
            print("To".ljust(20, "-"), result)
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def parse_super_name_s():
        """推导上一个目录，安全版本."""
        start_time = 0
        path = askopenfilename(title="选择根目录")
        if path:
            start_time = time()
            path = os.path.abspath(path)
            result = FSNode.parse_super_name_s(path)
            print("Parsed".ljust(20, "-"), path)
            print("To".ljust(20, "-"), result)
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def gen_gif():
        """生成GIF."""
        start_time = 0
        if suffix_str_var.get():
            dirname = askdirectory(title="选择根目录")
            if dirname:
                start_time = time()
                node = GifFSNode(
                    dirname=dirname,
                    suffix=suffix_str_var.get(),
                    sort=True
                    )
                node.save_gif(log=True)
            end_time = time()
            print("DONE:{0}s".format(end_time-start_time))
        else:
            print("请输入序列帧后缀名")

    """
    UI FUNC
    """
    def gen_gif_std():
        """STD生成GIF."""
        start_time = 0
        if suffix_str_var.get():
            dirname = askdirectory(title="选择根目录")
            if dirname:
                start_time = time()
                for root, dirs, files in os.walk(dirname):
                    suffix = suffix_str_var.get()
                    frames = [Image.open(join(root, i))
                              for i in files if i.endswith(suffix)]
                    if frames:
                        dirname = abspath(join(root, "../"))
                        basename = root+".gif"
                        fullname = join(dirname, basename)
                        frames[0].save(
                            fullname,
                            save_all=True,
                            append_images=frames,
                            duration=24/1.0)
                        print("Saved".ljust(20, "-"), fullname)
            end_time = time()
            print("DONE:{0}s".format(end_time-start_time))
        else:
            print("请输入序列帧后缀名")

    """
    UI FUNC
    """
    def log_nodeinfo():
        """打印节点信息."""
        start_time = 0
        dirname = askdirectory(title="选择根目录")
        if dirname:
            start_time = time()
            node = FSNode(dirname=dirname, suffix=suffix_str_var.get())
            print(node)
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def log_treeinfo():
        """打印节点树信息."""
        start_time = 0
        dirname = askdirectory(title="选择根目录")
        if dirname:
            start_time = time()
            node = FSNode(dirname=dirname, suffix=suffix_str_var.get())
            treeinfo = node.get_traversal_treeinfo()
            print(treeinfo)
            output = open("output.txt", "w", encoding="utf-8")
            output.write(treeinfo)
            output.close()
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def get_files():
        """获取指定类型文件."""
        start_time = 0
        dirname = askdirectory(title="选择根目录")
        if dirname:
            start_time = time()
            node = FSNode(dirname=dirname, suffix=suffix_str_var.get())
            content = node.get_traversal_content()
            for i in content:
                print(i)
            print(len(content))
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def get_files_std():
        """STD获取指定类型文件."""
        start_time = 0
        dirname = askdirectory(title="选择根目录")
        if dirname:
            start_time = time()
            all_files = set()
            for root, dirs, files in os.walk(dirname):
                for f in files:
                    if not f.endswith(suffix_str_var.get()):
                        continue
                    file_name = join(root, f)
                    all_files.add(file_name)
                    print(file_name)
        print(len(all_files))
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def get_folders():
        """获取指所有文件夹."""
        start_time = 0
        dirname = askdirectory(title="选择根目录")
        if dirname:
            start_time = time()
            node = FSNode(dirname=dirname)
            subnode = node.get_traversal_nodes()
            for i in subnode:
                print(i.abs_dirname)
            print(len(subnode))
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def get_folders_std():
        """STD获取指所有文件夹."""
        start_time = 0
        dirname = askdirectory(title="选择根目录")
        if dirname:
            start_time = time()
            folders = set()
            for root, dirs, files in os.walk(dirname):
                folders.add(root)
                for d in dirs:
                    fullname = abspath(join(root, d))
                    folders.add(fullname)
                    print(fullname)
            print(len(folders))
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def del_files():
        """删除指定类型文件."""
        start_time = 0
        dirname = askdirectory(title="选择根目录")
        if dirname:
            start_time = time()
            node = FSNode(dirname=dirname, suffix=suffix_str_var.get())
            count = len(node.get_traversal_content())
            node.remove_traversal_content(log=True)
            print(count)
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def del_files_std():
        """STD删除指定类型文件."""
        start_time = 0
        dirname = askdirectory(title="选择根目录")
        if dirname:
            start_time = time()
            content = set()
            for root, dirs, files in os.walk(dirname):
                for f in files:
                    if f.endswith(suffix_str_var.get()):
                        fullname = abspath(join(root, f))
                        content.add(fullname)
                        print(fullname)
            print(len(content))
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def del_empty_folder():
        """递归删除空文件夹."""
        start_time = 0
        dirname = askdirectory(title="选择根目录")
        if dirname:
            start_time = time()
            node = FSNode(dirname=dirname, suffix="*")
            node.remove_empty_folders(log=True)
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def del_empty_content_folder():
        """递归删除没有指定类型文件的文件夹."""
        start_time = 0
        dirname = askdirectory(title="选择根目录")
        if dirname:
            start_time = time()
            node = FSNode(dirname=dirname, suffix=suffix_str_var.get())
            node.remove_empty_content_folders(log=True)
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def del_with_content_folder():
        """递归删除包含指定类型文件的文件夹."""
        start_time = 0
        dirname = askdirectory(title="选择根目录")
        if dirname:
            start_time = time()
            node = FSNode(dirname=dirname, suffix=suffix_str_var.get())
            node.remove_with_content_folders(log=True)
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def rebuild_empty_tree():
        """重建空文件夹树."""
        start_time = 0
        src_dirname = askdirectory(title="选择源目录")
        if src_dirname:
            dst_dirname = askdirectory(title="选择目标目录")
            if dst_dirname:
                start_time = time()
                node = FSNode(dirname=src_dirname, suffix="*")
                node.rebuild_dirs_tree(
                    parent_dirname=dst_dirname,
                    log=True)
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    UI FUNC
    """
    def rebuild_content_tree():
        """重建文件夹树拷贝指定类型文件."""
        start_time = 0
        src_dirname = askdirectory(title="选择源目录")
        if src_dirname:
            dst_dirname = askdirectory(title="选择目标目录")
            if dst_dirname:
                start_time = time()
                node = FSNode(
                    dirname=src_dirname,
                    suffix=suffix_str_var.get())
                node.rebuild_dirs_tree(
                    parent_dirname=dst_dirname,
                    log=True,
                    copy_file=True)
        end_time = time()
        print("DONE:{0}s".format(end_time-start_time))

    """
    ----------------------------------------------------------------------
    """
    tk.Label(
        master=root,
        text=delimiter*width
        ).grid(row=counter(), column=0)
    if debug_std:
        tk.Label(
            master=root,
            text=delimiter*width
            ).grid(row=counter.last, column=1)

    """
    名称后缀输入框
    """
    entry = tk.Entry(
        master=root,
        textvariable=suffix_str_var,
        width=width,
        background="#DDFFFF",
        foreground="#000000")
    entry.grid(row=counter(), column=0)

    if debug_std:
        tk.Label(
            master=root,
            text="标准库实现",
            width=width
            ).grid(row=counter.last, column=1)

    """
    ----------------------------------------------------------------------
    """
    tk.Label(
        master=root,
        text=delimiter*width
        ).grid(row=counter(), column=0)
    if debug_std:
        tk.Label(
            master=root,
            text=delimiter*width
            ).grid(row=counter.last, column=1)

    if debug:
        tk.Button(
            master=root,
            text="生成一堆垃圾文件",
            width=width,
            command=gen_garbage,
            ).grid(row=counter(), column=0)

    if debug:
        tk.Button(
            master=root,
            text="比较两个文件夹节点",
            width=width,
            command=cmp_node,
            ).grid(row=counter(), column=0)

    if debug:
        tk.Button(
            master=root,
            text="推导上级目录",
            width=width,
            command=parse_super_dir,
            ).grid(row=counter(), column=0)

    if debug:
        tk.Button(
            master=root,
            text="推导上级目录 确保上级目录存在",
            width=width,
            command=parse_super_dir_s,
            ).grid(row=counter(), column=0)

    if debug:
        tk.Button(
            master=root,
            text="推导上级名称",
            width=width,
            command=parse_super_name,
            ).grid(row=counter(), column=0)

    if debug:
        tk.Button(
            master=root,
            text="推导上级名称 确保上级目录存在",
            width=width,
            command=parse_super_name_s,
            ).grid(row=counter(), column=0)

    """
    ----------------------------------------------------------------------
    """
    if debug:
        tk.Label(
            master=root,
            text=delimiter*width
            ).grid(row=counter(), column=0)
        if debug_std:
            tk.Label(
                master=root,
                text=delimiter*width
                ).grid(row=counter.last, column=1)

    tk.Button(
        master=root,
        text="根据指定序列帧后缀名递归生成GIF于序列帧上级目录",
        width=width,
        command=gen_gif,
        ).grid(row=counter(), column=0)

    if debug_std:
        tk.Button(
            master=root,
            text="STD根据指定序列帧后缀名递归生成GIF于序列帧上级目录",
            width=width,
            command=gen_gif_std,
            ).grid(row=counter.last, column=1)

    """
    ----------------------------------------------------------------------
    """
    tk.Label(
        master=root,
        text=delimiter*width
        ).grid(row=counter(), column=0)
    if debug_std:
        tk.Label(
            master=root,
            text=delimiter*width
            ).grid(row=counter.last, column=1)

    tk.Button(
        master=root,
        text="打印文件夹节点信息",
        width=width,
        command=log_nodeinfo,
        ).grid(row=counter(), column=0)

    tk.Button(
        master=root,
        text="递归打印指定类型文件树",
        width=width,
        command=log_treeinfo,
        ).grid(row=counter(), column=0)

    tk.Button(
        master=root,
        text="递归获取指定类型文件",
        width=width,
        command=get_files
        ).grid(row=counter(), column=0)

    if debug_std:
        tk.Button(
            master=root,
            text="STD递归获取指定类型文件",
            width=width,
            command=get_files_std
            ).grid(row=counter.last, column=1)

    tk.Button(
        master=root,
        text="递归获取所有文件夹",
        width=width,
        command=get_folders
        ).grid(row=counter(), column=0)

    if debug_std:
        tk.Button(
            master=root,
            text="STD递归获取所有文件夹",
            width=width,
            command=get_folders_std
            ).grid(row=counter.last, column=1)

    """
    ----------------------------------------------------------------------
    """
    tk.Label(
        master=root,
        text=delimiter*width
        ).grid(row=counter(), column=0)
    if debug_std:
        tk.Label(
            master=root,
            text=delimiter*width
            ).grid(row=counter.last, column=1)

    tk.Button(
        master=root,
        text="递归删除指定类型文件",
        width=width,
        command=del_files
        ).grid(row=counter(), column=0)

    if debug_std:
        tk.Button(
            master=root,
            text="STD递归删除指定类型文件",
            width=width,
            command=del_files_std
            ).grid(row=counter.last, column=1)

    tk.Button(
        master=root,
        text="递归删除空文件夹",
        width=width,
        command=del_empty_folder
        ).grid(row=counter(), column=0)

    tk.Button(
        master=root,
        text="递归删除没有指定类型文件的文件夹",
        width=width,
        command=del_empty_content_folder
        ).grid(row=counter(), column=0)

    tk.Button(
        master=root,
        text="递归删除包含指定类型文件的文件夹",
        width=width,
        command=del_with_content_folder
        ).grid(row=counter(), column=0)

    """
    ----------------------------------------------------------------------
    """
    tk.Label(
        master=root,
        text=delimiter*width
        ).grid(row=counter(), column=0)
    if debug_std:
        tk.Label(
            master=root,
            text=delimiter*width
            ).grid(row=counter.last, column=1)

    tk.Button(
        master=root,
        text="递归重建空文件夹树",
        width=width,
        command=rebuild_empty_tree
        ).grid(row=counter(), column=0)

    tk.Button(
        master=root,
        text="递归重建文件夹树并拷贝指定类型文件",
        width=width,
        command=rebuild_content_tree
        ).grid(row=counter(), column=0)

    """
    ----------------------------------------------------------------------
    """
    tk.Label(
        master=root,
        text=delimiter*width
        ).grid(row=counter(), column=0)
    if debug_std:
        tk.Label(
            master=root,
            text=delimiter*width
            ).grid(row=counter.last, column=1)

    root.mainloop()
