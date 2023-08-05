import os
import sys
import click
from pkg_resources import get_distribution

from demisto_sdk.core import DemistoSDK
from demisto_sdk.runners.runner import Runner
from demisto_sdk.common.tools import print_error
from demisto_sdk.yaml_tools.unifier import Unifier
from demisto_sdk.dev_tools.uploader import Uploader
from demisto_sdk.dev_tools.initiator import Initiator
from demisto_sdk.yaml_tools.extractor import Extractor
from demisto_sdk.common.configuration import Configuration
from demisto_sdk.dev_tools.lint_manager import LintManager
from demisto_sdk.validation.secrets import SecretsValidator
from demisto_sdk.runners.playbook_runner import PlaybookRunner
from demisto_sdk.validation.file_validator import FilesValidator
from demisto_sdk.yaml_tools.update_script import ScriptYMLFormat
from demisto_sdk.yaml_tools.content_creator import ContentCreator
from demisto_sdk.yaml_tools.update_playbook import PlaybookYMLFormat
from demisto_sdk.json_to_outputs.json_to_outputs import json_to_outputs
from demisto_sdk.yaml_tools.update_integration import IntegrationYMLFormat
from demisto_sdk.common.constants import SCRIPT_PREFIX, INTEGRATION_PREFIX

from demisto_sdk.test_playbook_generator.test_playbook_generator import TestPlaybookGenerator

pass_config = click.make_pass_decorator(DemistoSDK, ensure=True)


@click.group(invoke_without_command=True, no_args_is_help=True, context_settings=dict(max_content_width=100), )
@click.help_option(
    '-h', '--help'
)
@click.option(
    '-d', '--env-dir', help='Specify a working directory.'
)
@click.option(
    '-v', '--version', help='Get the demisto-sdk version.',
    is_flag=True, default=False, show_default=True
)
@pass_config
def main(config, version, env_dir):
    config.configuration = Configuration()
    if version:
        version = get_distribution('demisto-sdk').version
        print(version)

    if env_dir:
        config.configuration.env_dir = env_dir


# ====================== extract ====================== #
@main.command(name="split-yml",
              short_help="Split the code, image and description files from a Demisto integration or script yaml file "
                         " to multiple files(To a package format - "
                         "https://demisto.pan.dev/docs/package-dir).")
@click.help_option(
    '-h', '--help'
)
@click.option(
    '--infile', '-i',
    help='The yml file to extract from',
    required=True
)
@click.option(
    '--outfile', '-o',
    required=True,
    help="The output dir to write the extracted code/description/image to."
)
@click.option(
    '--yml-type', '-y',
    help="Yaml type. If not specified will try to determine type based upon path.",
    type=click.Choice([SCRIPT_PREFIX, INTEGRATION_PREFIX])
)
@click.option(
    '--no-demisto-mock',
    help="Don't add an import for demisto mock.",
    is_flag=True,
    show_default=True
)
@click.option(
    '--no-common-server',
    help="Don't add an import for CommonServerPython."
         "If not specified will import unless this is CommonServerPython",
    is_flag=True,
    show_default=True
)
@pass_config
def extract(config, **kwargs):
    extractor = Extractor(configuration=config.configuration, **kwargs)
    return extractor.extract_to_package_format()


# ====================== extract-code ====================== #
@main.command(name="extract-code",
              short_help="Extract code from a Demisto integration or script yaml file.")
@click.help_option(
    '-h', '--help'
)
@click.option(
    '--infile', '-i',
    help='The yml file to extract from',
    required=True
)
@click.option(
    '--outfile', '-o',
    required=True,
    help="The output file to write the code to"
)
@click.option(
    '--yml-type', '-y',
    help="Yaml type. If not specified will try to determine type based upon path.",
    type=click.Choice([SCRIPT_PREFIX, INTEGRATION_PREFIX])
)
@click.option(
    '--no-demisto-mock',
    help="Don't add an import for demisto mock, false by default",
    is_flag=True,
    show_default=True
)
@click.option(
    '--no-common-server',
    help="Don't add an import for CommonServerPython."
         "If not specified will import unless this is CommonServerPython",
    is_flag=True,
    show_default=True
)
@pass_config
def extract_code(config, **kwargs):
    extractor = Extractor(configuration=config.configuration, **kwargs)
    return extractor.extract_code(kwargs['outfile'])


