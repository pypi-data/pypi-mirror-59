from django.contrib.auth.models import AnonymousUser
from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import APIPermissionModel
from .exceptions import APIPermissionException
import logging
import re


logger = logging.getLogger(__name__)


class APIPermCheckMiddleware(MiddlewareMixin):

    def process_request(self, request):
        path = request.path
        method = request.method
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        user = request.user or AnonymousUser()
        if request.user and header_token is not None:
            try:
                token = header_token.split(' ')
                token_obj = Token.objects.get(key=token[1])
                user = token_obj.user
            except Token.DoesNotExist as e:
                logger.warning(f"api_permission checker: bearer token invalid: {e}")
                raise APIPermissionException("Bearer Token invalid")
            except Exception as e:
                logger.warning(f"APIPermissionException : {e}")
                raise APIPermissionException(e)

        logger.debug(f"header_token is:{header_token} user: {user}, method: {method}, path: {path}")
        if not path.startswith('/admin/'):
            if not self._check_permission(path, user, method):
                res = JsonResponse({
                    'code': 1,
                    'msg': f'permission denied: user: {user}, method: {method}, path: {path}',
                }, status=status.HTTP_403_FORBIDDEN)
                return res

    def _check_permission(self, path, user, method):
        groups = user.groups.all()
        queryset = APIPermissionModel.objects.filter(group__in=groups, method__in=[method, APIPermissionModel.ALL], active=True)
        logger.debug(f'api permission queryset count: {queryset.count()}')
        for api in queryset:
            if re.match(api.pattern, path):
                if api.method in [APIPermissionModel.ALL, method]:
                    return True
                else:
                    logger.debug(f"permission denied: user: {user} api.method:{api.method}, method: {method}")
            else:
                logger.info(f"path not match: user: {user} api.pattern:{api.pattern}, path: {path}")
        return False
