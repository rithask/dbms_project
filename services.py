import requests
import json
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API endpoint
url = 'https://api.ktu.edu.in/ktu-web-service/anon/individualresult'


def fetch_result(register_no, dob, sem):
    # Get the semester details
    semester_details = get_semester_details(sem)

    # Data to be sent in the POST request
    data = {
        "registerNo": register_no,
        "dateOfBirth": dob,
        "examDefId": semester_details['examDefId'],
        "schemeId": semester_details['schemeId']
    }

    # Convert the data to JSON format
    json_data = json.dumps(data)

    # Set the headers
    headers = {'Content-Type': 'application/json'}

    # Send the POST request with SSL verification disabled
    response = requests.post(url, headers=headers, data=json_data, verify=False)

    return response

def get_semester_details(sem):
    data = {
        "s1": {
            "examDefId": "646",
            "schemeId": "1"
        },
        "s2": {
            "examDefId": "722",
            "schemeId": "1"
        },
        "s3": {
            "examDefId": "794",
            "schemeId": "1"
        },
        "s4": {
            "examDefId": "899",
            "schemeId": "1"
        }
    }

    return data.get(sem)

def purify_personal_details(data):
    full_name = data.get('fullName', '')
    result_name = data.get('resultName', '')
    institution_name = data.get('institutionName', '')
    register_no = data.get('registerNo', '')
    semester_name = data.get('semesterName', '')
    branch_name = data.get('branchName', '')

    return {
        'fullName': full_name,
        'resultName': result_name,
        'institutionName': institution_name,
        'registerNo': register_no,
        'semesterName': semester_name,
        'branchName': branch_name
    }

def purify_result_details(data):
    course_grades = []
    result_details = data.get('resultDetails', [])
    
    for detail in result_details:
        course_name = detail.get('courseName')
        grade_obtained = detail.get('gradeObtained')
        
        if course_name and grade_obtained:
            course_grades.append({
                'courseName': course_name,
                'gradeObtained': grade_obtained
            })
    
    return course_grades

# multiline comment
def purify_details(data):
    personal_details = purify_personal_details(data)
    result_details = purify_result_details(data)

    return {
        'personalDetails': personal_details,
        'resultDetails': result_details
    }

# open json file
with open('sample.json', 'r') as f:
    json_data = json.load(f)

    # Call the function to extract details
    extracted_data = purify_details(json_data)

    # print(extracted_data)

# Print the extracted details
# for key, value in extracted_data.items():
#     print(f"{key}: {value}")