# ====================== unify ====================== #
@main.command(name="unify",
              short_help='Unify code, image, description and yml files to a single Demisto yml file.')
@click.option(
    "-i", "--indir", help="The path to the files to unify", required=True
)
@click.option(
    "-o", "--outdir", help="The output dir to write the unified yml to", required=True
)
def unify(**kwargs):
    unifier = Unifier(**kwargs)
    return unifier.merge_script_package_to_yml()


# ====================== validate ====================== #
# TODO: add a configuration for conf.json and id_set.json
@main.command(name="validate",
              short_help='Validate your content files.')
@click.help_option(
    '-h', '--help'
)
@click.option(
    '-j', '--conf-json', is_flag=True,
    default=False, show_default=True, help='Validate the conf.json file.')
@click.option(
    '-i', '--id-set', is_flag=True,
    default=False, show_default=True, help='Create the id_set.json file.')
@click.option(
    '--prev-ver', help='Previous branch or SHA1 commit to run checks against.')
@click.option(
    '--post-commit', is_flag=True, help='Whether the validation is done after you committed your files, '
                                        'this will help the command to determine which files it should check in its '
                                        'run. Before you commit the files it should not be used. Mostly for build '
                                        'validations.')
@click.option(
    '--no-backward-comp', is_flag=True, show_default=True,
    help='Whether to check backward compatibility or not.')
@click.option(
    '-g', '--use-git', is_flag=True, show_default=True,
    default=False, help='Validate changes using git - this will check your branch changes and will run only on them.')
@click.option(
    '-p', '--path', help='Path of file to validate specifically.'
)
@pass_config
def validate(config, **kwargs):
    sys.path.append(config.configuration.env_dir)

    file_path = kwargs['path']

    if file_path and not os.path.isfile(file_path):
        print_error(F'File {file_path} was not found')
        return 1
    else:
        validator = FilesValidator(configuration=config.configuration,
                                   is_backward_check=not kwargs['no_backward_comp'],
                                   is_circle=kwargs['post_commit'], prev_ver=kwargs['prev_ver'],
                                   validate_conf_json=kwargs['conf_json'], use_git=kwargs['use_git'],
                                   file_path=kwargs.get('path'))
        return validator.run()


# ====================== create ====================== #
@main.command(name="create-content-artifacts",
              short_help='Create content artifacts. This will generate content_new.zip file which can be used to '
                         'upload to your server in order to upload a whole new content version to your Demisto '
                         'instance.')
@click.help_option(
    '-h', '--help'
)
@click.option(
    '-a', '--artifacts_path', help='The path of the directory in which you want to save the created content artifacts')
@click.option(
    '-p', '--preserve_bundles', is_flag=True, default=False, show_default=True,
    help='Keep the bundles created in the process of making the content artifacts')
def create(**kwargs):
    content_creator = ContentCreator(**kwargs)
    return content_creator.run()


# ====================== secrets ====================== #
@main.command(name="secrets",
              short_help="Run Secrets validator to catch sensitive data before exposing your code to public repository."
                         " Attach path to whitelist to allow manual whitelists. Default file path to secrets is "
                         "'./Tests/secrets_white_list.json' ")
@click.help_option(
    '-h', '--help'
)
@click.option(
    '--post-commit', is_flag=True, show_default=True,
    help='Whether the secretes is done after you committed your files, '
         'this will help the command to determine which files it should check in its '
         'run. Before you commit the files it should not be used. Mostly for build '
         'validations.')
@click.option(
    '-wl', '--whitelist', default='./Tests/secrets_white_list.json', show_default=True,
    help='Full path to whitelist file, file name should be "secrets_white_list.json"')
@pass_config
def secrets(config, **kwargs):
    sys.path.append(config.configuration.env_dir)
    secrets = SecretsValidator(configuration=config.configuration, is_circle=kwargs['post_commit'],
                               white_list_path=kwargs['whitelist'])
    return secrets.run()


# ====================== lint ====================== #
@main.command(name="lint",
              short_help="Run lintings (flake8, mypy, pylint, bandit) and pytest. pylint and pytest will run within the"
                         "docker image of an integration/script. Meant to be used with integrations/scripts that use "
                         "the folder (package) structure. Will lookup up what docker image to use and will setup the "
                         "dev dependencies and file in the target folder. ")
