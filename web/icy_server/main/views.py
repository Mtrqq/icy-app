import flask

import icy_server.main.tasks as tasks
import classifier as img_classifier

main_blueprint = flask.Blueprint('main', __name__)


@main_blueprint.route('/')
def index():
    models_list = img_classifier.list_available_models()
    template_file = 'index.html.j2'
    return flask.render_template(template_file, models=models_list)


@main_blueprint.route('/classification', methods=['POST'])
def classify_image():
    image_url = flask.request.form["image_url"]
    selected_model = flask.request.form["model"]
    task_args = {
        'image_url': image_url,
        'model_name': selected_model,
        'stringify_labels': True
    }
    task_id = tasks.submit_task(img_classifier.recognize_image, **task_args)
    response_json = {
        'Status': 'Success',
        'Data': {
            'TaskID': task_id
        }
    }
    return response_json, 202


@main_blueprint.route('/classification/<task_id>', methods=['GET'])
def classification_status(task_id: str):
    jqueue = tasks.acquire_job_queue()
    task = jqueue.fetch_job(task_id)
    if task:
        return {
            'Status': "Success",
            'Data': {
                'Task': {
                    'ID': task.get_id(),
                    'Status': task.get_status(),
                    'Result': task.result,
                }
            }
        }
    else:
        return {'Status': "Failed"}
    
    
