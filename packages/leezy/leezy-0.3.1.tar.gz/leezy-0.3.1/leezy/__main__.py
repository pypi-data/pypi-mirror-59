import argparse

from leezy.crawler import Problem
from leezy.utils import CFG

from leezy.errors import show_error_and_exit, LeezyError


def pull(args):
    for pid in expand_ids(args.ids):
        try:
            Problem(pid, args.context).pull()
        except LeezyError as e:
            show_error_and_exit(e)
        except Exception as e:
            print(f'Uncaught Exception: {e!r}')


def expand_ids(ids_arg):
    if len(ids_arg) == 1 and ids_arg[0].count('-') == 1:
        s, e = ids_arg[0].split('-')[:2]
        return list(range(int(s), int(e)+1))
    else:
        return ids_arg


def show(args):
    for pid in expand_ids(args.ids):
        try:
            print(Problem(pid).digest())
        except LeezyError as e:
            show_error_and_exit(e)
        except Exception as e:
            print(f'Uncaught Exception: {e!r}')


def config(args):
    kvs = CFG.open()
    if args.list:
        print('\n'.join(map('='.join, CFG.fetch_all(kvs, ''))))
    elif args.add:
        CFG.store(kvs, args.add[0], args.add[1])
    elif args.unset:
        CFG.unset(kvs, args.unset[0])
    if args.add or args.unset:
        CFG.write(kvs)


parser = argparse.ArgumentParser(prog='leezy',usage='leezy [-h] COMMAND [...]')
subs = parser.add_subparsers(
    title="commands",
    description="use 'leezy command -h' to see more",
    metavar='')

pull_parser = subs.add_parser('pull', help='拉取题目到本地文件')
pull_parser.add_argument('ids', nargs='+', help="题目编号，多个使用空格分隔")
pull_parser.add_argument('--context', choices=['tree', 'linked_list'],
                         help="题目上下文，影响题目参数转换")
pull_parser.set_defaults(func=pull)

show_parser = subs.add_parser('show', help='打印编号的题目')
show_parser.add_argument('ids', nargs='+', help="题目编号，多个使用空格分隔")
show_parser.set_defaults(func=show)

config_parser = subs.add_parser('config', help='全局配置')
group = config_parser.add_mutually_exclusive_group()
group.add_argument('--add', nargs=2, metavar='', help='name value')
group.add_argument('--unset', nargs=1, metavar='', help='name')
group.add_argument('--list', action='store_true')
config_parser.set_defaults(func=config)

args = parser.parse_args()
if len(args._get_kwargs()) + len(args._get_args()) == 0:
    parser.print_help()
else:
    args.func(args)

# this is for setup:entry_points:console_scripts
def dummy_main(*_args, **_kwargs):
    return