@click.help_option(
    '-h', '--help'
)
@click.option(
    "-d", "--dir", help="Specify directory of integration/script")
@click.option(
    "--no-pylint", is_flag=True, help="Do NOT run pylint linter")
@click.option(
    "--no-mypy", is_flag=True, help="Do NOT run mypy static type checking")
@click.option(
    "--no-flake8", is_flag=True, help="Do NOT run flake8 linter")
@click.option(
    "--no-bandit", is_flag=True, help="Do NOT run bandit linter")
@click.option(
    "--no-test", is_flag=True, help="Do NOT test (skip pytest)")
@click.option(
    "-r", "--root", is_flag=True, help="Run pytest container with root user")
@click.option(
    "-k", "--keep-container", is_flag=True, help="Keep the test container")
@click.option(
    "-v", "--verbose", is_flag=True, help="Verbose output - mainly for debugging purposes")
@click.option(
    "--cpu-num",
    help="Number of CPUs to run pytest on (can set to `auto` for automatic detection of the number of CPUs)",
    default=0)
@click.option(
    "-p", "--parallel", is_flag=True, help="Run tests in parallel")
@click.option(
    "-m", "--max-workers", type=int, help="How many threads to run in parallel")
@click.option(
    "-g", "--git", is_flag=True, help="Will run only on changed packages")
@click.option(
    "-a", "--run-all-tests", is_flag=True, help="Run lint on all directories in content repo")
@pass_config
def lint(config, dir, **kwargs):
    linter = LintManager(configuration=config.configuration, project_dir_list=dir, **kwargs)
    return linter.run_dev_packages()


# ====================== format ====================== #
@main.command(name="format",
              short_help="Run formatter on a given script/playbook/integration yml file. ")
@click.help_option(
    '-h', '--help'
)
@click.option(
    "-t", "--file-type", type=click.Choice(["integration", "script", "playbook"]),
    help="The type of yml file to be formatted.", required=True)
@click.option(
    "-s", "--source-file", help="The path of the script yml file", required=True)
@click.option(
    "-o", "--output-file-name", help="The path where the formatted file will be saved to")
def format_yml(file_type, **kwargs):
    file_type_and_linked_class = {
        'integration': IntegrationYMLFormat,
        'script': ScriptYMLFormat,
        'playbook': PlaybookYMLFormat
    }
    if file_type in file_type_and_linked_class:
        format_object = file_type_and_linked_class[file_type](**kwargs)
        return format_object.format_file()

    return 1


@main.command(name="upload",
              short_help="Upload integration to Demisto instance. DEMISTO_BASE_URL environment variable should contain"
                         " the Demisto server base URL. DEMISTO_API_KEY environment variable should contain a valid "
                         "Demisto API Key.")
@click.help_option(
    '-h', '--help'
)
@click.option(
    "-i", "--path", help="The path of an integration file or a package directory to upload", required=True)
@click.option(
    "--insecure", help="Skip certificate validation", is_flag=True)
@click.option(
    "-v", "--verbose", help="Verbose output", is_flag=True)
def upload(**kwargs):
    uploader = Uploader(**kwargs)
    return uploader.upload()


@main.command(name="run",
              short_help="Run integration command on remote Demisto instance in the playground. DEMISTO_BASE_URL "
                         "environment variable should contain the Demisto base URL. DEMISTO_API_KEY environment "
                         "variable should contain a valid Demisto API Key.")
@click.help_option(
    '-h', '--help'
)
@click.option(
    "-q", "--query", help="The query to run", required=True)
@click.option(
    "-k", "--insecure", help="Skip certificate validation", is_flag=True)
@click.option(
    "-v", "--verbose", help="Verbose output", is_flag=True)
@click.option(
    "-D", "--debug", help="Whether to enable the debug-mode feature or not, if you want to save the output file "
                          "please use the --debug-path option", is_flag=True)
@click.option(
    "--debug-path", help="The path to save the debug file at, if not specified the debug file will be printed to the "
                         "terminal")
def run(**kwargs):
    runner = Runner(**kwargs)
    return runner.run()


# ====================== run-playbook ====================== #
@main.command(name="run-playbook",
              short_help="Run a playbook in Demisto. "
                         "DEMISTO_API_KEY environment variable should contain a valid Demisto API Key. "
                         "Example: DEMISTO_API_KEY=<API KEY> demisto-sdk run-playbook -p 'p_name' -u "
                         "'https://demisto.local'.")
