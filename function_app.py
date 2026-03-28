import azure.functions as func
import json
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = func.FunctionApp()

@app.route(route="match", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def ResumeMatcher(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('NLP Match Calculation started.')

    try:
        req_body = req.get_json()
        resume_text = req_body.get('resume')
        jd_text = req_body.get('jd')

        if not resume_text or not jd_text:
            return func.HttpResponse("Missing resume or jd text", status_code=400)

        # --- THE PERFORMANCE WORKLOAD ---
        # 1. Convert text to numerical vectors
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        
        # 2. Calculate Cosine Similarity
        match_percentage = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100

        return func.HttpResponse(
            json.dumps({
                "match_score": round(match_percentage, 2),
                "algorithm": "TF-IDF Cosine Similarity"
            }),
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

@app.route(route="MatchFunction", auth_level=func.AuthLevel.ANONYMOUS)
def MatchFunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )