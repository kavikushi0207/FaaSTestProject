import json
import logging

import azure.functions as func

from matcher import calculate_match_scores, validate_match_request

app = func.FunctionApp()


@app.route(route="match", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def ResumeMatcher(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("NLP Match Calculation started.")

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON request body."}),
            status_code=400,
            mimetype="application/json",
        )

    validation_error = validate_match_request(req_body)
    if validation_error:
        return func.HttpResponse(
            json.dumps({"error": validation_error}),
            status_code=400,
            mimetype="application/json",
        )

    try:
        result = calculate_match_scores(req_body["resume"], req_body["jd"])
        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
        )
    except Exception as error:
        return func.HttpResponse(f"Error: {str(error)}", status_code=500)
