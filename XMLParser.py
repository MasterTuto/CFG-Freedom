import xml.etree.cElementTree as ET
import xml.dom.minidom as minidom
import clipboard


class Main(object):
    def __init__(self, has_info=False, width=640, height=480):
        self.has_info = has_info
        self.width = width
        self.height = height

    def add_parameters(self, name="<NO NAME>", author="<NO AUTHOR>", debug=False):
        root = ET.Element('ThemeConfig')
        ET.SubElement(root, "Name").text = name
        ET.SubElement(root, "Author").text = author
        ET.SubElement(root, "HasInfoPage").text = str(self.has_info).lower()
        ET.SubElement(root, "Width").text = str(self.width)
        ET.SubElement(root, "HeightY").text = str(self.height)
        ET.SubElement(root, "Debug").text = str(debug).lower()
        c = ET.ElementTree(root)
        return c

    def read_parameters(self, mainpage, others, reading, infopage=None):
        others = filter(lambda opt_value: len(opt_value.split('=')) > 1, others)
        others = [x.split("=") for x in others]
        reading = reading
        root = reading.getroot()
        main_page = ET.SubElement(root, 'MainPage')
        if self.has_info:
            info_page = ET.SubElement(root, 'InfoPage')
            info_elements = ET.SubElement(info_page, 'Elements')

        main_elements = ET.SubElement(main_page, 'Elements')
        last_used = None
        possible_use = None
        has_height = False
        has_width = False
        num = 0

        for i in others:
            if i[0] == 'bg_color':
                ET.SubElement(main_page, 'BgColor').text = i[1]
                print type(info_page)
                if self.has_info:
                    ET.SubElement(info_page, 'BgColor').text = i[1]
            elif i[0] == 'sel_text_color':
                sel_color = i[1]
            elif i[0] == 'text_color':
                text_color = i[1]
            elif i[0] == 'ui_text_color':
                ui_color = i[1]

        for i in mainpage:
            mainpage[i] = [n.split('=') for n in mainpage[i]]
            mainpage[i] = filter(lambda funny: len(funny) > 1, mainpage[i])

            num += 1
            for j in mainpage[i]:
                if j[1] == 'Background':
                    ET.SubElement(main_elements, 'Background', {'type': 'BG'})
                elif j[1] == 'COV2':
                    cov2 = ET.SubElement(main_elements, 'Image', {'type': 'COV2'})
                    ET.SubElement(cov2, 'origin').text = "Center"
                    last_used = cov2
                elif j[1] == "MenuIcon":
                    break
                elif j[1] == 'ItemCover':
                    cov = ET.SubElement(main_elements, 'Image', {'type': 'COV'})
                    ET.SubElement(cov, 'origin').text = "Center"
                    last_used = cov
                elif j[1] == 'ItemIcon':
                    icon = ET.SubElement(main_elements, 'Image', {'type': 'ICO'})
                    ET.SubElement(icon, 'origin').text = "Center"
                    last_used = icon
                elif j[1] == 'LAB':
                    lab = ET.SubElement(main_elements, 'Image', {'type': 'LAB'})
                    ET.SubElement(lab, 'origin').text = "Center"
                    last_used = lab
                elif j[1] == 'ItemsList':
                    lista = ET.SubElement(main_elements, 'GameList')
                    ET.SubElement(lista, 'color').text = text_color
                    ET.SubElement(lista, 'colorSelected').text = sel_color
                    ET.SubElement(lista, 'fontSize').text = '15'
                    last_used = lista
                    possible_use = 'list'
                elif j[1] == 'HintText':
                    hinttext = ET.SubElement(main_elements, 'Text')
                    ET.SubElement(hinttext, 'color').text = text_color
                    ET.SubElement(hinttext, 'align').text = 'Center'
                    ET.SubElement(hinttext, 'text').text = '{OPLM:Help}'
                    ET.SubElement(hinttext, 'fontSize').text = '18'
                    last_used = hinttext
                    possible_use = 'list'
                elif j[0] == 'x' and last_used is not None:
                    if int(j[1]) < 0:
                        new_x = str(self.width + int(j[1]))
                        ET.SubElement(last_used, 'x').text = new_x
                    else:
                        ET.SubElement(last_used, 'x').text = j[1]
                elif j[0] == 'y' and last_used is not None:
                    if int(j[1]) < 0:
                        new_y = str(self.height + int(j[1]))
                        ET.SubElement(last_used, 'y').text = new_y
                    else:
                        ET.SubElement(last_used, 'y').text = j[1]
                elif j[0] == 'height' and possible_use == 'list' and j[1] != 'DIM_INF':
                    ET.SubElement(last_used, 'maxHeight').text = j[1]
                elif j[0] == 'width' and possible_use == 'list' and j[1] != 'DIM_INF':
                    ET.SubElement(last_used, 'maxWidth').text = j[1]
                elif j[0] == 'height' and possible_use != 'list' and j[1] != 'DIM_INF':
                    ET.SubElement(last_used, 'heightY').text = j[1]
                elif j[0] == 'width' and possible_use != 'list' and j[1] != 'DIM_INF':
                    ET.SubElement(last_used, 'widthX').text = j[1]

            last_used = None

        if self.has_info:
            for i in infopage:
                infopage[i] = [n.split('=') for n in infopage[i]]
                infopage[i] = filter(lambda info_item: len(info_item) > 1, infopage[i])

                num += 1
                print i
                for item in infopage[i]:
                    print item
                    if item[1] == '#Size':
                        size = ET.SubElement(info_elements, 'Text')
                        ET.SubElement(size, 'color').text = text_color
                        ET.SubElement(size, 'text').text = '{OPLM:Size}'
                        ET.SubElement(size, 'fontSize').text = '15'
                        last_used = size
                    elif item[1] == 'Players':
                        players = ET.SubElement(info_elements, 'Image', {'type': 'CFG'})
                        ET.SubElement(players, 'source').text = 'Players'
                        ET.SubElement(players, 'origin').text = 'Center'
                        last_used = players
                    elif item[1] == 'LoadingIcon':
                        break
                    elif item[1] == 'Cheat':
                        cheat = ET.SubElement(info_elements, 'Text')
                        ET.SubElement(cheat, 'fontSize').text = '15'
                        ET.SubElement(cheat, 'color').text = text_color
                        ET.SubElement(cheat, 'text').text = '{CFG:Cheat}'
                        last_used = cheat
                    elif item[1] == 'Developer':
                        dev = ET.SubElement(info_elements, 'Text')
                        ET.SubElement(dev, 'text').text = '{CFG:Developer}'
                        ET.SubElement(dev, 'fontSize').text = '15'
                        ET.SubElement(dev, 'color').text = text_color
                        last_used = dev
                    elif item[1] == 'Description':
                        desc = ET.SubElement(info_elements, 'Text')
                        ET.SubElement(desc, 'text').text = '{CFG:Description}'
                        ET.SubElement(desc, 'fontSize').text = '15'
                        ET.SubElement(desc, 'color').text = text_color
                        last_used = desc
                    elif item[1] == 'StaticText':
                        statictext = ET.SubElement(info_elements, 'Text')
                        last_used = statictext
                    elif item[1] == '#Format':
                        formato = ET.SubElement(info_elements, 'Image', type='OPLM')
                        ET.SubElement(formato, 'source').text = "#Format"
                        ET.SubElement(formato, 'origin').text = 'Center'
                        last_used = formato
                    elif item[1] == 'PS1ID':
                        break
                    elif item[1] == 'Scan':
                        scan = ET.SubElement(info_elements, 'Image', type="CFG")
                        has_height = True
                        has_width = True
                        ET.SubElement(scan, 'source').text = 'Scan'
                        ET.SubElement(scan, 'origin').text = 'Center'
                        last_used = scan
                    elif item[1] == 'SCR':
                        scr1 = ET.SubElement(info_elements, 'Image', {'type': 'SCR'})
                        ET.SubElement(scr1, 'origin').text = 'Center'
                        has_height = True
                        has_width = True
                        possible_use = 'image'
                        last_used = scr1
                    elif item[1] == 'Release':
                        release = ET.SubElement(info_elements, 'Text')
                        ET.SubElement(release, 'fontSize').text = '15'
                        ET.SubElement(release, 'color').text = text_color
                        ET.SubElement(release, 'text').text = '{CFG:Release}'
                        last_used = release
                    elif item[1] == 'Parental':
                        parental = ET.SubElement(info_elements, 'Image', type='CFG')
                        ET.SubElement(parental, 'origin').text = 'Center'
                        ET.SubElement(parental, 'source').text = 'Parental'
                        last_used = parental
                    elif item[1] == 'Modes':
                        modes = ET.SubElement(info_elements, 'Text')
                        ET.SubElement(modes, "color").text = text_color
                        ET.SubElement(modes, "fontSize").text = '15'
                        ET.SubElement(modes, "text").text = '{CFG:Modes}'
                        last_used = modes
                    elif item[1] == 'InfoHintText':
                        break
                    elif item[1] == 'ItemText':
                        break
                    elif item[1] == 'Notes':
                        notes = ET.SubElement(info_elements, 'Text')
                        ET.SubElement(notes, "color").text = text_color
                        ET.SubElement(notes, "fontSize").text = '15'
                        ET.SubElement(notes, "text").text = '{CFG:Notes}'
                        last_used = notes
                    elif item[1] == 'StaticText':
                        static = ET.SubElement(info_elements, 'Text')
                        last_used = static
                    elif item[1] == 'Title':
                        title = ET.SubElement(info_elements, 'Text')
                        ET.SubElement(title, "color").text = text_color
                        ET.SubElement(title, "fontSize").text = '15'
                        ET.SubElement(title, "text").text = '{CFG:Title}'
                        last_used = title
                    elif item[1] == '#Media':
                        media = ET.SubElement(info_elements, 'Image', type='OPLM')
                        ET.SubElement(media, 'origin').text = 'Center'
                        ET.SubElement(media, 'source').text = '#Media'
                        last_used = media
                    elif item[1] == 'Vmode':
                        vmode = ET.SubElement(info_elements, 'Image', type="CFG")
                        ET.SubElement(vmode, 'origin').text = 'Center'
                        ET.SubElement(vmode, 'source').text = 'Vmode'
                        last_used = vmode
                    elif item[1] == 'Aspect':
                        aspect = ET.SubElement(info_elements, 'Image', type="CFG")
                        ET.SubElement(aspect, 'origin').text = 'Center'
                        ET.SubElement(aspect, 'source').text = 'Aspect'
                        last_used = aspect
                    elif item[1] == 'SCR2':
                        scr2 = ET.SubElement(info_elements, 'Image', {'type': 'SCR2'})
                        ET.SubElement(scr2, 'origin').text = 'Center'
                        has_height = True
                        has_width = True
                        possible_use = 'image'
                        last_used = scr2
                    elif item[1] == 'Rating':
                        rating = ET.SubElement(info_elements, 'Image', type="CFG")
                        ET.SubElement(rating, 'origin').text = 'Center'
                        ET.SubElement(rating, 'source').text = 'Rating'
                        possible_use = 'image'
                        last_used = rating
                    elif item[1] == 'Genre':
                        genre = ET.SubElement(info_elements, 'Text', type="CFG")
                        ET.SubElement(genre, "color").text = text_color
                        ET.SubElement(genre, "fontSize").text = '15'
                        ET.SubElement(genre, "text").text = '{CFG:Genre}'
                        last_used = genre
                    elif item[1] == 'Device':
                        device = ET.SubElement(info_elements, 'Image', type="CFG")
                        ET.SubElement(device, 'source').text = "Device"
                        ET.SubElement(device, 'origin').text = 'Center'
                        last_used = device
                    elif item[0] == 'x' and last_used is not None:
                        if int(item[1]) < 0:
                            new_x = str(self.width + int(item[1]))
                            ET.SubElement(last_used, 'x').text = new_x
                        else:
                            ET.SubElement(last_used, 'x').text = item[1]
                    elif item[0] == 'y' and last_used is not None:
                        if int(item[1]) < 0:
                            new_y = str(self.height + int(item[1]))
                            ET.SubElement(last_used, 'y').text = new_y
                        else:
                            ET.SubElement(last_used, 'y').text = item[1]
                    elif item[0] == 'width' and possible_use != 'image':
                        has_width = True
                        if item[1] == 'DIM_INF':
                            item[1] = str(int(self.width) / 2)
                            ET.SubElement(last_used, 'maxWidth').text = item[1]
                        elif item[1] != 'DIM_INF':
                            ET.SubElement(last_used, 'maxWidth').text = item[1]
                    elif item[0] == 'height' and possible_use != 'image':
                        has_height = True
                        if item[1] == 'DIM_INF':
                            item[1] = str(int(self.width) / 2)
                            ET.SubElement(last_used, 'maxHeight').text = item[1]
                        elif item[1] != 'DIM_INF':
                            ET.SubElement(last_used, 'maxHeight').text = item[1]
                    elif item[0] == 'height' and possible_use == 'image':
                        has_height = True
                        if item[1] == 'DIM_INF':
                            item[1] = str(int(self.width) / 2)
                            ET.SubElement(last_used, 'heightY').text = item[1]
                        elif item[1] != 'DIM_INF':
                            ET.SubElement(last_used, 'heightY').text = item[1]
                    elif item[0] == 'width' and possible_use == 'image':
                        has_width = True
                        if item[1] == 'DIM_INF':
                            item[1] = str(int(self.width) / 2)
                            ET.SubElement(last_used, 'widthX').text = item[1]
                        elif item[1] != 'DIM_INF':
                            ET.SubElement(last_used, 'widthX').text = item[1]
                    elif item[0] == 'default':
                        ET.SubElement(last_used, 'fallback').text = item[1]
                    elif item[0] == 'value':
                        ET.SubElement(last_used, 'text').text = item[1]
                        ET.SubElement(last_used, 'fontSize').text = '15'
                else:
                    if not has_height:
                        ET.SubElement(last_used, 'maxHeight').text = '25'
                    if not has_width:
                        ET.SubElement(last_used, 'maxWidth').text = '25'
                has_height = False
                has_width = False

                possible_use = None
                print '----'*30
        asd = print_elements(root)
        #print asd

        return root, reading


def print_elements(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")