from requests.exceptions import HTTPError
from datetime import datetime, timedelta
import click
import json
from api import Api


@click.group()
def cli():
    pass


@cli.command()
@click.option('--api-public', help="Atlas API public key", required=True, envvar='ATLAS_API_PUBLIC')
@click.option('--api-private', help="Atlas API private key", required=True, envvar='ATLAS_API_PRIVATE')
@click.option('--project', help="Atlas project ID", required=True, envvar='ATLAS_PROJECT_ID')
@click.option('--cluster-name', help="Atlas cluster name", required=True, envvar='ATLAS_CLUSTER_NAME')
def get_cluster_info(api_public, api_private, project, cluster_name):
    api = Api(api_public, api_private, project, cluster_name)
    try:
        res = api.get_cluster_info()
        click.echo(json.dumps(res, indent=2))
    except HTTPError as http_err:
        click.echo(f'HTTP {http_err.response.status_code}: {http_err.response.json()["detail"]}')


@cli.command()
@click.option('--api-public', help="Atlas API public key", required=True, envvar='ATLAS_API_PUBLIC')
@click.option('--api-private', help="Atlas API private key", required=True, envvar='ATLAS_API_PRIVATE')
@click.option('--project', help="Atlas project ID", required=True, envvar='ATLAS_PROJECT_ID')
@click.option('--cluster-name', help="Atlas cluster name", required=True, envvar='ATLAS_CLUSTER_NAME')
def get_processes(api_public, api_private, project, cluster_name):
    api = Api(api_public, api_private, project, cluster_name)
    try:
        res = api.get_processes()
        click.echo(json.dumps(res, indent=2))
    except HTTPError as http_err:
        click.echo(f'HTTP {http_err.response.status_code}: {http_err.response.json()["detail"]}')


@cli.command()
@click.option('--api-public', help="Atlas API public key", required=True, envvar='ATLAS_API_PUBLIC')
@click.option('--api-private', help="Atlas API private key", required=True, envvar='ATLAS_API_PRIVATE')
@click.option('--project', help="Atlas project ID", required=True, envvar='ATLAS_PROJECT_ID')
@click.option('--cluster-name', help="Atlas cluster name", required=True, envvar='ATLAS_CLUSTER_NAME')
@click.option('--process-id', help="Atlas process id (host:port)", required=True)
def get_process_by_id(api_public, api_private, project, cluster_name, process_id):
    api = Api(api_public, api_private, project, cluster_name)
    try:
        res = api.get_process_by_id(process_id)
        click.echo(json.dumps(res, indent=2))
    except HTTPError as http_err:
        click.echo(f'HTTP {http_err.response.status_code}: {http_err.response.json()["detail"]}')


@cli.command()
@click.option('--api-public', help="Atlas API public key", required=True, envvar='ATLAS_API_PUBLIC')
@click.option('--api-private', help="Atlas API private key", required=True, envvar='ATLAS_API_PRIVATE')
@click.option('--project', help="Atlas project ID", required=True, envvar='ATLAS_PROJECT_ID')
@click.option('--cluster-name', help="Atlas cluster name", required=True, envvar='ATLAS_CLUSTER_NAME')
@click.option('--hostname', help="Atlas cluster node hostname", required=True)
@click.option('--log-name', help="Atlas log name (mongodb.gz or mongodb-audit-log.gz)", default='mongodb.gz')
@click.option('--output-file', help="Output filename for log", default='mongodb.gz')
@click.option('--start-date', help="Start date for log output (in UTC)", type=click.DateTime(formats=['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']), default=str(datetime.now()-timedelta(minutes=5)))
@click.option('--end-date', help="End date for log output (in UTC)", type=click.DateTime(formats=['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']), default=str(datetime.now()))
def get_process_log(api_public, api_private, project, cluster_name, hostname, log_name, output_file, start_date, end_date):
    api = Api(api_public, api_private, project, cluster_name)
    start_epoch = int(start_date.timestamp()*1000)
    end_epoch = int(end_date.timestamp()*1000)
    try:
        res = api.get_process_log(hostname, log_name, start_epoch, end_epoch)
        open(output_file, 'wb').write(res.content)
    except HTTPError as http_err:
        click.echo(f'HTTP {http_err.response.status_code}: {http_err.response.json()["detail"]}')


@cli.command()
@click.option('--api-public', help="Atlas API public key", required=True, envvar='ATLAS_API_PUBLIC')
@click.option('--api-private', help="Atlas API private key", required=True, envvar='ATLAS_API_PRIVATE')
@click.option('--project', help="Atlas project ID", required=True, envvar='ATLAS_PROJECT_ID')
@click.option('--cluster-name', help="Atlas cluster name", required=True, envvar='ATLAS_CLUSTER_NAME')
@click.option('--process-id', help="Atlas process id (host:port)", required=True)
@click.option('--start-date', help="Start date for measurement output (in UTC)", type=click.DateTime(formats=['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']), default=str(datetime.now()-timedelta(minutes=5)))
@click.option('--end-date', help="End date for measurement output (in UTC)", type=click.DateTime(formats=['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']), default=str(datetime.now()))
@click.option('--granularity', help="Measurement granularity (PT1M, PT5M, PT1H or P1D", default='PT1M')
def get_process_measurements(api_public, api_private, project, cluster_name, process_id, start_date, end_date, granularity):
    api = Api(api_public, api_private, project, cluster_name)

    # no timezone conversion is taking place here - we assume UTC date are being passed in
    start_iso = start_date.replace(microsecond=0).isoformat() + "Z"
    end_iso = end_date.replace(microsecond=0).isoformat() + "Z"
    try:
        res = api.get_process_measurements(process_id, start_iso, end_iso, granularity)
        click.echo(json.dumps(res, indent=2))
    except HTTPError as http_err:
        click.echo(f'HTTP {http_err.response.status_code}: {http_err.response.json()["detail"]}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cli()
