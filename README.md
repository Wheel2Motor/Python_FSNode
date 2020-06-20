# Python_FSNode

## Introduction
### File system node. 
### Easy methods for file system recursive operation.
The motivation for writing this python class is for easy folder recursive operation.
After searching and searching on the internet, people always give some awkward methods, these methods can truely run, but not convenient.

## Structure
|FSNode

|---__content(str1, str2, str3)

|---__subnode(FSNode1, FSNode2, FSNode3)

## Example

#### 获取当前文件夹下所有文件相对路径
FSNode().content

#### 获取当前文件夹下所有文件绝对路径
FSNode().abs_content

#### 获取当前文件夹节点相对路径（名称）
FSNode().dirname

#### 获取当前文件夹节点绝对路径
FSNode().abs_dirname

#### 获取当前文件夹节点子文件夹节点
FSNode().subnode

#### 获取当前文件夹节点上级节点
FSNode().supnode

#### 递归删除.png文件
FSNode(".png").remove_traversal_content()

#### 递归获取所有文件
FSNode().get_traversal_content()

#### 递归清理空文件夹
FSNode(suffix="*").remove_empty_folders()

#### 递归清理没有.png文件的所有文件夹
FSNode(".png").remove_empty_content_folders()

#### 递归清理包含.png文件的所有文件夹

FSNode(".png").remove_with_content_folder()

#### 获取所有指定类型文件的树状信息字符串
FSNode(".png").get_traversal_treeinfo()

#### 重建空的目录树
FSNode(src_path).rebuild_dirs_tree(target_parent_path)

#### 重建目录树并拷贝指定类型文件
FSNode(src_path, suffix=".png").rebuild_dirs_tree(target_parent_path, copy_file=True)

#### 推导上级目录
FSNode.parse_super_dir("./")

#### 推导当前文件在上级目录下的名称（安全版，确保上级目录一定存在）
FSNode.parse_super_name_s("./test.png")

首次上传，还没来及写帮助文档，具体请看fsnode_util.py中的示例
