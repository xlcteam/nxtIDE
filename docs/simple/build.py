#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
sys.path.append('../../nxtemu/')
sys.path.append('../../nxted/')
import yaml, re
import ConfigParser

from string import Template

LATEX_DOC_TEMPLATE = """
\\documentclass[10pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[Bjarne]{fncychap}                                                 
\\usepackage[parfill]{parskip}

\\title{$title}
\\author{$author}
\\date{}

\\begin{document}
\\maketitle
$text

\\end{document}
"""

LATEX_FUNCTION_TEMPLATE = """
\\vspace{6pt}
{\\bf $func}({\it $args}) 
$desc
$items 
"""

LATEX_ARGS_ITEMS_TEMPLATE = """
\\begin{quote}
    \\begin{description}
        $items
    \\end{description}
\\end{quote}

"""

LATEX_ARG_ITEMS_TEMPLATE = """
\\item[$name] ({\emph{$type}}) $desc
"""


def getAPI():
    """Returns a list of available functions for NXT brick. """
    
    out = {}
    
    api = __import__('api')

    for func in dir(api):
        if func[0].isupper():
            id = getattr(api, func)
            if type(id).__name__ == "function":
                lang = 'en'
                first = True
                tmp = {}
                for split in re.split('.*\.\. ((?:\/|)\[\w\w\]).*\\n', id.__doc__):
                    if ("[" in split and "]" in split) and first:
                        lang = split.replace('[', '').replace(']', '')
                        first = False
                    elif split is '\n':
                        continue
                    else:
                        if split[0:4] == '    ': 
                            split = split[4:]

                        tmp[lang] = split.replace('.. [/{0}]\n'.format(lang),
                                                    '')
                        first = True 


                out[func] = tmp

    return out

def getConstants():
    """Returns a list of constants for NXT brick. """
    
    out = []
    
    api = __import__('api')

    for constant in dir(api):
        if constant[0].isupper():
            id = getattr(api, constant)
            if type(id).__name__ not in ["function", "type"]:
                out.append(constant)

    return out



def exportYaml(fname='../nxted/help.yml', lang='en'):
    api = getAPI()

    for func,desc in api.iteritems():
        if desc.has_key(lang):
            api[func] = desc[lang].replace(':param ', '')
        else:
            api[func] = ''
        
    f = open(fname, 'w')
    f.write(yaml.dump(api, default_flow_style=False))
    f.close() 

    return fname

def exportIni(fname='../nxted/help.ini', lang='en'):
    config = ConfigParser.RawConfigParser(dict_type=dict, allow_no_value=True)
    config.optionxform = str
    api = getAPI()

    config.add_section('functions')

    for func,desc in api.iteritems():
        if desc.has_key(lang):
            desc[lang] = desc[lang].replace(':param ', '')
            desc[lang] = desc[lang].replace('    ', '\\t')
            desc[lang] = desc[lang].replace('\n', '\\n')

            config.set('functions', func, desc[lang])
        else:
            config.set('functions', func, '')
    
    with open(fname, 'wb') as configfile:
        config.write(configfile)

    return fname


def exportLatex(fname = 'reference.tex', lang='en'):
    api = getAPI()
    
    document_template = Template(LATEX_DOC_TEMPLATE)
    function_template = Template(LATEX_FUNCTION_TEMPLATE)
    args_template = Template(LATEX_ARG_ITEMS_TEMPLATE)
    arg_items_template = Template(LATEX_ARGS_ITEMS_TEMPLATE)
    
    funcs = ''

    for func,desc in api.iteritems():
        if desc.has_key(lang):
            args = desc[lang].split('\n')[0].split('(')[1][:-1]
            desc = desc[lang].split('\n')[1:]
            desc = '\n'.join(desc)
        else:
            args = ''
            desc = ''


        matches = re.findall(":param (.*?) (.*?): (.*)", desc)
        items = ''
        if matches != []:
            for match in matches:
                items += args_template.safe_substitute(name=match[1],
                                                       type=match[0],
                                                       desc=match[2])

        desc = re.sub(".*:param .*", '', desc)

        if items != '':
            generated_items  = arg_items_template.safe_substitute(items=items)
        else:
            generated_items = ''

        funcs += function_template.safe_substitute(func=func, 
                                                   args=args, 
                                                   desc=desc,
                                                   items=generated_items)

    document = document_template.safe_substitute(text=funcs, 
                                                title="nxtIDE reference manual",
                                                author="XLC Team")

    f = open(fname, 'w')
    f.write(document)
    f.close() 

    return fname




if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Please specify target:"
        print "\tini"
        print "\tlatex"
        print "\tyaml"
        print "\tconst"
        sys.exit()

    if sys.argv[1] == 'yaml':
        if len(sys.argv) > 2:
            file = exportYaml(*sys.argv[2:])
        else:
            file = exportYaml()

    elif sys.argv[1] == 'latex':
        if len(sys.argv) > 2:
            file = exportLatex(*sys.argv[2:])
        else:
            file = exportLatex()

    elif sys.argv[1] == 'ini':
        if len(sys.argv) > 2:
            file = exportIni(*sys.argv[2:])
        else:
            file = exportIni()



    elif sys.argv[1] == 'const':
        print getConstants()
        file = "<stdout>"



    else:
        print "Unknown format"
        sys.exit()

    print "Output written to ", file

   
