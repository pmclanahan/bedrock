import logging

from commander.deploy import task

from deploy_base import *  # noqa


log = logging.getLogger(__name__)
base_update_assets = update_assets
base_database = database


@task
def database(ctx):
    # only ever run this one on demo and dev.
    base_database()
    management_cmd(ctx, 'rnasync')
    management_cmd(ctx, 'update_security_advisories --quiet', use_src_dir=True)
    management_cmd(ctx, 'cron update_ical_feeds')
    management_cmd(ctx, 'cron update_tweets')
    management_cmd(ctx, 'runscript update_firefox_os_feeds')


@task
def update_assets(ctx):
    """Compile/compress static assets and fetch external data."""
    base_update_assets()
    # can't do this in `database` because it needs to run before
    # the file sync from SRC -> WWW.
    management_cmd(ctx, 'update_product_details', use_src_dir=True)
