from pathlib import Path
import click
from click import prompt

from indico_install.config import ConfigsHolder
from indico_install.utils import run_cmd, options_wrapper
from indico_install.infra.init import init

SCRIPT = Path(__file__).parent / "bin" / "indico_infra.sh"


@click.group("sn")
@click.pass_context
def single_node(ctx):
    """
    Create and validate Indico platform installation on a single node
    """
    pass


single_node.command("init")(init(__name__))


@single_node.command("check")
@click.pass_context
@options_wrapper(check_input=True)
def check(ctx, *, input_yaml, **kwargs):
    """Validate local MicroK8S cluster installation"""
    conf = ConfigsHolder(config=input_yaml)
    run_cmd([str(SCRIPT.resolve()), "check"], tty=True)

    rw_dir = Path(conf["clusterVolumes"]["rwx"]["hostPath"]["path"])
    ro_dir = Path(conf["clusterVolumes"]["rox"]["hostPath"]["path"])
    assert (
        rw_dir and rw_dir.is_dir()
    ), "Directory selected for read-write data does not exist!"
    assert (
        ro_dir and ro_dir.is_dir()
    ), "Directory selected for read-only data does not exist!"


@single_node.command("create")
@click.pass_context
@options_wrapper(check_input=True)
def create(ctx, *, input_yaml, **kwargs):
    """Install local MicroK8S cluster"""
    conf = ConfigsHolder(config=input_yaml)
    run_cmd([str(SCRIPT.resolve()), "create"], tty=True)
    ask_for_infra_input(conf)

    rw_dir = Path(conf["clusterVolumes"]["rwx"]["hostPath"]["path"])
    ro_dir = Path(conf["clusterVolumes"]["rox"]["hostPath"]["path"])

    rw_dirs = " ".join(
        [
            str(rw_dir / sub_dir)
            for sub_dir in ("postgres_data", "rainbow", "finetune_models")
        ]
    )
    run_cmd(f"sudo mkdir -pm 777 {rw_dirs} {str(ro_dir)}".split(), tty=True)


def ask_for_infra_input(conf):
    conf["clusterVolumes"]["rwx"]["hostPath"]["path"] = prompt(
        "Directory for all indico data - should have at least 800GB available",
        default=conf["clusterVolumes"]["rwx"]["hostPath"].get("path", None),
    )

    conf["clusterVolumes"]["rox"]["hostPath"]["path"] = prompt(
        "Directory for read-only-v7 API data - should have 120GB available",
        default=conf["clusterVolumes"]["rox"]["hostPath"].get("path", None),
    )
    conf.save()
