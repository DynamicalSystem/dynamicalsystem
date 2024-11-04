# dynamicalsystem

Describe your project here.

## Structure

We use a [namespace](https://peps.python.org/pep-0420/) [src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) structure which has consequences for testing, build, deployment and dependency management.

Project structure is maintained by [Rye](https://rye.astral.sh/guide/) via a couple of scripts which jang Rye's output around to force (Rye Workspaces)[] to approximate namespaces.

- `mkpkg.sh` creates a new package within the namepace, setting the package name and putting dots in the right place correcting directory structure and whatnot.
- `mknsp.sh` creates a new namespace, setting the Rye virtual flag, appending a workspace designator and creating a test package.

We end up with something like this:

```text
namespace
├── README.md
├── pyproject.toml
└── namespace_project
│   ├── README.md
│   ├── pyproject.toml
│   └── src
│       └── namespace
│           └── project
│               ├── __init__.py
│               └── __main__.py
└── namespace_pytests
    ├── README.md
    ├── pyproject.toml
    └── src
        └── namespace
            └── pytests
                ├── __init__.py
                └── __main__.py
                └── test_project_module.py
```

## Testing

Structure raises the spectre of test location... We move them out of the library and application projects into `namespace_pytests` and use a naming convention to keep them all square.  There are tradeoffs here:

| Negatives | Positives|
| --- | --- |
| `rye test --package namespace-pytests` becomes the default. | There is a reduced chance of shipping the tests |
| It's harder to isolate a set of tests - they all run on command. | dave |
| Ruff doesn't handle fixtures very well |  |

## Workflow

One of the reasons for employing namespaces is to enable separation of concerns within an organisation's codebase.  We can take mixins and utils and shove them into a garden shed library under the namespace.  We can then build a series of apps which use the things in the shed and we can modify the apps and the shed all within the same code tree. The tests keep you sane. It's a nice way of working.

Rye workspaces help make this pleasant by structuring the dev dependencies into a single venv using `-e` to install all the namespaces packages in a workspace.  This is one of the reasons why the `namespace_pytests` structure works cleanly... the tests are just an editable install in the same venv as the code.

Working becomes an OODA loop of:

- Change code
- Change tests
- `rye sync`
- `rye test --package dynamicalsystem-pytests`
- Loop

There are targets in the `makefile` to enshrine this workflow.  It would be great to add `rye lint` to this too but there's a problem:

```makefile
sync:
    rye fmt --all --check
    rye sync

test:
    rye test --package dynamicalsystem-pytests
```

There are different concerns when promoting all this to a test environment.