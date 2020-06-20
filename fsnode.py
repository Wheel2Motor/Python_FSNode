# -*- coding: utf-8 -*-
"""
2020年6月15日.

@author: 李伟
@mail: 1462965949@qq.com
"""

import os
import shutil


class FSNode():
    """File System Node."""

    @classmethod
    def equal(cls, node1, node2, *argv, **kargv):
        """比较两个节点是否数据相同."""
        return (node1.sort == node2.sort) and \
            (node1.level == node2.level) and \
            (node1.suffix == node2.suffix) and \
            (node1.abs_dirname == node2.abs_dirname) and \
            (node1.content == node2.content) and \
            (
                {i.abs_dirname for i in node1.subnode} ==
                {i.abs_dirname for i in node2.subnode}
            ) and \
            (
                ((not node1.supnode) and (not node2.supnode)) or
                (
                    (node1.supnode and node2.supnode) and
                    (node1.supnode.abs_dirname == node2.supnode.abs_dirname)
                )
            )

    @classmethod
    def parse_super_dir(cls, dirname, *argv, **kargv):
        """推导输入目录的上级目录."""
        dirname = os.path.join(dirname, "..")
        dirname = os.path.abspath(dirname)
        return dirname

    @classmethod
    def parse_super_name(cls, fullname, *argv, **kargv):
        """推导输入文件名在上级目录下的名称."""
        dirname = os.path.dirname(fullname)
        basename = os.path.basename(fullname)
        dirname = os.path.join(dirname, "..")
        fullname = os.path.join(dirname, basename)
        fullname = os.path.abspath(fullname)
        return fullname

    @classmethod
    def parse_super_dir_s(cls, dirname, *argv, **kargv):
        """推导输入目录的上级目录，_s版本确保目录存在."""
        dirname = FSNode.parse_super_dir(dirname)
        if os.path.exists(dirname):
            return dirname
        else:
            return None

    @classmethod
    def parse_super_name_s(cls, fullname, *argv, **kargv):
        """推导输入文件名在上级目录下的名称, _s版本确保目录存在."""
        fullname = FSNode.parse_super_name(fullname)
        dirname = os.path.dirname(fullname)
        if os.path.exists(dirname):
            return fullname
        else:
            return None

    def __init__(
            self,
            dirname=".",
            suffix="",
            parent=None,
            level=0,
            sort=False,
            *argv,
            **kargv
            ):
        self.__level = 0
        self.__supnode = None
        self.__dirname = ""
        self.__suffix = ""
        self.__content = set()
        self.__subnode = set()
        assert isinstance(dirname, str)
        assert isinstance(suffix, str)
        assert isinstance(parent, FSNode) or (not parent)
        assert isinstance(level, int)
        assert isinstance(sort, bool)
        self.__level = level
        self.__supnode = parent
        self.__dirname = os.path.abspath(dirname)
        self.__suffix = suffix
        self.__sort = sort
        self.update()

    @property
    def suffix(self):
        """获取文件识别后缀名."""
        return self.__suffix

    @property
    def level(self):
        """获取节点层级，根节点为0."""
        return self.__level

    @property
    def sort(self):
        """是否需要名称按照长度优先排序."""
        return self.__sort

    @property
    def dirname(self):
        """获取节点目录的相对路径."""
        return os.path.basename(self.__dirname)

    @property
    def abs_dirname(self):
        """获取节点目录的绝对路径."""
        return self.__dirname

    @property
    def content(self):
        """获取节点下所有识别的文件相对路径集合."""
        if self.sort:
            return sorted(self.__content, key=lambda item: (len(item), item))
        else:
            return list(self.__content)

    @property
    def abs_content(self):
        """获取节点下所有识别的文件绝对路径集合."""
        if self.sort:
            return sorted(map(
                lambda item: os.path.join(self.__dirname, item),
                self.__content
                ), key=lambda item: (len(item), item))
        else:
            return list(map(
                lambda item: os.path.join(self.__dirname, item),
                self.__content
                ))

    @property
    def content_size(self):
        """获取节点下所有识别文件dict{相对路径:文件大小}."""
        return list(map(
            lambda item: (
                item,
                os.path.getsize(os.path.join(self.abs_dirname, item))
                ),
            self.content
            ))

    @property
    def abs_content_size(self):
        """获取节点下所有识别文件dict{绝对路径:文件大小}."""
        return list(map(
            lambda item: (item, os.path.getsize(item)),
            self.abs_content
            ))

    @property
    def content_atime(self):
        """获取节点下所有识别文件的最近访问时间dict{相对路径:最近访问时间}."""
        return list(map(
            lambda item: (
                item,
                os.path.getatime(os.path.join(self.abs_dirname, item))
                ),
            self.content
            ))

    @property
    def abs_content_atime(self):
        """获取节点下所有识别文件的最近修改时间dict{绝对路径:最近访问时间}."""
        return list(map(
            lambda item: (item, os.path.getatime(item)),
            self.abs_content
            ))

    @property
    def content_ctime(self):
        """获取节点下所有识别文件的创建时间dict{相对路径:创建时间}."""
        return list(map(
            lambda item: (
                item,
                os.path.getctime(os.path.join(self.abs_dirname, item))
                ),
            self.content
            ))

    @property
    def abs_content_ctime(self):
        """获取节点下所有识别文件的创建时间dict{绝对路径:创建时间}."""
        return list(map(
            lambda item: (item, os.path.getctime(item)),
            self.abs_content
            ))

    @property
    def content_mtime(self):
        """获取节点下所有识别文件的最近修改时间dict{相对路径:最近访问时间}."""
        return list(map(
            lambda item: (
                item,
                os.path.getmtime(os.path.join(self.abs_dirname, item))
                ),
            self.content
            ))

    @property
    def abs_content_mtime(self):
        """获取节点下所有识别文件的最近修改时间dict{绝对路径:最近访问时间}."""
        return list(map(
            lambda item: (item, os.path.getmtime(item)),
            self.abs_content
            ))

    @property
    def subnode(self):
        """获取当前节点的所有子节点."""
        if self.sort:
            return sorted(
                self.__subnode,
                key=lambda item: (len(item.dirname), item.dirname)
                )
        else:
            return list(self.__subnode)

    @property
    def supnode(self):
        """获取当前节点的父节点."""
        return self.__supnode

    def __repr__(self):
        """获取上级节点."""
        represent_str = ""
        represent_str += "NODE : " + self.dirname + "\n"
        represent_str += "SUFFIX : " + self.suffix + "\n"
        represent_str += "CONTENT CNT : " + str(len(self.content)) + "\n"
        represent_str += "SUBNODE CNT : " + str(len(self.subnode)) + "\n"
        represent_str += "CONTENT : \n"
        for i in self.content:
            represent_str += "--- " + i + "\n"
        represent_str += "SUBNODE : \n"
        for i in self.subnode:
            represent_str += "--- " + i.dirname + "\n"
        return represent_str

    def __str__(self):
        """直接打印单个节点."""
        return self.abs_dirname

    def __sub__(self, number):
        """单个节点强制转换字符串."""
        assert isinstance(number, int) and (number >= 0)
        node = self
        for i in range(number):
            if node.supnode:
                node = node.supnode
        return node

    def __update_content(self):
        self.__content = set()
        for i in os.listdir(self.__dirname):
            if os.path.isfile(os.path.join(self.__dirname, i)):
                if i.endswith(self.__suffix):
                    self.__content.add(os.path.basename(i))

    def __update_subnode(self):
        self.__subnode = set()
        for i in os.listdir(self.__dirname):
            if os.path.isdir(os.path.join(self.__dirname, i)):
                self.__subnode.add(
                    type(self)(
                        dirname=os.path.join(self.__dirname, i),
                        suffix=self.__suffix,
                        parent=self,
                        level=self.__level+1,
                        sort=self.__sort
                        ))

    def update(self, *argv, **kargv):
        """更新子节点列表和内容列表."""
        self.__update_content()
        self.__update_subnode()

    def get_traversal_treeinfo(
            self,
            indent="|   ",
            header_folder="|---",
            header_file="|-> ",
            include_empty_folder=False,
            *argv,
            **kargv
            ):
        """获取所有节点下节点、识别文件树状信息."""
        assert isinstance(indent, str)
        assert isinstance(header_folder, str)
        assert isinstance(header_file, str)
        assert isinstance(include_empty_folder, bool)
        represent_str = ""
        represent_str += "NODE : " + self.dirname + "\n"
        for i in self.content:
            represent_str += self.level * indent + header_file + i + "\n"
        for i in self.subnode:
            if (
                    (not include_empty_folder) and
                    (not i.get_traversal_content())
                    ):
                continue
            represent_str += self.level * indent + \
                header_folder + \
                i.get_traversal_treeinfo(
                    indent=indent,
                    header_folder=header_folder,
                    header_file=header_file,
                    include_empty_folder=include_empty_folder
                    )
        return represent_str

    def get_traversal_content(self, *argv, **kargv):
        """获取所有节点下所有识别文件."""
        content = set()
        for root, dirs, files in os.walk(self.abs_dirname):
            for f in files:
                if not f.endswith(self.suffix):
                    continue
                fullname = os.path.join(root, f)
                fullname = os.path.abspath(fullname)
                content.add(fullname)
        return list(content)

    def get_traversal_nodes(self, *argv, **kargv):
        """获取当前节点和所有子节点."""
        content = self.subnode
        for i in self.subnode:
            content += i.get_traversal_nodes()
        return content

    def get_traversal_folders(self, *argv, **kargv):
        """获取当前文件夹和所有子文件夹."""
        content = set()
        for root, dirs, files in os.walk(self.abs_dirname):
            for f in dirs:
                path = os.path.join(root, f)
                path = os.path.abspath(path)
                content.add(path)
        return list(content)

    def remove_traversal_content(
            self,
            log=False,
            warning=True,
            *argv,
            **kargv
            ):
        """递归删除所有节点下所有识别文件."""
        for i in self.subnode:
            i.remove_traversal_content(log=log, warning=warning)
        self.__update_content()
        for i in self.abs_content:
            try:
                os.remove(i)
                if log:
                    print("Removed".ljust(20, "-"), i)
            except Exception as e:
                if warning:
                    print(e)

    def remove_empty_content_folders(
            self,
            log=False,
            warning=True,
            *argv,
            **kargv
            ):
        """递归删除所有子节点下没有识别文件类型的文件夹."""
        for i in self.subnode:
            i.remove_empty_content_folders(log=log, warning=warning)
        self.__update_subnode()
        if (not self.subnode) and (not self.content):
            try:
                shutil.rmtree(self.abs_dirname)
                if log:
                    print("Removed".ljust(20, "-"), self.abs_dirname)
            except Exception as e:
                if warning:
                    print(e)

    def remove_with_content_folders(
            self,
            log=False,
            warning=True,
            *argv,
            **kargv
            ):
        """递归删除所有子节点包含有识别文件类型的文件夹."""
        for i in self.subnode:
            i.remove_with_content_folders(log=log, warning=warning)
        self.__update_subnode()
        if self.content:
            try:
                shutil.rmtree(self.abs_dirname)
                if log:
                    print("Removed".ljust(20, "-"), self.abs_dirname)
            except Exception as e:
                if warning:
                    print(e)

    def remove_empty_folders(
            self,
            log=False,
            warning=True,
            *argv,
            **kargv
            ):
        """递归删除所有子节点下空文件夹，包括自己."""
        for i in self.subnode:
            i.remove_empty_folders(log=log, warning=warning)
        self.__update_subnode()
        if not os.listdir(self.abs_dirname):
            try:
                os.rmdir(self.abs_dirname)
                if log:
                    print("Removed".ljust(20, "-"), self.abs_dirname)
            except Exception as e:
                if warning:
                    print(e)

    def rebuild_dirs(
            self,
            parent_dirname,
            copy_file=False,
            log=False,
            warning=True,
            *argv,
            **kargv
            ):
        """在新的路径下重建目录树."""
        assert not self.abs_dirname == parent_dirname
        target_dirname = os.path.join(parent_dirname, self.dirname)
        try:
            if not os.path.exists(target_dirname):
                os.makedirs(target_dirname)
                if log:
                    print("Rebuilt".ljust(20, "-"), target_dirname)
            if copy_file:
                for i, j in zip(self.abs_content, self.content):
                    src = i
                    dst = os.path.join(target_dirname, j)
                    shutil.copyfile(src, dst)
                    if log:
                        print("Copied".ljust(20, "-"), src)
                        print("To".ljust(20, "-"), dst)
            return target_dirname
        except Exception as e:
            if warning:
                print(e)
            return None

    def rebuild_dirs_tree(
            self,
            parent_dirname,
            copy_file=False,
            log=False,
            warning=True,
            *argv,
            **kargv
            ):
        """在新的目录下重建目录树及子目录."""
        target_dirname = self.rebuild_dirs(
            parent_dirname=parent_dirname,
            copy_file=copy_file,
            log=log,
            warning=warning
            )
        if target_dirname:
            for i in self.subnode:
                i.rebuild_dirs_tree(
                    target_dirname,
                    copy_file=copy_file,
                    log=log,
                    warning=warning
                    )
