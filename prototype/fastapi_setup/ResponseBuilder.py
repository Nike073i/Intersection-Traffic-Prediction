from fastapi import status
from fastapi.responses import JSONResponse
from dataclasses import asdict

class ResponseBuilder:
    def __init__(self):
        self.data = dict()
        self.headers= dict()

    def set_data(self, data):
        if not data: return self
        data_dict = data if isinstance(data, dict) else asdict(data)
        self.data.update(data_dict)
        return self

    def set_status(self, status_code: int):
        self.status_code = status_code
        return self

    def set_message(self, message: str):
        self.message = message
        return self

    def set_details(self, details: str):
        self.details = details
        return self

    def set_header(self, key, value):
        self.headers[key]=value
        return self

    def build(self):
        if self.status_code >= 300:
            content = {
                "code": self.status_code,
                "message": self.message,
                "details": self.details,
                "data": self.data if len(self.data) else None
            }
        else:
            content = self.data

        content = {key: value for key, value in content.items() if value is not None}

        return JSONResponse(content=content, status_code=self.status_code, headers=self.headers)

    def ok(self, data=None):
        return self.set_status(status.HTTP_200_OK).set_data(data)

    def created(self, location=None):
        self.set_status(status.HTTP_201_CREATED)
        if location:
            self.set_data({"location": location})
            self.headers['location'] = location

        return self

    def not_found(self, details=None):
        return self.set_status(status.HTTP_404_NOT_FOUND).set_message("Not found").set_details(details)

    def bad_request(self, details=None):
        return self.set_status(status.HTTP_400_BAD_REQUEST).set_message("Bad Request").set_details(details)

    def unauthorized(self, details="Unauthorized access"):
        return self.set_status(status.HTTP_401_UNAUTHORIZED).set_message("Unauthorized").set_details(details)

    def forbidden(self, details="Forbidden"):
        return self.set_status(status.HTTP_403_FORBIDDEN).set_message("Forbidden").set_details(details)

    def internal_error(self, details="Internal server error"):
        return self.set_status(status.HTTP_500_INTERNAL_SERVER_ERROR).set_message("Internal Server Error").set_details(details)

    def custom(self, status_code, message, details=None):
        return self.set_status(status_code).set_message(message).set_details(details)