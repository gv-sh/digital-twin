"""Auth, logging, rate limiting middleware."""


def auth_middleware(request):
    """Authentication middleware (stub)."""
    return True


def logging_middleware(request):
    """Logging middleware (stub)."""
    print(f"Request: {request}")


__all__ = ["auth_middleware", "logging_middleware"]
