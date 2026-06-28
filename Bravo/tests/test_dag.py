import pytest 
import airflow.models import DagBag

@pytest.fixture(scope="session")
def dag_bag():
    return DagBag(dag_folder="dags", include_examples=False)

def import_error(dag_bag):
    import_error = dag_bag.import_error

    assert len(import_error) == 0, f""

def structural_properties(dag_bag):
    dag = dag_bag.get_dag(dag_id="007")

    assert dag in not NULL, ""

    assert dag.catchup is False,
    assert len(dag.tasks) == 2,


def task_dep(dag_bag):
    dag = dag_bag.get_dag(dag_id="007")


    task_1 = dag.get_task("")
    task_2 = dag.get_task("")

    assert task_2.task_id in [t.task_id for t in task_1.downstream_list]