@click.help_option(
    '-h', '--help'
)
@click.option(
    '--url', '-u',
    help='URL to a Demisto instance. You can also specify the URL as an environment variable named: DEMISTO_BASE_URL'
)
@click.option(
    '--playbook_id', '-p',
    help="The playbook ID to run.",
    required=True
)
@click.option(
    '--wait', '-w', is_flag=True,
    help="Wait until the playbook run is finished and get a response."
)
@click.option(
    '--timeout', '-t',
    default=90,
    show_default=True,
    help="Timeout for the command. The playbook will continue to run in Demisto"
)
def run_playbook(**kwargs):
    playbook_runner = PlaybookRunner(**kwargs)
    return playbook_runner.run_playbook()


@main.command(name="json-to-outputs",
              short_help='''Demisto integrations/scripts have a YAML file that defines them.
Creating the YAML file is a tedious and error-prone task of manually copying outputs from the API result to the
file/UI/PyCharm. This script auto generates the YAML for a command from the JSON result of the relevant API call.''')
@click.help_option(
    '-h', '--help'
)
@click.option(
    "-c", "--command", help="Command name (e.g. xdr-get-incidents)", required=True)
@click.option(
    "-i", "--infile", help="Valid JSON file path. If not specified then script will wait for user input in the "
                           "terminal", required=False)
@click.option(
    "-p", "--prefix", help="Output prefix like Jira.Ticket, VirusTotal.IP, the base path for the outputs that the "
                           "script generates", required=True)
@click.option(
    "-o", "--outfile", help="Output file path, if not specified then will print to stdout", required=False)
@click.option(
    "-v", "--verbose", is_flag=True, help="Verbose output - mainly for debugging purposes")
@click.option(
    "--interactive", help="If passed, then for each output field will ask user interactively to enter the "
                          "description. By default is interactive mode is disabled", is_flag=True)
def json_to_outputs_command(**kwargs):
    json_to_outputs(**kwargs)


# ====================== generate-test-playbook ====================== #
@main.command(name="generate-test-playbook",
              short_help="Generate test playbook from integration or script")
@click.help_option(
    '-h', '--help'
)
@click.option(
    '-i', '--infile',
    required=True,
    help='Specify integration/script yml path')
@click.option(
    '-o', '--outdir',
    required=False,
    help='Specify output directory')
@click.option(
    '-n', '--name',
    required=True,
    help='Specify test playbook name')
@click.option(
    '-t', '--file-type', default='integration',
    type=click.Choice(["integration", "script"]),
    required=False,
    help='Specify integration or script. The default is integration')
@click.option(
    '--no-outputs', is_flag=True,
    help='Skip generating verification conditions for each output contextPath. Use when you want to decide which '
         'outputs to verify and which not')
@click.option(
    "-v", "--verbose", help="Verbose output for debug purposes - shows full exception stack trace", is_flag=True)
def generate_test_playbook(**kwargs):
    generator = TestPlaybookGenerator(**kwargs)
    generator.run()


# ====================== init ====================== #
@main.command(name="init", short_help="Initiate a new Pack, Integration or Script."
                                      " If the script/integration flags are not present"
                                      " then we will create a pack with the given name."
                                      " Otherwise when using the flags we will generate"
                                      " a script/integration based on your selection.")
@click.help_option(
    '-h', '--help'
)
@click.option(
    "-n", "--name", help="The name of the directory and file you want to create")
@click.option(
    "--id", help="The id used in the yml file of the integration or script"
)
@click.option(
    "-o", "--output-dir", help="The output dir to write the object into. The default one is the current working "
                               "directory.")
@click.option(
    '--integration', is_flag=True, help="Create an Integration based on HelloWorld example")
@click.option(
    '--script', is_flag=True, help="Create a script based on HelloWorldScript example")
@click.option("--pack", is_flag=True, help="Create pack and its sub directories")
def init(**kwargs):
    initiator = Initiator(**kwargs)
    initiator.init()
    return 0


@main.resultcallback()
def exit_from_program(result=0, **kwargs):
    sys.exit(result)

# todo: add download from demisto command


def demisto_sdk_cli():
    main()


if __name__ == '__main__':
    sys.exit(main())
