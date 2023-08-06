[![npm version](https://badge.fury.io/js/%40taimos%2Fcdk-construct-gitlab-variable.svg)](https://badge.fury.io/js/%40taimos%2Fcdk-construct-gitlab-variable)
[![PyPI version](https://badge.fury.io/py/taimos.cdk-construct-gitlab-variable.svg)](https://badge.fury.io/py/taimos.cdk-construct-gitlab-variable)

# A CDK L3 Construct for storing Gitlab CI variables from a SecretsManager secret

## Installation

You can install the library into your project using npm or pip.

```bash
npm install @taimos/cdk-construct-gitlab-variable

pip3 install taimos.cdk-construct-gitlab-variable
```

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
secret = Secret(self, "DBSecret",
    description="Some Secret",
    generate_secret_string={
        "secret_string_template": "{\"username\":\"admin2\"}",
        "generate_string_key": "password",
        "password_length": 20
    }
)

gitlab_secret = Secret.from_secret_arn(self, "GitlabToken", "arn:aws:secretsmanager:eu-central-1:123456789012:secret:GitlabToken-abcde")

db_password = GitlabVariable(self, "GitlabVarPassword",
    gitlab_secret=gitlab_secret,
    secret=secret,
    secret_field="password",
    project_id="group/secrets-test",
    variable_name="RDS_PASSWORD"
)
```

# Contributing

We welcome community contributions and pull requests.

# License

The CDK construct library is distributed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

See [LICENSE](./LICENSE) for more information.
