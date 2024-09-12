

def user_info(request):
    """Context processor to provide user information globally."""
    if request.user.is_authenticated:  # Check if the user is logged in
        return {
            # This will be available as {{ user_full_name }} in templates
            'user_full_name': request.user.full_name,
            # This will be available as {{ user_email }} in templates
            'user_email': request.user.email,
            # This will be available as {{ user_profile_pic }} in templates
            'user_profile_pic': request.user.profile_pic,
        }
    return {}  # Return an empty dictionary if the user is not logged in
