#!/usr/bin/env python
"""
package_container

functions for building the initial docker container
templates for docker-image command

"""
import sys
import os
import json
import pystache

from cirrus.logger import get_logger
from cirrus.templates import find_template
from cirrus.utils import working_dir
from cirrus.configuration import load_configuration
from cirrus.git_tools import (
    commit_files_optional_push,
    checkout_and_pull,
    has_unstaged_changes
)

LOGGER = get_logger()


def make_executable(path, repo):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2    # copy R bits to X
    os.chmod(path, mode)


def write_basic_dockerfile(opts, config, path):
    """
    write the basic dockerfile for the example/template

    """
    LOGGER.info("writing Dockerfile {}".format(path))
    template = find_template("Dockerfile.mustache")
    context = {
        'open_brace': '{{',
        'close_brace': '}}',
        'package': config.package_name(),
        'container': opts.container,
        'entrypoint': opts.entrypoint,
        'maintainer': config.author_email()
        }
    renderer = pystache.Renderer()
    result = renderer.render_path(template, context)
    with open(path, 'w') as handle:
        handle.write(result)


def write_json_file(path, data):
    """write json data to a file"""
    LOGGER.info("writing JSON {}".format(path))
    with open(path, 'w') as handle:
        json.dump(data, handle)


def write_script(repo, path, content, **extras):
    """write script content to a file"""
    LOGGER.info("writing script {}".format(path))

    script = content.format(**extras)
    with open(path, 'w') as handle:
        handle.write(script)
    # run chmod +x on new script
    make_executable(path, repo)


def edit_cirrus_conf(opts, config):
    """
    add docker settings to cirrus conf

    """
    LOGGER.info("updating cirrus.conf docker section...")
    config.add_docker_settings(
        opts.template_dir,
        opts.context_file,
        opts.image_dir,
        opts.docker_registry
    )


def init_container(opts):
    """
    Initialise a basic container-template setup
    for this package
    """
    cirrus_conf = os.path.join(opts.repo, 'cirrus.conf')
    if not os.path.exists(cirrus_conf):
        msg = "No cirrus.conf found, need to init repo first?"
        LOGGER.error(msg)
        sys.exit(1)

    config = load_configuration(opts.repo)
    template_dir = os.path.join(opts.repo, opts.template_dir)
    if not os.path.exists(template_dir):
        LOGGER.info("Creating Template in {}".format(template_dir))
        os.makedirs(template_dir)

    docker_file = os.path.join(template_dir, 'Dockerfile.mustache')
    dotfile = os.path.join(template_dir, '.dockerstache')
    pre_script = os.path.join(template_dir, 'pre_script.sh')
    post_script = os.path.join(template_dir, 'post_script.sh')
    context = os.path.join(template_dir, 'context.json')
    installer_script = os.path.join(template_dir, 'install_script.sh.mustache')
    opts.context_file = os.path.join(opts.template_dir, 'context.json')

     # make sure repo is clean
    if has_unstaged_changes(opts.repo):
        msg = (
            "Error: Unstaged changes are present on the branch "
            "Please commit them or clean up before proceeding"
        )
        LOGGER.error(msg)
        raise RuntimeError(msg)

    main_branch = config.gitflow_branch_name()
    LOGGER.info("checking out latest {} branch...".format(main_branch))
    checkout_and_pull(opts.repo,  main_branch, not opts.no_remote)

    venv_option = ""
    if opts.virtualenv:
        venv_option = ". {}/bin/activate".format(opts.virtualenv)

    with working_dir(template_dir):
        write_basic_dockerfile(opts, config, docker_file)
        write_json_file(dotfile, {
            "post_script": "post_script.sh",
            "pre_script": "pre_script.sh",
            "inclusive": True,
            "excludes": ["post_script.sh", "post_script.sh", ".dockerstache"]
        })
        write_json_file(context, {})

        # render templates for container scripts
        template_context = {
            'open_brace': '{{',
            'close_brace': '}}',
            'package': config.package_name(),
            'virtualenv': venv_option,
            'pip_options': config.pip_options() if config.pip_options() else ""
        }

        install_template = find_template('install_script.sh.mustache')
        pre_template = find_template('pre_script.sh.mustache')
        post_template = find_template('post_script.sh.mustache')

        renderer = pystache.Renderer()
        install_result = renderer.render_path(install_template, template_context)

        with open(installer_script, 'w') as handle:
            handle.write(install_result)

        post_result = renderer.render_path(post_template, template_context)
        with open(post_script, 'w') as handle:
            handle.write(post_result)

        pre_result = renderer.render_path(pre_template, template_context)
        with open(pre_script, 'w') as handle:
            handle.write(pre_result)

        make_executable(pre_script, opts.repo)
        make_executable(post_script, opts.repo)
        make_executable(installer_script, opts.repo)

        edit_cirrus_conf(opts, config)

        modified = [
            cirrus_conf,
            docker_file,
            dotfile,
            pre_script,
            post_script,
            installer_script,
            context
        ]
        LOGGER.info("commiting changes...")
        commit_files_optional_push(
            opts.repo,
            "git cirrus package container-init",
            not opts.no_remote,
            *modified
        )
