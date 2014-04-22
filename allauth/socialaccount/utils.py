
from .adapter import get_adapter

def get_next_redirect_url(request, redirect_field_name="next"):
    """
    Returns the next URL to redirect to, if it was explicitly passed
    via the request.
    """
    redirect_to = request.REQUEST.get(redirect_field_name)
    # light security check -- make sure redirect_to isn't garabage.
    if not redirect_to or "://" in redirect_to or " " in redirect_to:
        redirect_to = None
    return redirect_to


def get_login_redirect_url(request, url=None, redirect_field_name="next"):
    redirect_url \
        = (url
           or get_next_redirect_url(request,
                                    redirect_field_name=redirect_field_name)
           or get_adapter().get_login_redirect_url(request))
    return redirect_url

