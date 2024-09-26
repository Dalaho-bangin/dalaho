
import core.config as mem

def text_export(result):
    """
    exports results to a text file, one url per line
    """
    with open(mem.var['text_file'], 'a+', encoding='utf8') as text_file:
        for url in result:
            text_file.write(url+"\n")

def exporter(result):
    """
    main exporter function that calls other export functions
    """
    if len(result) !=0:
        text_export(result)
