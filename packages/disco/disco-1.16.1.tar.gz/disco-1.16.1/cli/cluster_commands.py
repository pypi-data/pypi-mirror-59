import click

from cli.command_utils import info_message, list_to_table
from disco import Cluster

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cluster():
    """Manage clusters."""
    pass

@cluster.command(context_settings=CONTEXT_SETTINGS, short_help="List available clusters for the current user.")
def list():
    """
    List available clusters for the current user.

    $ disco cluster list
    """
    # TODO: check logged in and try catch after remove spinners is merged
    clusters = Cluster.list_clusters()
    display_clusters(clusters)


def display_clusters(clusters_list):
    """
    Display clusters as table
    Args:
        clusters_list: list of cluster details

    Returns:

    """
    cluster_table = []
    for cluster in clusters_list:
        cluster_table.append(
            [
                "V" if cluster.is_default else "",
                cluster.id,
                cluster.name,
                cluster.type,
                cluster.region,
                cluster.external_account_id,
                cluster.bucket_name,
                "Yes" if cluster.is_last_connection_check_valid else "No",
                "Yes" if cluster.is_active else "No",
                "Yes" if cluster.cloud_offload_enabled else "No"
            ]
        )
    info_message(list_to_table(cluster_table, headers=["Default", "ID", "Name", "Cloud type", "Region",
                                                       "Account", "Bucket", "Connection valid", "Active",
                                                       "Cloud offload enabled"]))
