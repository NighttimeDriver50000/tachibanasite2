# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2016 Chris McKinney.

import sys

def render_template_env(filename, **environment):
    """Render the template in the given environment."""
    from bottle import SimpleTemplate
    with open(filename, encoding="UTF-8") as fileobj:
        return SimpleTemplate(fileobj, name=filename).render(**environment)

def render_template(filename, **environment):
    """Render the template in the default environment with additional values."""
    env = DEFAULT_TEMPLATE_ENV.copy()
    env.update(environment)
    return render_template_env(filename, **env)

def _get_tpl_lib_bindings():
    """Gets bindings from modules."""
    import importlib
    import os
    from os import path
    modules_path = path.join(path.dirname(__file__), "ts1modules")
    if path.isdir(modules_path):
        sys.path.append(modules_path)
        module_names = os.listdir(modules_path)
    else:
        module_names = []
    module_names.sort()
    bindings = []
    for name in module_names:
        module_init = path.join(path.join(modules_path, name), "__init__.py")
        if not path.isfile(module_init):
            continue
        try:
            module = importlib.import_module(name)
            bindings.append(module.TACHIBANASITE_TPL_LIB_BINDINGS)
        except ImportError:
            continue
        except AttributeError:
            continue
    return bindings

# The default environment for render_template.
DEFAULT_TEMPLATE_ENV = {
        "_GET": {},
        "render_template_env": render_template_env,
        "render_template": render_template,
        }

for lib_bindings in _get_tpl_lib_bindings():
    DEFAULT_TEMPLATE_ENV.update(lib_bindings)
