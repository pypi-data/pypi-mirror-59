# Copyright 2015 Rackspace US, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import os
import subprocess

import dulwich.repo
from pbr import packaging
from sphinx.ext import extlinks
from sphinx.util import logging

from otcdocstheme import paths

_series = None
_project = None
_giturl = 'https://github.com/{}/{}'
_html_context_data = None

logger = logging.getLogger(__name__)


def _get_other_versions(app):
    if not app.config.html_theme_options.get('show_other_versions', False):
        return []

    all_series = []
    try:
        repo = dulwich.repo.Repo.discover()
    except dulwich.repo.NotGitRepository:
        return []

    refs = repo.get_refs()
    for ref in refs.keys():
        ref = ref.decode('utf-8')
        if ref.startswith('refs/remotes/origin/stable'):
            series = ref.rpartition('/')[-1]
            all_series.append(series)
        elif ref.startswith('refs/tags/') and ref.endswith('-eol'):
            series = ref.rpartition('/')[-1][:-4]
            all_series.append(series)
    all_series.sort()

    # NOTE(dhellmann): Given when this feature was implemented, we
    # assume that the earliest version we can link to is for
    # mitaka. Projects that have older docs online can set the option
    # to indicate another start point. Projects that come later should
    # automatically include everything they actually have available
    # because the start point is not present in the list.
    earliest_desired = app.config.html_theme_options.get(
        'earliest_published_series', 'mitaka')
    if earliest_desired and earliest_desired in all_series:
        interesting_series = all_series[all_series.index(earliest_desired):]
    else:
        interesting_series = all_series

    # Reverse the list because we want the most recent to appear at
    # the top of the dropdown. The "latest" release is added to the
    # front of the list by the theme so we do not need to add it
    # here.
    interesting_series.reverse()
    return interesting_series


def _get_doc_path(app):
    # Handle 'doc/{docType}/source' paths
    doc_parts = os.path.abspath(app.srcdir).split(os.sep)[-3:]
    if doc_parts[0] == 'doc' and doc_parts[2] == 'source':
        return '/'.join(doc_parts)

    # Handle '{docType}/source' paths
    doc_parts = os.path.abspath(app.srcdir).split(os.sep)[-2:]
    if doc_parts[1] == 'source':
        return '/'.join(doc_parts)

    logger.info('Cannot identify project\'s root directory.')
    return


def _html_page_context(app, pagename, templatename, context, doctree):
    global _html_context_data
    if _html_context_data is None:
        _html_context_data = {}
        try:
            _html_context_data['gitsha'] = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
            ).decode('utf-8').strip()
        except Exception as e:
            logger.warning('Cannot get gitsha from git repository: %s.'
                           % str(e))
            _html_context_data['gitsha'] = 'unknown'

        doc_path = _get_doc_path(app)
        repo_name = app.config.repository_name
        if repo_name and doc_path:
            _html_context_data['giturl'] = _giturl.format(repo_name, doc_path)
        bug_project = app.config.bug_project
        if bug_project:
            _html_context_data['bug_project'] = bug_project
        if bug_project and bug_project.isdigit():
            _html_context_data['use_storyboard'] = True
        bug_tag = app.config.bug_tag
        if bug_tag:
            _html_context_data['bug_tag'] = bug_tag

    context.update(_html_context_data)
    context['other_versions'] = _get_other_versions(app)


def _get_series_name():
    "Return string name of release series, or 'latest'"
    global _series
    if _series is None:
        parser = configparser.ConfigParser()
        parser.read('.gitreview')
        try:
            branch = parser.get('gerrit', 'defaultbranch')
        except configparser.Error:
            _series = 'latest'
        else:
            _series = branch.rpartition('/')[-1]
    return _series


def _setup_link_roles(app):
    series = _get_series_name()
    for project_name in app.config.otc_projects:
        url = 'https://docs.otc.org/{}/{}/%s'.format(
            project_name, series)
        role_name = '{}-doc'.format(project_name)
        logger.info('adding role %s to link to %s', role_name, url)
        app.add_role(role_name, extlinks.make_link_role(url, project_name))


