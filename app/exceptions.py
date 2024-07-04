class AccessTokenExpired(Exception):
    """Raised when the access token is already expired"""
    pass


class RefreshTokenExpired(Exception):
    """Raised when the refresh token is already expired"""
    pass


class InvalidMeetingId(Exception):
    """Raised when invalid meeting id is passed"""
    pass


class InvalidMeetingTime(Exception):
    """Raised when invalid meeting time is passed"""
    pass


class ServiceUnavailable(Exception):
    """Raised when the service is unavailable"""
    pass


class ZohoErrorResponse(Exception):
    """Raised when the response from zoho is an error"""
    pass
