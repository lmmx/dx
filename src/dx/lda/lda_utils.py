from .plot_options import default_kwargs
from .plot_cropper import crop_image
from .stopword_utils import StopWords
from ..dataset import (
    abstracts,
    readerships,
    reviews,
    titles,
    tocs,
    abstracts_by_subject,
    readerships_by_subject,
    reviews_by_subject,
    titles_by_subject,
    tocs_by_subject,
)

import warnings
from pathlib import Path
from random import shuffle
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

__all__ = []

def get_rows_shape(n_components):
    "Pick a roughly computer screen shaped plot arrangement given plot count"
    if n_components < 4:
        n_rows = 1
    elif n_components < 9:
        n_rows = 2
    elif n_components < 16:
        n_rows = 3
    elif n_components == 16:
        n_rows = 2
    elif n_components < 25:
        n_rows = 3
    elif n_components < 33:
        n_rows = 4
    elif n_components < 41:
        n_rows = 5
    else:
        n_rows = int(n_components ** 0.5)
    n_per_row = (n_components + (n_components % n_rows)) // n_rows
    if (n_rows * n_per_row) < n_components:
        n_per_row += 1
    return n_rows, n_per_row

def plot_top_words(
    lda,
    feature_names,
    n_top_words,
    title,
    max_df,
    n_components,
    save=True,
    save_subpath=".",
):
    n_rows, row_size = get_rows_shape(n_components)
    fig, axes = plt.subplots(n_rows, row_size, figsize=(30, 10), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(lda.components_):
        top_features_ind = topic.argsort()[: -n_top_words - 1 : -1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]
        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f"Topic {topic_idx +1}", fontdict={"fontsize": 14})
        ax.invert_yaxis()
        ax.tick_params(axis="both", which="major", labelsize=10)
        for i in "top right left".split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=20)

    plt.subplots_adjust(top=0.95, bottom=0.05, wspace=(row_size / 8), hspace=0.2)
    if save:
        k_label = f"{n_components}k"
        max_df_label = f"max_df_{int(max_df *100)}pc"
        save_dir = (
            Path.home()
            / "Pictures"
            / "2021"
            / "lda"
            / save_subpath
            / max_df_label
            / k_label
        )
        save_dir.mkdir(parents=True, exist_ok=True)  # mkdir -p
        png_counter = len([*save_dir.glob("Figure_*.png")])
        save_location = save_dir / f"Figure_{png_counter}.png"
        plt.savefig(save_location)
        crop_image(save_location, inplace=True)
    else:
        plt.show()
    plt.close("all")


def plot_lda(
    data=None,
    data_is_shuffled=False,
    remove_falsey=True,
    n_samples=2000,
    max_features=1000,
    n_components=24,
    n_top_words=20,
    min_df=2,
    max_df=0.6,
    stop_words=StopWords["ALL"].value,
    save=True,
    save_subpath=".",
):
    if data is None:
        data = [x for x in abstracts if x]
    if not data_is_shuffled:
        shuffle(data)
    if remove_falsey:
        data = list(filter(lambda x: x, data))
    data_samples = data[:n_samples]

    # Use tf (raw term count) features for LDA.
    tf_vectorizer = CountVectorizer(
        max_df=max_df, min_df=min_df, max_features=max_features, stop_words=stop_words
    )
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message=".*stop_words", category=UserWarning, append=False)
        tf = tf_vectorizer.fit_transform(data_samples)
    lda = LatentDirichletAllocation(
        n_components=n_components,
        max_iter=20,
        learning_method="online",
        learning_offset=50.0,
        random_state=0,
    )
    lda.fit(tf)

    tf_feature_names = tf_vectorizer.get_feature_names()
    plot_top_words(
        lda,
        tf_feature_names,
        n_top_words,
        "",
        max_df,
        n_components,
        save=save,
        save_subpath=save_subpath,
    )
