import re
import ahocorasick
import html

def htmlify(content):
    if content == None or content == '':
        return ''

    A = ahocorasick.Automaton()

    keywords = ['ジョイ・ギルフォード', '897年', '983年', '9']
    for a in keywords:
        A.add_word(a, a)

    A.make_automaton()
    replace_items = []
    for end_index, original_value in A.iter(content):
        start_index = end_index - len(original_value) + 1
        print((start_index, end_index, original_value))
        replace_items.append((end_index + 1 - start_index, start_index))
    replace_items.sort(key=lambda x: (-x[0], x[1]))
    use = [False] * len(replace_items)
    fill = [False] * len(content)
    replace_items2 = []
    for i in range(len(replace_items)):
        start = replace_items[i][1]
        end = replace_items[i][1] + replace_items[i][0]
        ok = True
        for j in range(start, end):
            if fill[j]:
                ok = False
                break
        if ok:
            use[i] = True
            replace_items2.append((start, end))
            for j in range(start, end):
                fill[j] = True

    offset = 0
    for st, en in replace_items2:
        kw = content[offset+st:offset+en]
        url = 'http://example.com/' + kw
        link = "<a href=\"%s\">%s</a>" % (url, html.escape(kw))
        content = content[:offset+st] + link + content[offset+en:]
        offset += len(link) - len(kw)

    result = content

    return re.sub(re.compile("\n"), "<br />", content)

if __name__ == '__main__':
    content = "'ジョイ・ギルフォード'（''Joy Paul Guilford''、1897年 - 1983年）は、アメリカ合衆国の心理学者。"
    print(htmlify(content))
