# -*- coding: utf-8 -*-
import ConfigParser
import CFGParser
import XMLParser
import xml.etree.cElementTree as cET

__name__ = "CFG Freedom"
__version__ = 1.0

print """ ______     ______   ______        ______   ______     ______     ______     _____     ______     __    __
/\  ___\   /\  ___\ /\  ___\      /\  ___\ /\  == \   /\  ___\   /\  ___\   /\  __-.  /\  __ \   /\ "-./  \\
\ \ \____  \ \  __\ \ \ \__ \     \ \  __\ \ \  __<   \ \  __\   \ \  __\   \ \ \/\ \ \ \ \/\ \  \ \ \-./\ \\
 \ \_____\  \ \_\    \ \_____\     \ \_\    \ \_\ \_\  \ \_____\  \ \_____\  \ \____-  \ \_____\  \ \_\ \ \_\\
  \/_____/   \/_/     \/_____/      \/_/     \/_/ /_/   \/_____/   \/_____/   \/____/   \/_____/   \/_/  \/_/
coded by Lord13                                                                                          v1.0
"""
read_file = CFGParser.CFGParsing('conf_theme.cfg')
mains, infos, others = read_file.read_file()

Main = XMLParser.Main(has_info=True)

parameters = Main.add_parameters(name="Texture On Stone", author="Jay-Jay", debug=False)
salvar, imprimir = Main.read_parameters(mains, others, parameters, infos)

with open('filename.xml', 'w+') as filen:
    for i in str(XMLParser.print_elements(salvar)):
        filen.write(i)

#print XMLParser.print_elements(imprimir)
