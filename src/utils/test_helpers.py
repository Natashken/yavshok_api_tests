def assert_user_response_structure(response, expected_email=None, expected_age = None):

    if "body" in response:
        response_data = response["body"]
    else:
        response_data = response
    
    assert "user" in response_data
    user = response_data["user"]
    
    required_fields = {
        "id": int,
        "email": str,
        "name": str,
        "age": int
    }

    for field, expected_type in required_fields.items():
        assert field in user, f"Missing field: {field}"
        assert isinstance(user[field], expected_type), f"Field {field} should be {expected_type.__name__}, got {type(user[field]).__name__}"

    if expected_email:
        assert user["email"] == expected_email

    if expected_age:
        assert user["age"] == expected_age

def assert_validation_error_structure(response, field_name=None):

    if "body" in response:
        body = response["body"]
    else:
        body = response
    
    assert body.get("type") == "validation"
    assert body.get("on") == "body"
    assert "found" in body
    
    if field_name:
        assert field_name in body["found"]

def assert_auth_response_structure(response, expected_email=None, expected_age = None):
    
    if "body" in response:
        response_data = response["body"]
    else:
        response_data = response
    
    assert "token" in response_data
    assert "user" in response_data
    assert isinstance(response_data["token"], str)
    assert len(response_data["token"]) > 0
    
    assert_user_response_structure(response, expected_email, expected_age) 