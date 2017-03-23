from unittest.mock import Mock, patch
# --------------------------
# Shakespeare API Constants
# --------------------------

SHAKESPEARE_NO_PERSON_RESPONSE = {
  "detail": "Unable to find a contact by that email."
}


# ---
# Mock Requests Response
# ---

# Thanks https://gist.github.com/evansde77/45467f5a7af84d2a2d34f3fcb357449c
def _mock_response(
        self,
        status=200,
        json_data=None,
        raise_for_status=None):
    """
    since we typically test a bunch of different
    requests calls for a service, we are going to do
    a lot of mock responses, so its usually a good idea
    to have a helper function that builds these things
    """
    mock_resp = Mock()
    # mock raise_for_status call w/optional error
    mock_resp.raise_for_status = Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    # set status code and content
    mock_resp.status_code = status
    # add json data if provided
    if json_data:
        mock_resp.json = Mock(
            return_value=json_data
        )
    return mock_resp
    