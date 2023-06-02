from os import path as op
import yaml

"""
    上面的代码包含用于读取和写入 YAML 文件以及从 YAML 数据结构中检索特定值的 Python 函数。
    
    Args:
      url (str): 一个字符串，表示要读取的 YAML 文件的文件路径或 URL。
"""


default_path = "./data/fck.yaml"


def read(url: str) -> dict:
    """
    此 Python 函数从给定的 URL 读取 YAML 文件并将其内容作为字典返回。

    Args:
      url (str): `url` 参数是一个字符串，表示需要读取的 YAML 文件的文件路径或 URL。

    Returns:
      包含位于指定 URL 的 YAML 文件内容的字典。
    """
    with open(op.abspath(url), mode="r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg


def settings_get(path: str, key="default"):
    """
    此函数读取配置文件并返回指定键的值，如果找不到该键，则返回默认值。

    Args:
      path (str): 表示配置文件路径的字符串。
      key: “key”参数是一个可选参数，默认值为“default”。它用于指定要从配置文件中检索的特定值。如果配置文件是一个字典，将返回与指定键关联的值。如果配置文件是一个列表，则.
    Defaults to default

    Returns:
      位于给定路径的配置文件中指定的键的值。如果配置文件是字典，它将返回与指定键关联的值。如果配置文件是一个列表，它将返回指定索引处的值。如果找不到密钥，它将返回 None。
    """
    cfg = read(op.abspath(path))
    return (
        get_dict_value(cfg, key) if isinstance(cfg, dict) else get_list_value(cfg, key)
    )


def get_list_value(now_list: list, target_key, results=[], mod="value"):
    """
    此函数递归地在字典列表中搜索目标键并返回相应的值。

    Args:
      now_list (list): 需要搜索目标键的列表。
      target_key: 参数 target_key 是我们要在列表或字典中搜索的键。该函数将返回与此键关联的值。
      results: results 参数是一个默认的可变参数，用于存储在递归遍历列表或字典期间找到的 target_key 的值。它被初始化为一个空列表，并作为参数传递给递归函数调用。
    target_key 的值附加到
      mod: mod 参数是一个字符串，指定函数的操作模式。它可以有两个可能的值：“value”或“key”。如果 mod 设置为“value”，该函数将在字典列表中搜索与 target_key
    关联的值。如果设置了mod. Defaults to value

    Returns:
      该函数将返回列表中目标键第一次出现的值。如果未找到目标键，它将返回 None。
    """
    # sourcery skip: default-mutable-arg
    for i in now_list:  # 当前迭代的list
        if isinstance(i, dict):  # 如果data是一个字典，就调用递归函数：get_dict_value()进行遍历
            get_dict_value(i, target_key, results=results)
        elif isinstance(i, list):  # 如果data是一个列表，就调用递归函数：get_list_value()进行遍历
            get_list_value(i, target_key, results=results)
    return results


def get_dict_value(now_dict: dict, target_key, results=[]):
    """
    此函数递归地在字典中搜索目标键并返回其值。

    Args:
      now_dict (dict): 我们要搜索特定键及其对应值的字典。
      target_key: 我们要检索其值的字典中的键。
      results: 参数“results”是一个列表，用于存储在通过字典进行递归搜索期间找到的目标键的值。它在函数定义中被初始化为一个空列表，并作为参数传递给递归调用以存储结果。的最终价值

    Returns:
      输入字典中目标键第一次出现的值。
    """
    # sourcery skip: default-mutable-arg
    for key, value in now_dict.items():  # 当前迭代的字典
        if isinstance(value, dict):  # 如果data是一个字典，就调用递归函数：get_dict_value()进行遍历
            get_dict_value(value, target_key, results=results)
        elif isinstance(value, list):  # 如果data是一个列表，就调用递归函数：get_list_value()进行遍历
            get_list_value(value, target_key, results=results)
        if key == target_key and not isinstance(value, (dict, list)):
            # 如果key等于target_key，而且value不为字典或列表
            # 则将当前key对应的键加入results中
            results.append(now_dict[key])
    return results


def write(cfg, write_path, dict1, k=None, n=0, mod="change"):
    """
    此函数将字典或列表写入指定路径的 YAML 文件，也可以将新字典添加到原始字典中的特定键。

    Args:
      cfg: 配置数据，可以是字典或列表。
      write_path: YAML 数据将写入的文件路径。
      dict1: 需要写入 YAML 文件的字典。
      k: “k”是一个键列表，表示到嵌套字典中需要写入新数据的特定位置的路径。
      n: 参数“n”是一个整数，用于跟踪函数中的递归深度。Defaults to 0
    Returns:
      包含更新的 `cfg` 字典和 `father` 列表的元组。
    """
    # sourcery skip: default-mutable-arg, low-code-quality
    if k is None:
        return "Error Code: 0"
    data = {}
    if isinstance(cfg, dict):  # 当cfg为字典
        for key, value in cfg.items():  # 取出cfg中的键值对
            if key in k:  # 当cfg中的键key在k列表中时
                if key == k[-1] and isinstance(value, list):
                    # 当key在k列表的最后一个时，意味着已经匹配到最终的路径，
                    # 如果value为dict，则直接将要写入或刷新的字典与原字典拼合，
                    # 由于Python的dict的特性，刷新value的值，cfg的值也会随之改变。
                    if mod != "remove":
                        value.append(dict1)
                    else:
                        # 当method为remove时
                        for dict_key in dict1.keys():
                            # 遍历要删除的键
                            for text in value:
                                # 遍历value这一列表，取出字典元素
                                if dict_key in text:
                                    # 当要删除的键在value的元素中时，
                                    # 将该元素从value中删除
                                    value.remove(text)
                    data = cfg
                elif key == k[-1] and isinstance(value, dict):  # 当cfg为列表时
                    # PS：该种情况极难出现，所以该elif已停止维护
                    cfg[key] = value
                    data = cfg
                    # data.update(dict1)
                elif key != k[-1] and isinstance(value, dict):
                    # 该elif为递归的起点，十分重要
                    # 当key与k列表中最后一个值不匹配，且value为一个字典时，
                    # 将当前的value作为新一轮递归的cfg，递归深度值加一
                    cfg[key] = write(
                        value, write_path=write_path, dict1=dict1, k=k, n=n + 1, mod=mod
                    )
                    data = cfg
            if n == 0:
                # 将处理完毕的data字典写入write_path所指定的文件中，
                # Args：
                # allow_unicode：让yaml文件支持Unicode编码，能正常显示中文
                # indent：让yaml文件拥有缩进，增强可读性
                # Function：
                #   yaml.safe_dump()相较与yaml.dump()更加安全
                #   safe_dump()不会加载yaml文件中的不安全的对象(object)
                with open(op.abspath(write_path), mode="+w", encoding="utf-8") as f:
                    yaml.safe_dump(data, f, allow_unicode=True, indent=2)
    elif isinstance(cfg, list):
        if dict1 not in cfg:
            cfg.append(dict1)
            data = cfg
            with open(op.abspath(write_path), mode="+w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, allow_unicode=True, indent=2)
    return cfg  # 返回结果


def key_clever(key: str):
    """
    该函数按句点拆分字符串并返回结果子字符串的列表，如果没有句点则返回原始字符串。

    Args:
      key (str): 输入参数是一个名为“key”的字符串。

    Returns:
      函数 key_clever 将字符串 key 作为输入，并使用句点 (.) 作为分隔符将其拆分为字符串列表。如果结果列表只有一个元素，则该函数将该元素作为字符串返回。否则，该函数返回字符串列表。
    """
    keys = key.split(".")
    if len(keys) == 1:
        keys = key
    return keys


def wr_first(cfg: dict, write_path: str, dict1: dict, k: str, n=0, mod="change"):
    """
    如果输入“k”是一个列表，此函数将调用带有特定参数的另一个函数“write”。

    Args:
      cfg: 它可能是一个配置对象或字典，其中包含要使用的函数的各种设置和选项。
      write_path: 将写入输出的文件路径。
      dict1: 包含键值对的字典对象。
      k: 参数 `k` 是一个列表，用作访问 `dict1` 字典中特定值的键。它是一个可选参数，默认值为“None”。
      n: 参数“n”是一个整数，表示字典中的嵌套级别。它用于在遍历字典时跟踪字典的深度。 “n”的初始值为0，表示函数从字典的顶层开始. Defaults to 0
    """
    # sourcery skip: default-mutable-arg
    write_path = op.abspath(write_path)  # 获取绝对路径
    if isinstance(k, str):
        # 当k为字符串时，将它格式化为一个List
        k = key_clever(k)
        write(cfg, write_path=write_path, dict1=dict1, k=k, n=n, mod=mod)


if __name__ == "__main__":
    wr_first(
        read(default_path),
        default_path,
        {"picgo": "https://picgo.github.io/PicGo-Doc/zh/"},
        k="settings.login",
        mod="remove",
    )
