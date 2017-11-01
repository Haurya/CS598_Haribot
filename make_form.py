import requests
import json
import os

def get_choices(fname):
    choices = []
    with open(fname, 'r') as f:
        for line in f:
            uid, username, submission = line.split('\t')
            submission = submission[:-1]
            choices.append(dict(label=submission))
    return choices

def get_form_info(choices=None, fname=None):
    access_token = "6sGwNcaLyVhhvG5mNc78otxLQBSEfnU38Edr71V6jhQB"
    api_key = '8945d7dba18726788a1c016661b9315c2bb81af4'

    title = 'CS598hs slack bot'

    q1 = "Enter NetID"
    q1d = {"type": "short_text", "question": q1, "required": True, "ref":"q1_ref"}

    q2 = "Select up to 3 responses to upvote"
    choices = choices or [dict(label='A'), dict(label='B')]
    q2d = {"type": "multiple_choice", "question": q2, "choices":choices, "required": True,
           "allow_multiple_selections": True, "randomize": True, "vertical_alignment": True}

    data = {'title': 'title', 'fields': [q1d, q2d]}
    str_data = json.dumps(data)

    cmd = 'curl -X POST https://api.typeform.io/v0.4/forms -H "X-API-TOKEN: 61b315aead2aac9be58448727f21ccdc" --data \'{}\''
    cmd = cmd.format(str_data)
    output = os.popen(cmd).read()
    output_json = json.loads(output)

    if fname:
        with open('./form_info.json', 'w') as f:
            json.dump(output_json, f)

    for links in output_json['_links']:
        if links['rel'] == u'form_render':
            main_link = links['href']

    return main_link, output_json

if __name__ == '__main__':
    choices = get_choices('./submissions.txt')
    user_form_link, form_info = get_form_info(choices=choices, fname='form.json')
    print user_form_link
