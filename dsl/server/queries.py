def concord_query_builder(query_file, **kwargs):
    """
    Execute a query on a CPG after a project has been loaded into joern.
    """
    if not kwargs:
        scala_params = "Map()"
    else:
        scala_params = _param_builder(kwargs.items())
    return f"cpg.runScript(\"{query_file}\", {scala_params})"


def _param_builder(params):
    """
    Receives an object and parses it into a Scala Map
    """
    _str = ""
    for k,v in params:
        _str += f"\"{k}\"->\"{v}\","
    # Remove last comma
    _str = _str[:-1]

    return f"Map({_str})"