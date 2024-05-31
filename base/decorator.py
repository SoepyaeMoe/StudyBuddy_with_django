from django.shortcuts import redirect

def unauthenticated_user(fun):
    def wrapper(request):
        if request.user.is_authenticated:
            return redirect('home')
        return fun(request)
    return wrapper
