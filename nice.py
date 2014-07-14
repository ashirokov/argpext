



#def get_func_defaults(func):
#    "Populate D with the default values from the function"
#    D = {}
#    vs = func.__defaults__
#    if vs is not None and len(vs):
#        ns = func.__code__.co_varnames
#        offset = len(ns)-len(vs)
#        for i in range(offset,len(ns)):
#            name = ns[i]
#            value = vs[i-offset]
#            D[name] = value
#    return D
#
#def get_parser_defaults( populate, argument_default):
#    "Populate D with the default values from parser, except for those None."
#    D = {}
#
#    parser = argparse.ArgumentParser(argument_default=argument_default)
#
#    populate( parser )
#
#    # Populate the default values
#    for k,v in parser._option_string_actions.items():
#        if issubclass(type(v),argparse.Action):
#            if isinstance(v,argparse._HelpAction): continue
#            key = v.dest
#            value = v.default
#            D[key] = value
#
#    return D
#

