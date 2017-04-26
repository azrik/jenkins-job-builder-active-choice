# Copyright 2016 Bulat Gaifullin
#
# This file is part of jenkins-job-builder-active-choice
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import glob
import os

from jenkins_jobs import parser
from jenkins_jobs.config import JJBConfig
from jenkins_jobs.registry import ModuleRegistry
from jenkins_jobs.xml_config import XmlJobGenerator

import pytest

class Scenario(object):
    def __init__(self, name, test_input, expected):
        self.name = name
        self.test_input = test_input
        self.expected = expected


def get_scenarios():
    fixtures_path = os.path.join(os.path.dirname(__file__), 'fixtures')
    scenarios = []
    for path in glob.iglob(os.path.join(fixtures_path, "*.yaml")):
            wo_ext = os.path.splitext(path)[0]
            scenarios.append(Scenario(os.path.basename(wo_ext), path, wo_ext + ".xml"))
    return scenarios


def generate_xml(fn):
    yaml_parser = parser.YamlParser(config)
    yaml_parser.parse(fn)

    yaml_registry = ModuleRegistry(config)
    yaml_registry.set_parser_data(yaml_parser.data)
    job_data_list, view_data_list = yaml_parser.expandYaml(yaml_registry)

    xml_generator = XmlJobGenerator(yaml_registry)
    xml_jobs = xml_generator.generateXML(job_data_list)
    assert 1 == len(xml_jobs), "Expected one job"

    return xml_jobs[0].output()


def load_xml(fn):
    with open(fn, "rb") as stream:
        return stream.read().encode("utf-8")


config = JJBConfig()
scenarios = get_scenarios()

@pytest.mark.parametrize("scenario", scenarios, ids=[x.name for x in scenarios])
def test_scenario(scenario):
    actual = generate_xml(scenario.test_input)
    expected = load_xml(scenario.expected)
    assert actual == expected, "check result xml"
