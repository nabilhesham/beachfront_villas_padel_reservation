from home import variables


def global_variables(request):
    # Extract all variables from the variables.py file
    context = {key: value for key, value in vars(variables).items() if not key.startswith("__")}
    context['user'] = request.user
    return context