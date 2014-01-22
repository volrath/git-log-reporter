import subprocess

from flask import Flask, jsonify, request

app = Flask('__name__')
app.debug = True

GIT_REPOS_PATH = '/path/to/projects/'

GIT_COMMIT_FIELDS = ['id', 'author_name', 'author_email', 'date', 'message']
GIT_LOG_FORMAT = ['%H', '%an', '%ae', '%ad', '%s']
GIT_LOG_FORMAT = '%x1f'.join(GIT_LOG_FORMAT) + '%x1e'


@app.route('/', methods=['POST'])
def report():
    """Returns a json response with `git log` information data."""
    if not request.json.get('repos'):
        return 'invalid request', 400

    GIT_COMMAND = 'git log --format="{}"'.format(GIT_LOG_FORMAT)
    for key, value in request.json.get('options', {}).iteritems():
        GIT_COMMAND += ' --{}="{}"'.format(key, value)

    response = {}
    for repo in request.json['repos']:
        command = 'cd {}{} ; {}'.format(GIT_REPOS_PATH, repo, GIT_COMMAND)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            continue
        # dict the output
        output = output.strip('\n\x1e').split("\x1e")
        output = [row.strip().split("\x1f") for row in output]
        # add the commits to the response
        response[repo] = [dict(zip(GIT_COMMIT_FIELDS, row)) for row in output]

    return jsonify(response)


if __name__ == "__main__":
    app.run()
