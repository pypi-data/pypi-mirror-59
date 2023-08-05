#!/usr/bin/env python3

import logging
import json
import pprint as pp
import time
from urllib.parse import urlparse

import click
import redis

from cathpy.core import tasks, ssap, version

#import click_log
# click_log.basic_config(LOG)

logging.basicConfig(
    level='DEBUG', format='%(asctime)s %(levelname)6s | %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
LOG = logging.getLogger(__name__)

DEFAULT_PDB_PATH = '/cath/data/{cath_version}/pdb'
DEFAULT_DATASTORE_DSN = 'mongodb://localhost/cath'
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_DUMP_MAX_ENTRIES = 1000


class SsapBatchContext(object):
    def __init__(self, *, pdb_path, datastore_dsn, cath_version, chunk_size, ssap_batch, force=False, debug=False):
        self.pdb_path = pdb_path
        self.datastore_dsn = datastore_dsn
        self.ssap_batch = ssap_batch
        self.chunk_size = chunk_size
        self.cath_version = str(cath_version)
        self.force = force
        self.debug = debug


@click.group()
@click.help_option('-h', '--help')
@click.version_option('0.1', '-v', '--version', message='%(prog)s %(version)s')
@click_log.simple_verbosity_option(LOG, '--verbosity')
def cli():
    pass


def validate_cath_version(ctx, param, value):
    if value is None:
        return None
    try:
        return version.CathVersion(value)
    except ValueError as e:
        raise click.BadParameter(
            f'failed to parse cath version "{value}" (eg "current") err:{e}')


def validate_datastore_dsn(ctx, param, value):
    if value is None:
        return None
    try:
        ds = ssap.SsapStorageFactory.get(value)
        return value
    except ValueError as e:
        raise click.BadParameter(
            f'failed to parse dsn "{value}" (eg "mongodb://localhost/cath", "redis://localhost/0") err:{e}')


@click.command()
@click.option('--cath_version', type=str, callback=validate_cath_version, required=True)
@click.option('--datastore_dsn', type=str, callback=validate_datastore_dsn, default=DEFAULT_DATASTORE_DSN)
@click.option('--max_entries', type=int, default=DEFAULT_DUMP_MAX_ENTRIES)
def ssap_redis_dump(datastore_dsn, cath_version, max_entries):
    '''
    dump SSAP data from Redis datastore
    '''
    ds = ssap.SsapStorageFactory.get(datastore_dsn)

    match_key = ssap.SsapResult.mk_key(
        cath_version=cath_version, id1='ID1', id2='ID2').replace('ID1-ID2', '*')

    LOG.info(f"Dumping datastore records matching '{match_key}'")

    report_chunk_size = int(max_entries / 10)

    for idx, key in enumerate(ds.scan_iter(match=match_key), 1):
        key = key.decode('utf-8')
        ssap_data = json.loads(ds.get(key))
        ssap_str = json.dumps({'id': key, **ssap_data})
        print(ssap_str)
        if idx % report_chunk_size == 0:
            LOG.info(f"Dumped {idx} records")
        if max_entries and idx >= max_entries:
            break

    LOG.info("DONE")


@click.group()
@click.option('--cath_version', type=str, callback=validate_cath_version, required=True)
@click.option('--pairs', type=click.Path(exists=True, file_okay=True), required=True)
@click.option('--datastore_dsn', type=str, callback=validate_datastore_dsn, default=DEFAULT_DATASTORE_DSN)
@click.option('--pdb_path', type=str, default=DEFAULT_PDB_PATH)
@click.option('--chunk_size', type=int, default=DEFAULT_CHUNK_SIZE)
@click.option('--force/--no-force', default=False)
@click.option('--debug/--no-debug', default=False, envvar='CATHPY_DEBUG')
@click.pass_context
def ssap_batch_group(ctx, datastore_dsn, chunk_size, cath_version, pairs, pdb_path, force, debug):
    '''
    manage SSAP jobs
    '''

    ssap_batch = ssap.SsapBatch(cath_version=cath_version,
                                datastore_dsn=datastore_dsn,
                                pairs_file=pairs,)
    opts = {
        'datastore_dsn': datastore_dsn,
        'chunk_size': chunk_size,
        'cath_version': cath_version,
        'debug': debug,
        'pdb_path': pdb_path,
        'ssap_batch': ssap_batch,
        'force': force,
    }

    ctx.obj = SsapBatchContext(**opts)


@click.command()
@click.pass_obj
def ssap_batch_submit(batch_ctx):
    """
    Submits batches of SSAP pairs onto a queue
    """
    LOG.info('Loading missing SSAP pairs onto the queue')

    batch = batch_ctx.ssap_batch
    chunk_size = batch_ctx.chunk_size
    datastore_dsn = batch_ctx.datastore_dsn
    pdb_path = batch_ctx.pdb_path
    cath_version = batch_ctx.cath_version
    force = batch_ctx.force

    batch_count = 1
    total_processed = 0
    celery_tasks = []
    for pairs_missing, processed in batch.read_pairs(chunk_size=chunk_size, force=force):
        if not pairs_missing:
            LOG.info("All pairs present, not submitting any ssap tasks")
            break

        LOG.info(
            f'Submitting {len(pairs_missing)} missing records from datastore ({datastore_dsn})')
        LOG.debug(
            f'cath_version:{cath_version} pdb_path:{pdb_path} datastore_dsn={datastore_dsn}')
        result = tasks.run_ssap_pairs.delay(
            pairs_missing, cath_version=str(cath_version), pdb_path=pdb_path, datastore_dsn=datastore_dsn)
        celery_tasks.extend([result])

    LOG.info(
        f"Created {len(celery_tasks)} batch tasks")

    while True:
        status_types = ('PENDING', 'STARTED', 'RETRY', 'FAILURE', 'SUCCESS')
        status_count = {}
        for status_type in status_types:
            status_count[status_type] = len(
                [t for t in celery_tasks if t.status == status_type])

        LOG.info("Batch status at {} ({}):".format(
            time.strftime('%Y-%m-%d %H:%M:%S'), datastore_dsn))
        LOG.info(
            ' '.join(['{:15s}'.format(f'{t}:{status_count[t]:<3}') for t in status_types]))
        LOG.info("")

        if len(celery_tasks) == len([t for t in celery_tasks if t.status not in ('PENDING', 'STARTED', 'RETRY')]):
            LOG.info("All tasks finished")
            break

        time.sleep(5)


@click.command()
@click.pass_obj
def ssap_batch_info(batch_ctx):
    """Report information on this batch"""

    LOG.info('SSAP pairs in ')
    batch = batch_ctx.ssap_batch

    total_processed = 0
    total_missing = 0
    total_found = 0
    for pairs_missing, processed in batch.read_pairs():
        LOG.info(
            f'Processed {processed} records, found {len(pairs_missing)} missing from datastore ({batch.datastore})')

        total_missing += len(pairs_missing)
        total_found += processed - len(pairs_missing)
        total_processed += processed

    LOG.info(f'TOTAL_RECORDS: {total_processed}')
    LOG.info(f'TOTAL_MISSING: {total_missing}')
    LOG.info(f'TOTAL_FOUND:   {total_found}')


@click.command()
def ssap_batch_worker(datastore_dsn, cath_version, pairs):
    """Start a worker to process SSAP pairs"""
    LOG.info('Starts worker(s) to process SSAP pairs from queue')


ssap_batch_group.add_command(ssap_batch_submit, name='submit')
ssap_batch_group.add_command(ssap_batch_info, name='info')
ssap_batch_group.add_command(ssap_batch_worker, name='worker')


cli.add_command(ssap_redis_dump, name='ssap-redis-dump')
cli.add_command(ssap_batch_group, name='ssap-batch')


if __name__ == '__main__':
    cli()
