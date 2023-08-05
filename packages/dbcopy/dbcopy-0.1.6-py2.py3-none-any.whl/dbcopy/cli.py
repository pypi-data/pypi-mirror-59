import click
import logging
import tqdm

from dbcopy.db import Database
from dbcopy.util import NameMapping

log = logging.getLogger('dbcopy')


@click.command()
@click.argument('source_uri', nargs=1, envvar='DBCOPY_SOURCE_URI')
@click.argument('target_uri', nargs=1, envvar='DBCOPY_TARGET_URI')
@click.option('-p', '--prefix', help='Prefix for table names')
@click.option('-d', '--drop', is_flag=True, default=False, help='Drop existing tables')  # noqa
@click.option('-s', '--skip', is_flag=True, default=False, help='Skip existing tables')  # noqa
@click.option('-i', '--include', multiple=True, help='Include these tables')  # noqa
@click.option('-x', '--exclude', multiple=True, help='Exclude these tables')  # noqa
@click.option('-nt', '--normalize-tables', is_flag=True, default=False, help='Normalize table names')  # noqa
@click.option('-nc', '--normalize-columns', is_flag=True, default=False, help='Normalize column names')  # noqa
@click.option('-c', '--chunk-size', type=int, default=10000, help='Row batch size')  # noqa
def dbcopy(source_uri, target_uri, prefix, drop, skip, include, exclude,
           normalize_tables, normalize_columns, chunk_size):
    """Copy tables from a source database to a target database."""
    logging.basicConfig(level=logging.DEBUG)
    # logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)
    source_db = Database(source_uri)
    target_db = Database(target_uri)
    for table in source_db.tables:
        not_included = len(include) and table.name not in include
        if table.name in exclude or not_included:
            log.info("Skip table: %s", table.name)
            continue
        mapping = NameMapping(table,
                              prefix=prefix,
                              normalize_tables=normalize_tables,
                              normalize_columns=normalize_columns)
        if len(mapping.columns) != len(table.columns):
            msg = 'Column name collision: %r' % mapping.columns
            raise click.ClickException(msg)

        count = source_db.count(table)
        target_table, exists = target_db.create(table, mapping, drop=drop)
        if exists and skip:
            log.info("Skip existing table: %s", table.name)
            continue
        log.info('Copy: %s -> %s (%s columns, %s rows)',
                 table.name, mapping.name,
                 len(mapping.columns), count)
        progress = target_db.copy(source_db, table, target_table,
                                  mapping, chunk_size=chunk_size)
        for row in tqdm.tqdm(progress, total=count, unit='rows', leave=False):
            pass


if __name__ == "__main__":
    dbcopy()
