#!/usr/bin/env python
from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path
import sys
import os
import re

import jinja2


STARTER_PROJECT_DIR_PATH =  Path(__file__).parents[1]
STARTER_PROJECT_DIR = "starter-project"
STARTER_PROJECT_PATH = os.path.join(STARTER_PROJECT_DIR_PATH, STARTER_PROJECT_DIR)


def render_template(dir_path, filename, project):
    """ Load the starter project and render the project details """
    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(dir_path),
        undefined=jinja2.StrictUndefined,
        keep_trailing_newline=True,
    )

    loaded = environment.get_template(filename)

    rendered = loaded.render(project=project)

    return rendered


def write_file(file_path, contents):
    dir_name = os.path.dirname(file_path)
    os.makedirs(dir_name, exist_ok=True)
    with open(file_path, "w") as f:
        f.write(contents)


def parse_args(args):
    parser = ArgumentParser(description="dbt project starter")
    parser.add_argument(
        "--client",
        required=True,
        help="The name of the client you are creating this project for",
        type=check_snake_case,
    )
    parser.add_argument(
        "--warehouse",
        required=True,
        choices=["bigquery", "postgres", "redshift", "snowflake"],
        help="The warehouse your client is using",
    )
    parser.add_argument(
        "--target_dir",
        required=True,
        help="The target directory name. Note that the project will be created as a subdirectory within the target directory",
        type=check_file_path,
    )
    parser.add_argument(
        "--project_name",
        help="The name of your dbt project (as defined in dbt_project.yml). Defaults to <my_client>",
        type=check_snake_case,
    )
    parser.add_argument(
        "--project_directory",
        help="The name of your dbt project directory. Defaults to <my-client>-dbt",
        type=check_kebab_case,
    )
    parser.add_argument(
        "--profile_name",
        help="The name of the profile your dbt project will use. Defaults to <my_client>",
        type=check_snake_case,
    )

    parsed = parser.parse_args(args)
    return parsed


def handle(parsed):
    """ Checks that the arguments are valid, and returns a dictionary that
    describes the dbt project
    """

    kebab_case_client = parsed.client.replace("_", "-")

    project = {}

    project["client_name"] = parsed.client
    project["warehouse"] = parsed.warehouse
    project["name"] = parsed.project_name or parsed.client
    project["dir_path"] = parsed.target_dir
    project["dir_name"] = parsed.project_directory or "{}-dbt".format(kebab_case_client)
    project["profile_name"] = parsed.profile_name or parsed.client

    return project


def check_snake_case(s):
    if re.match("^[a-z0-9_]*$", s) is None:
        raise ArgumentTypeError(
            "{} should only contain lower case letters, numbers, and underscores.".format(
                s
            )
        )
    return s


def check_kebab_case(s):
    if re.match("^[a-z0-9-]*$", s) is None:
        raise ArgumentTypeError(
            "{} should only contain lower case letters, numbers, and hyphens.".format(s)
        )
    return s


def check_file_path(s):
    if not os.path.exists(s):
        raise ArgumentTypeError("Target directory {} does not exist!".format(s))
    return s


def should_copy_file(base_name, contents):
    is_empty_file = contents.strip() == ""
    if base_name == ".gitkeep" or not is_empty_file:
        return True


def create_starter_project(project):
    # set the path we are targeting
    client_project_path = os.path.join(project["dir_path"], project["dir_name"])
    # for each file in the starter project, copy a rendered version of the file
    for subdir, dirs, files in os.walk(STARTER_PROJECT_PATH):
        if os.path.basename(subdir) != '__pycache__':
            for base_name in files:
                rendered_template = render_template(subdir, base_name, project)
                if should_copy_file(base_name, rendered_template):
                    target_dir = subdir.replace(STARTER_PROJECT_PATH, client_project_path)
                    target_filepath = os.path.join(target_dir, base_name)
                    write_file(target_filepath, rendered_template)

    print(
        "New dbt project for {} created at {}! 🎉".format(
            project["client_name"], client_project_path
        )
    )


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parsed = parse_args(args)

    project = handle(parsed)

    create_starter_project(project)


if __name__ == "__main__":
    main()
