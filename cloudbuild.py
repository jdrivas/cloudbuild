#!/usr/bin/env python

from os import environ
import json

import click

import googleapiclient as gapi
import googleapiclient.discovery
from google.oauth2 import service_account

@click.group()
@click.option("--project", "-p", prompt=True, metavar="<project name>", help="GCE project name")
@click.option("--credential_file", "-c", default="./account.json", show_default=True, help="pathname of GCE credentials")
@click.pass_context
def cli(ctx, project, credential_file):
  ctx.obj = {} if ctx.obj == None else ctx.obj
  ctx.obj['project'] = project

  # get credentials and the cloudbuild connection.
  cloudbuild = None
  if "GOOGLE_APPLICATION_CREDENTIALS" in environ:
    cloudbuild = gapi.discovery.build('cloudbuild' , 'v1')
  else:
    try: 
      credentials = service_account.Credentials.from_service_account_file(credential_file)
      cloudbuild = gapi.discovery.build('cloudbuild' , 'v1', credentials=credentials)
    except Exception as err:
      print(f"Credentials error: {err}")
      exit()
  
  if cloudbuild:
    ctx.obj['cloudbuild'] = cloudbuild

@cli.command()
@click.pass_context
@click.argument('trigger_def_file', type=click.File(mode='r'), metavar="<trigger-def-json-file>")
def create(ctx, trigger_def_file):
  """Create a new  trigger from a file with a JSON trigger defintion"""
  cloudbuild = ctx.obj['cloudbuild']
  project = ctx.obj['project']
  trigger_def = json.load(trigger_def_file)
  print(trigger_def)
  result = cloudbuild.projects().triggers().create(projectId=project, body=trigger_def).execute()
  print(result)

@cli.command()
@click.pass_context
@click.argument('trigger-id', metavar="<trigger-id>")
def delete(ctx, trigger_id):
  """Delete the trigger by id"""
  cloudbuild = ctx.obj['cloudbuild']
  project = ctx.obj['project']

  result = cloudbuild.projects().triggers().delete(projectId=project, triggerId=trigger_id).execute()
  print(f"deleted {trigger_id}")
  print(result)

@cli.command()
@click.pass_context
def list(ctx):
  """List the currently defined triggers for the project."""
  cloudbuild = ctx.obj['cloudbuild']
  project = ctx.obj['project']

  result = cloudbuild.projects().triggers().list(projectId=project).execute()
  triggers = result['triggers']
  print(f"For {project} there are {len(triggers)} cloud build triggers defined.")
  for trigger in triggers:
    t = trigger['triggerTemplate']
    print(f"{trigger['description']}")
    print(f"    Id: {trigger['id']}")
    print(f"    repo: {t['repoName']}")
    print(f"    branch: {t['branchName']}")

if __name__ == '__main__':
    cli()

