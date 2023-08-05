import re


def parse_packages(regex, output, lower=True):
    packages = {}

    for line in output:
        matches = re.match(regex, line)

        if matches:
            # Sort out name
            name = matches.group(1)
            if lower:
                name = name.lower()

            packages.setdefault(name, set())
            packages[name].add(matches.group(2))

    return packages