def _find_setup_cfg(srcdir):
    """Find the 'setup.cfg' file, if it exists.

    This assumes we're using 'doc/source' for documentation, but also allows
    for single level 'doc' paths.
    """
    # TODO(stephenfin): Are we sure that this will always exist, e.g. for
    # an sdist or wheel? Perhaps we should check for 'PKG-INFO' or
    # 'METADATA' files, a la 'pbr.packaging._get_version_from_pkg_metadata'
    for path in [
            os.path.join(srcdir, os.pardir, 'setup.cfg'),
            os.path.join(srcdir, os.pardir, os.pardir, 'setup.cfg')]:
        if os.path.exists(path):
            return path

    return None


def _get_project_name(srcdir):
    """Return string name of project name, or None.

    This assumes every project is using 'pbr' and, therefore, the metadata can
    be extracted from 'setup.cfg'.

    We don't rely on distutils/setuptools as we don't want to actually install
    the package simply to build docs.
    """
    global _project
    if _project is None:
        parser = configparser.ConfigParser()

        path = _find_setup_cfg(srcdir)
        if not path or not parser.read(path):
            logger.info('Could not find a setup.cfg to extract project name '
                        'from')
            return None

        try:
            # for project name we use the name in setup.cfg, but if the
            # length is longer then 32 we use summary. Otherwise thAe
            # menu rendering looks brolen
            project = parser.get('metadata', 'name')
            if len(project.split()) == 1 and len(project) > 32:
                project = parser.get('metadata', 'summary')
        except configparser.Error:
            logger.info('Could not extract project metadata from setup.cfg')
            return None
        _project = project
    return _project


def _builder_inited(app):
    theme_dir = paths.get_html_theme_path()
    logger.info('Using otcdocstheme Sphinx theme from %s' % theme_dir)
    _setup_link_roles(app)

    # we only override configuration if the theme has been configured, meaning
    # users are using these features
    if app.config.html_theme != 'otcdocs':
        return

    # TODO(stephenfin): Once Sphinx 1.8 is released, we should move the below
    # to a 'config-inited' handler

    project_name = _get_project_name(app.srcdir)
    try:
        version = packaging.get_version(project_name)
    except Exception:
        version = None

    # NOTE(stephenfin): Chances are that whatever's in 'conf.py' is probably
    # wrong/outdated so, if we can, we intentionally overwrite it...
    if project_name:
        app.config.project = project_name

    app.config.html_last_updated_fmt = '%Y-%m-%d %H:%M'

    # ...except for version/release which, if blank, should remain that way to
    # cater for unversioned documents
    if app.config.version != '' and version:
        app.config.version = version
        app.config.release = version

    otc_logo = paths.get_otc_logo_path()
    pdf_theme_path = paths.get_pdf_theme_path()

    app.config.latex_engine = 'xelatex'
    app.config.latex_elements = {
        'papersize': 'a4paper',
        'pointsize': '11pt',
        'figure_align': 'H',
        'classoptions': ',openany',
        'preamble': r"""
\usepackage{""" + pdf_theme_path + """}
\\newcommand{\otclogo}{""" + otc_logo + """}
"""}


def setup(app):
    logger.info('connecting events for otcdocstheme')
    app.connect('builder-inited', _builder_inited)
    app.connect('html-page-context', _html_page_context)
    app.add_config_value('repository_name', '', 'env')
    app.add_config_value('bug_project', '', 'env')
    app.add_config_value('bug_tag', '', 'env')
    app.add_config_value('otc_projects', [], 'env')
    app.add_html_theme(
        'otcdocs',
        os.path.abspath(os.path.dirname(__file__)) + '/theme/otcdocs',
    )
    return {
        'parallel_read_safe': True,
    }
