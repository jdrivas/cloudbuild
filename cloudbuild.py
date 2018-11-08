#!/usr/bin/env python

import json
import click
import googleapiclient as gapi
import googleapiclient.discovery

@click.group()
@click.option("--project", "-p", prompt=True, metavar="<project name>", help="GCE project name")
@click.pass_context
def cli(ctx, project):
  ctx.obj = {} if ctx.obj == None else ctx.obj
  ctx.obj['project'] = project
  cloudbuild = gapi.discovery.build('cloudbuild' , 'v1')
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
def list(ctx):
  """List the currently defined triggers for the project."""
  cloudbuild = ctx.obj['cloudbuild']
  project = ctx.obj['project']

  result = cloudbuild.projects().triggers().list(projectId=project).execute()
  triggers = result['triggers']
  print(f"For {project} there are {len(triggers)} cloud build triggers defined.")
  for trigger in triggers:
    t = trigger['triggerTemplate']
    print(f"- {trigger['description']}")
    print(f"   repo: {t['repoName']}")
    print(f"   branch: {t['branchName']}")

if __name__ == '__main__':
    cli()

