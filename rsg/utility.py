import textwrap


def debug_print(x, desc=None, debug=False):
    
    if not debug:
        return
    print "***" + desc + "=" + str(x) 

def wrapped_text(text):
    wrapper = textwrap.TextWrapper(initial_indent='* ', width= 60,
                                   break_long_words=True,
                                   break_on_hyphens=True)
    return wrapper.fill(text)

