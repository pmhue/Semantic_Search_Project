def run_flow_and_get_url():
    # Register the flow
    flow_id = my_flow.register(project_name="my_project")

    # Create a flow run
    client = Client()
    flow_run = client.create_flow_run(flow_id=flow_id)

    # Construct the URL to the flow run in the Prefect UI
    prefect_ui_url = os.getenv("PREFECT_UI_URL", "https://app.prefect.io")
    flow_run_url = f"{prefect_ui_url}/flow-run/{flow_run.id}"

    return flow_run_url