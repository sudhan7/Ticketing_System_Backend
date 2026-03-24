import json
import os
from django.http import JsonResponse
from issues.models import Issue, CriticalIssue, LowPriorityIssue, Reporter
from rest_framework.decorators import api_view

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ISSUES_FILE = os.path.join(BASE_DIR, 'issues.json')
REPORTERS_FILE = os.path.join(BASE_DIR, 'reporters.json')


def read_json(filepath):
    with open(filepath, 'r') as f:
        content = f.read().strip()
        return json.loads(content) if content else []


def write_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

@api_view(['GET'])
def get_reporters(request):
    try:
        reporters = read_json(REPORTERS_FILE)
        return JsonResponse(reporters, status=200, safe=False)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['GET'])
def get_reporter_by_id(request, reporter_id):
    try:
        reporters = read_json(REPORTERS_FILE)
        reporter = next((r for r in reporters if r['id'] == reporter_id), None)
        if reporter:
            return JsonResponse(reporter)
        return JsonResponse({'error': 'Reporter not found'}, safe=False)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['POST'])
def create_reporter(request):
    try:
        data = json.loads(request.body)
        reporter = Reporter(**data)
        reporter.validate()
        reporters = read_json(REPORTERS_FILE)
        reporters.append(reporter.to_dict())
        write_json(REPORTERS_FILE, reporters)
        return JsonResponse(reporter.to_dict(), status=201)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['POST'])
def create_issue(request):
    try:
        data = json.loads(request.body)
        priority = data.get('priority', 'medium')

        if priority == 'critical':
            issue = CriticalIssue(**data)
        elif priority == 'low':
            issue = LowPriorityIssue(**data)
        else:
            issue = Issue(**data)

        issue.validate()
        issues = read_json(ISSUES_FILE)
        issues.append(issue.to_dict())
        write_json(ISSUES_FILE, issues)

        response = issue.to_dict()
        response['describe'] = issue.describe()
        return JsonResponse(response, status=201)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['GET'])
def get_issues(request):
    try:
        issues = read_json(ISSUES_FILE)
        return JsonResponse(issues, safe=False)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['GET'])
def get_issue_by_id(request, issue_id):
    try:
        issues = read_json(ISSUES_FILE)
        issue = next((i for i in issues if i['id'] == issue_id), None)
        if issue:
            return JsonResponse(issue, safe=False)
        return JsonResponse({'error': 'Issue not found'}, safe=False)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['GET'])
def get_issues_by_status(request,status):
    try:
        issues = read_json(ISSUES_FILE)
        issues = [i for i in issues if i['status'] == status]
        return JsonResponse(issues, safe=False)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
