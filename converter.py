import os
import sys
import xml.etree.ElementTree as ET
from enum import Enum

if len(sys.argv) == 1:
    raise NameError('No lint file specified')

if not os.path.isfile(sys.argv[1]):
    raise IOError('Invalid file specified')

RUNNER_WORKSPACE = os.environ['RUNNER_WORKSPACE']
REPO_NAME = os.environ['GITHUB_REPOSITORY'].split('/')[1]

checkstyle = ET.Element('checkstyle')
checkstyle.attrib['version'] = '8.0'

class StrEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class SeverityLevel(StrEnum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


for issue in ET.parse(sys.argv[1]).getroot().iter('issue'):
    file = ET.SubElement(checkstyle, 'file')

    if '.gradle/caches' in issue[0].attrib['file']:
        continue

    file.attrib['name'] = issue[0].attrib['file'].replace(f'{RUNNER_WORKSPACE}/{REPO_NAME}/', '')

    error = ET.SubElement(file, 'error')

    if 'line' in issue[0].attrib:
        error.attrib['line'] = issue[0].attrib['line']
    else:
        error.attrib['line'] = str(0)

    if 'column' in issue[0].attrib:
        error.attrib['column'] = issue[0].attrib['column']
    else:
        error.attrib['column'] = str(0)

    if 'severity' in issue.attrib:
        input_error_level = sys.argv[2].upper()

        if sys.argv[2] == '' or input_error_level == SeverityLevel.ERROR:
            error.attrib['severity'] = issue.attrib['severity']
        else:
            issue_error_level = issue.attrib['severity'].upper()

            if SeverityLevel.WARNING == input_error_level and (issue_error_level == SeverityLevel.WARNING or issue_error_level == SeverityLevel.ERROR):
                error.attrib['severity'] = 'error'
            else:
                error.attrib['severity'] = 'error'
    else:
        error.attrib['severity'] = 'info' 

    issueId = issue.attrib['id']
    message = issue.attrib['message']
    error.attrib['message'] = f'{issueId}: {message}'

checkStyleFile = ET.ElementTree(checkstyle)
checkStyleFile.write('output_checkstyle.xml')
