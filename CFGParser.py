# -*- coding: utf-8 -*-

class CFGParsing(object):
    def __init__(self, filename):
        self.filename = filename

    def read_file(self):

        file_for_parsing = open(self.filename, 'r+')
        list_of_lines = [x.strip('\n').strip('\t') for x in file_for_parsing.readlines()]
        all_main, all_info = [], []
        mains = {}
        infos = {}
        others = []

        for i in list_of_lines:
            if i[0:4] == 'main':
                all_main.append(list_of_lines.index(i))
            elif "info" in i:
                all_info.append(list_of_lines.index(i))
            else:
                others.append(i)

        for i in all_main:
            if i != all_main[-1]:
                new_list = list_of_lines[i:all_main[all_main.index(i) + 1]]
                mains[new_list[0]] = new_list[1:]
            else:
                new_list = list_of_lines[i:list_of_lines.index('info0:')]
                mains[new_list[0]] = new_list[1:]

        if len(all_info) != 0:
            for i in all_info:
                if i != all_info[-1]:
                    new_list = list_of_lines[i:all_info[all_info.index(i) + 1]]
                    infos[new_list[0]] = new_list[1:]
                else:
                    new_list = list_of_lines[i:]
                    infos[new_list[0]] = new_list[1:]

        file_for_parsing.close()
        return mains, infos, others
