from prefect import task

@task
def evaluate_search(results, ground_truth):
    # Calculate Precision@k and MRR@k
    pass