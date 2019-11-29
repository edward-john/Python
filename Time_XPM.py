import requests
import sys
from datetime import datetime
from xpm_config import API, APIKEY, ACCOUNTKEY, POST_TIME

def htmlpost(main_tag,param):
    """Function: Compile dictionary into html format"""
    head = f'<{main_tag}>'
    body = ''.join([f'<{i}>{param[i]}</{i}>' for i in param])
    foot = f'</{main_tag}>'
    return head + body + foot

def add(task, minutes, note):
    """Add time entry to XPM"""
    date = datetime.now().strftime('%Y%m%d')
    staff_id = str(32535)
    tasks = ['733095','733094','733102'] #GOA,Emails,TeaBreak
    parameters = {'Job':'J000794','Date':date,'Staff':staff_id}
    parameters['Task'] = tasks[task-1]
    parameters['Minutes'] = minutes
    parameters['Note'] = note
    data = htmlpost('Timesheet',parameters)
    requests.post(url=POST_TIME,data=data)
    print('Successfully added to XPM time entry')

if __name__ == '__main__':
    globals()[sys.argv[1]](int(sys.argv[2]), sys.argv[3], sys.argv[4])

