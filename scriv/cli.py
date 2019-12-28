"""Scriv command-line interface."""

import click


@click.group()
def cli():
    """Manage changelogs."""


@cli.command()
def hello():
    """Say hello."""
    click.echo("Hello!")
