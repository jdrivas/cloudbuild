#!/usr/bin/env python

import argparse
import click
import googleapiclient as gapi
import googleapiclient.discovery

# Account credentials have to be set for this to work.
# Set the environment variable to point to a file where the creds 
# are like this, for exmaple;
#      export GOOGLE_APPLICATION_CREDENTIALS="./account.json"
# 
#  You can see how to get the crednetials [here](https://cloud.google.com/docs/authentication/production#obtaining_and_providing_service_account_credentials_manually)

def list_triggers(cloudbuild, project):
  result = cloudbuild.projects().triggers().list(projectId=project).execute()
  triggers = result['triggers']
  print(f"For {project} there are {len(triggers)} cloud build triggers defined.")
  for trigger in triggers:
    t = trigger['triggerTemplate']
    print(f"- {trigger['description']}")
    print(f"   repo: {t['repoName']}")
    print(f"   branch: {t['branchName']}")

def create_trigger(cloudbuild, project, triggerDef):
  print(f"Creating a new trigger for project {project}")
  result = cloudbuild.projects().triggers().create(projectId=project, body=triggerDef).execute()
  print(f"Trigger result:")
  print(result)

if __name__ == '__main__':

  trigger_parser = argparse.ArgumentParser()
  trigger_commands = trigger_parser.add_subparsers(dest="command")
  trigger_parser.add_argument("--project", default="momentlabs-jupyter", help="GCE project")

  trigger_list_parser = trigger_commands.add_parser("list")
  trigger_create_parser = trigger_commands.add_parser("create")


  args = trigger_parser.parse_args()
  cloudbuild = gapi.discovery.build('cloudbuild' , 'v1')

  # We'll clean this up later,  maybe use the set_defaults func 
  # in the args or create a dictionary fo commands to execute against.
  if args.command == "list":
    list_triggers(cloudbuild, args.project)
  elif args.command == "create":
    triggerDef = {
      "description": "Image-build-dsn-test-2",
      "triggerTemplate": {
        "repoName": "github-momentlabs-athenaeum",
        "branchName": "staging|master",
        "projectId": "momentlabs-jupyter"
      },
      "includedFiles": [
        "images/datascience-notebook-lab/Dockerfile",
        "images/datascience-notebook-lab/cloudbuild.yaml"
      ], 
      "filename": "images/datascience-notebook-lab/cloudbuild.yaml"
    }
    create_trigger(cloudbuild, args.project, triggerDef)

    

