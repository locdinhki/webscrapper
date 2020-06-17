search_texts = ["<-Prev","|TOC|","on Twitter","Table of Content","Like Loading..."]
def clean(x):
    dirty_texts = []
    i = 0
    while i < len(x):
        for a in search_texts:
            if a in x[i]:
                dirty_texts.append(x[i])
            #x[1].split("<-Prev", 1)[0].strip()
        i += 1
    for dirty_text in dirty_texts:
        try:
            x.remove(dirty_text)
        except:
            continue
    return x