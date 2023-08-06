from dask.distributed import Client
from dask_jobqueue import SLURMCluster

DEFAULT_QUEUE = 'lix-atsas'
DEFAULT_NUM_CORES = 1
DEFAULT_MEMORY = '4GB'
DEFAULT_MINIMUM_WORKERS = 0
DEFAULT_MAXIMUM_WORKERS = 20
DEFAULT_ADDRESS = '127.0.0.1'
DEFAULT_PORT = 34567


_doc_dask_slurm_cluster = \
    f"""
    Run a Dask Slurm cluster.

    Parameters
    ----------
    queue: str, optional
        the Slurm queue to submit to. Default: {DEFAULT_QUEUE}
    cores: int, optional
        the number of cores to use per job. Default: {DEFAULT_NUM_CORES}
    memory: str, optional
        the amount of memory to use per job. Default: {DEFAULT_MEMORY}
    minimum_workers: int, optional
        the minimum number of workers to scale the cluster down to in the
        autoscale mode. Default: {DEFAULT_MINIMUM_WORKERS}
    maximum_workers: int, optional
        the maximum number of workers to scale the cluster up to in the
        autoscale mode. Default: {DEFAULT_MAXIMUM_WORKERS}
    address: str, optional
        the network address to be assigned to the cluster's scheduler.
        Default: {DEFAULT_ADDRESS}
    port: int, optional
        the network port to be assigned to the cluster's scheduler.
        Default: {DEFAULT_PORT}

    Returns
    -------
    cluster : dask_jobqueue.SLURMCluster
        an instance of the Dask Slurm Cluster
    """


def dask_slurm_cluster(queue=None, cores=None, memory=None,
                       minimum_workers=None, maximum_workers=None,
                       address=None, port=None, **kwargs):
    __doc__ = _doc_dask_slurm_cluster  # noqa

    queue = queue or DEFAULT_QUEUE
    cores = cores or DEFAULT_NUM_CORES
    memory = memory or DEFAULT_MEMORY
    minimum_workers = minimum_workers or DEFAULT_MINIMUM_WORKERS
    maximum_workers = maximum_workers or DEFAULT_MAXIMUM_WORKERS
    address = address or DEFAULT_ADDRESS
    port = port or DEFAULT_PORT

    cluster = SLURMCluster(queue=queue, cores=cores, memory=memory,
                           host=f'tcp://{address}:{port}', **kwargs)
    cluster.adapt(minimum=minimum_workers, maximum=maximum_workers)
    return cluster


def dask_client(cluster=None):
    args = []
    if cluster is not None:
        args.append(cluster)
    client = Client(*args)
    return client
