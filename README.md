# CDK Quickstart

It includes all steps to how this repository and deployment pipelines were built, including the workstation setup.  The repository can simply be cloned locally and development can being immediately.


## Windows Workstation Setup - Note: You may need temporary administrator access

> 1.  Download and Install the latest supported version of Python: **https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html**
> 2.  Download and Install the latest version of Node.js: **https://nodejs.org/en/download/**
> 3.  Download and Install the AWS CLI: **https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html**
> 4.  Install Git for windows: **https://git-scm.com/download/win**
> 5.  Install aws-CDK prerequisites: **npm install -g aws-cdk**
> 6.  Install python language-specific prerequisites: **python -m pip install aws-cdk-lib**
> 7.  Install git-remote-codecommit: **pip install git-remote-codecommit**

## AWS SSO Setup
Configuration of the CLI with a profile will be dependent on the setup of your environment.  This will be geared towards AWS SSO integrated with Azure AAD.

> 1. Open a windows command prompt
> 2. Add AWS SSO session: **aws configure sso-session**

SSO session name: **Name your SSO Session**\
SSO start URL [None]: **Enter the start URL for your org**\
SSO region [None]: **<Enter your region>**\
SSO registration scopes [sso:account:access]: **<Leave blank>**

> 3. Add AWS SSO Platform Profile to session: **aws configure sso --profile cdk-demo-platform**

SSO session name (Recommended): **Name your SSO Session**\
**Scroll through the list of accounts and select the platform account**\
CLI default client Region [None]: **<Enter your region>**\
CLI default output format {None]: **json**

> 4. Add AWS SSO Dev Profile to session: **aws configure sso --profile cdk-demo-dev**

SSO session name (Recommended): **cwh**\
**Scroll through the list of accounts and select the dev account**\
CLI default client Region [None]: **us-east-1**\
CLI default output format {None]: **json**

  ## Create CodeCommit repository

> 1. Using the aws CLI, create the repository in the platform account:
  **aws codecommit create-repository --repository-name cdk-demo-repo --repository-description "CDK Demo repo" --profile cdk-demo-platform**
