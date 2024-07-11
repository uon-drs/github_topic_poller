import logging
import azure.functions as func
import os
from generate_jwt import generate_jwt, get_private_key_from_env, get_private_key_from_pem

app = func.FunctionApp()

@app.schedule(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if (is_dev := os.getenv("IS_DEV", "")) and is_dev.title() == "True":
        pem_path = os.getenv("PEM", "")
        private_key = get_private_key_from_pem(pem_path)
    else:
        private_key = get_private_key_from_env(env_key="PEM")

    if private_key is None:
        logging.error("Unable to locate private key in the environment or in PEM file.")
        exit()

    client_id = os.getenv("CLIENT_ID")
    if client_id is None:
        logging.error("CLIENT_ID must be set in the environment.")
        exit()

    jwt = generate_jwt(private_key, client_id)