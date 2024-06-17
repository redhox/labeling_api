import os
import mlflow

mlflow.set_tracking_uri(os.getenv("MLFLOW_URL"))
os.environ['MLFLOW_TRACKING_USERNAME']=os.getenv("MLFLOW_USER")
os.environ['MLFLOW_TRACKING_PASSWORD']=os.getenv("MLFLOW_PASSWORD")
class MlflowConnect:

    def liste_mlflow():
        experiments_list = mlflow.search_experiments()
        liste_data=[]
        for experiment in experiments_list:
            runs=mlflow.search_runs(experiment_names=[experiment.name],output_format="list")
            for run in runs:
                data={'run_name':run.info._run_name,'run_id':run.info._run_id,'experiment_id':run.info._experiment_id,'path':f'/{run.info._experiment_id}/{run.info._run_id}/artifacts','metrics':run.data.metrics }
                liste_data.append(data)
        return liste_data
    
    def run_by_id(run_id):
        run = mlflow.get_run(run_id)
        data={'run_name':run.info._run_name,'run_id':run.info._run_id,'experiment_id':run.info._experiment_id,'path':f'/{run.info._experiment_id}/{run.info._run_id}/artifacts','metrics':run.data.metrics }
        return data
    
    def ping_mlflow_api():
        try:
            mlflow.search_experiments()
            print("mlflow connection up:")
        except Exception as e:
            print("mlflow connection fail:",str(e))
