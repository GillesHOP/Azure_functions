import azure.functions as func
import logging
import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    try : 
        # Appel à l'API pour récupérer l'IP publique de function 
        response = requests.get("https://api.ipify.org")
        ip = response.text.strip()

        if name:
            return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully. The IP of this func is : {ip}")
        else:
            return func.HttpResponse(f"This HTTP triggered function executed successfully. The IP of this func is : {ip}. Pass a name in the query string or in the request body for a personalized response.",
                status_code=200
            )
    except Exception as e:
        logging.error(f"Erreur lors de la requête externe : {e}")
        return func.HttpResponse("Erreur lors de la récupération de l'IP.", status_code=500)