from rest_framework.throttling import UserRateThrottle

class RegisterThrottle(UserRateThrottle):
    scope="registerthrottle"

    def get_cache_key(self, request, view):
        if request.user.is_authenticated or request.method == 'GET':
            return None

        return self.cache_format %{
            "scope":self.scope,
            "ident":self.get_ident(request)
        }