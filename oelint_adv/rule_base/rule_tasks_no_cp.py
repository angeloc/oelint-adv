from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Function
from oelint_parser.rpl_regex import RegexRpl


class TaskInstallNoCp(Rule):
    def __init__(self):
        super().__init__(id='oelint.task.nocopy',
                         severity='error',
                         message='\'cp\' shall not be used in do_install. Use \'install\'')

    def check(self, _file, stash):
        res = []
        for item in stash.GetItemsFor(filename=_file, classifier=Function.CLASSIFIER):
            if item.FuncName.startswith('do_install'):
                for lineindex, line in enumerate(item.get_items()):
                    if line.strip().startswith('#'):
                        continue
                    if RegexRpl.search(r'\s*cp ', line) and not RegexRpl.search(r'\s*cp\s+(-R|-r)', line):
                        res += self.finding(item.Origin,
                                            item.InFileLine + lineindex, blockoffset=item.InFileLine)
        return res
