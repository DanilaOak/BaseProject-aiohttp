PUBLIC_RESOURCES = (
    ('/api/v1/auth/login', ('POST',)),
    ('/api/version', ('GET',)),
    ('/api/v1/doc', ('GET',)),
)


def check_public_resources(path: str, method: str) -> bool:
    for resource, allowed_methods in PUBLIC_RESOURCES:
        if resource in path and method in allowed_methods:
            return True
    return False
