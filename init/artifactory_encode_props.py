#!/usr/bin/env python3
# python3 artifactory_encode_props.py "key1=value1" "key1=value2" "key2=value1,a,  b  b  ;c" "key2=value2" "key3=  last-value  "

import argparse
from collections import defaultdict


def artifactory_encode_prop_value(value: str) -> str:
    # this escapes a property value. the special characters, such as
    # backslashes (\), commas (,), semicolons (;), pipes (|) must be
    # escaped with a backslash (\) character.
    return (
        value
            .replace("\\", "\\\\")
            .replace(",", "\\,")
            .replace(";", "\\;")
            .replace("|", "\\|")
    )


def artifactory_encode_props(args: list[str]) -> str:
    # NB each property is separated by a semicolon (;), and each value within a
    #    property is separated by a comma (,). special characters, such as
    #    backslashes (\), commas (,), semicolons (;), pipes (|) within values
    #    must be escaped with a backslash (\) character.
    # NB when multiple values are used, their order is not preserved.
    # NB a prop key has a maximum length of 255 characters.
    # NB a prop value has a maximum length of 2400 characters.
    #    NB unfortunately, it seems, the value is truncated without any error.
    # NB the postgres public.node_props database table is defined as:
    #       prop_key   character varying(255)
    #       prop_value character varying(4000)
    # NB jf rt upload --target-props embeds the properties in the URL, e.g.,
    #    http://artifactory:8082/artifactory/example-repo-local/example-1.0.0.txt;k1=v1;k2=v2
    #    so the total length of the URL is also an limitation. from my test,
    #    the url has a maximum length of about 5k characters.
    # NB the UI (but not the API) trims the leading and trailing spaces from the
    #    values.
    # see https://jfrog.com/help/r/jfrog-rest-apis/set-item-properties
    # see https://jfrog.com/help/r/jfrog-artifactory-documentation/using-properties-in-deployment-and-resolution

    props = defaultdict(list)

    for prop in args:
        key, value = prop.split("=", 1)
        props[key].append(value)

    encoded_props = []
    for key, values in props.items():
        encoded_values = [artifactory_encode_prop_value(value) for value in values]
        encoded_props.append(f"{key}={','.join(encoded_values)}")

    return ";".join(encoded_props)


def main():
    parser = argparse.ArgumentParser(description="Encode Artifactory properties.")
    parser.add_argument(
        "props",
        metavar="PROPS",
        type=str,
        nargs="+",
        help="Properties to encode.\nUse the key=value format.\nYou can enter multiple pairs.\nExample: key=value key2=value1 key2=value2",
    )
    args = parser.parse_args()

    print(artifactory_encode_props(args.props))


if __name__ == "__main__":
    main()
