from fastapi import HTTPException
import configuration


class ExpirationValidator:
    def __init__(self, token_payload: dict):
        self.token_payload = token_payload
        self.maximum_time_to_live = configuration.MAXIMUM_TIME_TO_LIVE

    def validate_expiration(self) -> bool:
        """Checks if the time to live exceed the amount configured.
        The configuration can be changed the configuration.py file.
        """
        if self.token_payload["exp"] - self.token_payload["iat"] > self.maximum_time_to_live:
            raise HTTPException(
                status_code=422, detail=f"Invalid exp. The certificate could not be validated. The token's time to live exceeds the maximum time to live allowed ({self.maximum_time_to_live})")
        return True
