from functools import partial
from pathlib import Path
from .lda_utils import plot_lda
from .plot_options import default_kwargs
from ..dataset import (
    abstracts,
    abstracts_by_subject,
    tocs,
    tocs_by_subject,
)
from ..share import batch_multiprocess

__all__ = [
    "plot_abstracts",
    "plot_abstracts_by_subject",
    "plot_tocs_by_subject",
    "plot_tocs",
    "plot_dataset",
]


def make_plots(
    data,
    start_k=default_kwargs["start_k"],
    stop_k=default_kwargs["stop_k"],
    max_repeats=default_kwargs["max_repeats"],
    save_subpath=".",
):
    """
    Cycle repeatedly through the range of values for k, `max_repeats` times.
    """
    all_funcs = []
    for max_df in [0.5, 0.4, 0.3, 0.2, 0.1]:
        for _ in range(max_repeats):
            for k in range(start_k, stop_k + 1):
                f = partial(
                    plot_lda,
                    data=data,
                    n_components=k,
                    max_df=max_df,
                    save=True,
                    save_subpath=save_subpath,
                )
                all_funcs.append(f)
    batch_multiprocess(all_funcs)


def plot_abstracts(
    start_k=default_kwargs["start_k"],
    stop_k=default_kwargs["stop_k"],
    max_repeats=default_kwargs["max_repeats"],
    save_subpath_prefix=default_kwargs["save_subpath_prefix"],
    save_subpath_suffix=default_kwargs["save_subpath_suffix"],
):
    ns = locals()
    plot_dataset(
        "abstracts", by_subject=False, **{k: ns[k] for k in default_kwargs}
    )


def plot_abstracts_by_subject(
    start_k=default_kwargs["start_k"],
    stop_k=default_kwargs["stop_k"],
    max_repeats=default_kwargs["max_repeats"],
    save_subpath_prefix=default_kwargs["save_subpath_prefix"],
    save_subpath_suffix=default_kwargs["save_subpath_suffix"],
):
    ns = locals()
    plot_dataset(
        "abstracts", by_subject=True, **{k: ns[k] for k in default_kwargs}
    )


def plot_tocs_by_subject(
    start_k=default_kwargs["start_k"],
    stop_k=default_kwargs["stop_k"],
    max_repeats=default_kwargs["max_repeats"],
    save_subpath_prefix=default_kwargs["save_subpath_prefix"],
    save_subpath_suffix=default_kwargs["save_subpath_suffix"],
):
    ns = locals()
    plot_dataset("tocs", by_subject=True, **{k: ns[k] for k in default_kwargs})


def plot_tocs(
    start_k=default_kwargs["start_k"],
    stop_k=default_kwargs["stop_k"],
    max_repeats=default_kwargs["max_repeats"],
    save_subpath_prefix=default_kwargs["save_subpath_prefix"],
    save_subpath_suffix=default_kwargs["save_subpath_suffix"],
):
    ns = locals()
    plot_dataset("tocs", by_subject=False, **{k: ns[k] for k in default_kwargs})


def tocs_as_docs(tocs):
    return [" ".join(toc) for toc in tocs]


def plot_dataset(
    dataset,
    by_subject,
    start_k,
    stop_k,
    max_repeats,
    save_subpath_prefix,
    save_subpath_suffix,
):
    dataset_options = ["abstracts", "tocs"]
    if dataset not in dataset_options:
        raise NameError(f"{dataset=} is not one of {dataset_options=}")
    dir_type = f"{dataset}{'_by_subject' if by_subject else ''}"
    save_subpath = Path(f"{save_subpath_prefix}{dir_type}{save_subpath_suffix}")
    if dataset == "abstracts":
        data = abstracts_by_subject if by_subject else abstracts
    elif dataset == "tocs":
        if by_subject:
            data = {subject: tocs_as_docs(tocs) for k,v in tocs_by_subject.items()}
        else:
            data = tocs_as_docs(tocs)
    make_plots(
        data=data,
        start_k=start_k,
        stop_k=stop_k,
        max_repeats=max_repeats,
        save_subpath=save_subpath,
    )
