import math
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

RND_SEED: int = 12345 # Random seed

# Resolution for graph images
WIDTH: int = 1366
HEIGHT: int = 768

def set_random_seed() -> None:
    np.random.seed(RND_SEED) # for numpy, scipy
    pd.core.common.random_state(RND_SEED) # for pandas

def plot_box(
    data: pd.Series,
    feature_title: str,
    file_path: str,
    svg: bool = False,
    unit: str = "",
    value_left: tuple[str, ...] = ("min", "q1", "mean"),
    offset: dict[str, float] | None = None,
) -> dict[str, float]:
    set_random_seed()
    if offset is None:
        offset = dict()
    if len(unit) > 0:
        unit = f"Value ({unit})"
    else:
        unit = "Value"

    # Annotation and Plot Code from
    # "Windy": "https://community.plotly.com/t/show-value-in-text-no-need-hover-at-boxplot-q1-q3-fences-with-px-box/48511/4"
    arr: np.ndarray = data.dropna().to_numpy()
    arr.sort()
    
    # Statistical values for annotating Box-whisker Plot
    min_ = np.min(arr)
    max_ = np.max(arr)
    mean = np.mean(arr)
    std = np.std(arr, ddof=1)
    q1, median, q3 = data.quantile(0.25), data.quantile(0.5), data.quantile(0.75)
    iqr = q3 - q1

    # Calculate limit (Whisker)
    lw_limit = q1 - 1.5 * iqr
    lw_fence = np.min(list(filter(lambda x: x >= lw_limit, arr)))
    up_limit = q3 + 1.5 * iqr
    up_fence = np.max(list(filter(lambda x: x <= up_limit, arr)))
    
    # Count outliers
    l_outlier = list(filter(lambda x: not math.isclose(x, lw_fence, abs_tol=1e-6) and x < lw_limit, arr))
    u_outlier = list(filter(lambda x: not math.isclose(x, up_fence, abs_tol=1e-6) and x > up_limit, arr))
    print(f"Lower Outliers Count: {len(l_outlier)}")
    print(f"Upper Outliers Count: {len(u_outlier)}")
    del l_outlier, u_outlier
    
    annots: list[dict[str]] = [
        dict(name="min", y=min_, text=f'Min: {min_:.2f}'),
        dict(name="lower", y=lw_fence, text=f'Lower: {lw_fence:.2f}'),
        dict(name="q1", y=q1, text=f'Q1: {q1:.2f}'),
        dict(name="mean", y=mean, text=f'Mean: {mean:.2f}±{std:.2f}'),
        dict(name="median", y=median, text=f'Median: {median:.2f}'),
        dict(name="q3", y=q3, text=f'Q3: {q3:.2f}'),
        dict(name="upper", y=up_fence, text=f'Upper: {up_fence:.2f}'),
        dict(name="max", y=max_, text=f'Max: {max_:.2f}'),
    ]
    del lw_fence, up_fence
    
    fig = go.Figure(layout=px.box(data, y=data.name).layout)
    fig.add_trace(go.Box(
        y=arr,
        name=feature_title,
        boxpoints="outliers",
        boxmean=True,
        whiskerwidth=0.75,
        marker={
            "color": "rgba(90, 188, 110, 127)",
            "line": {
                "color": "red",
                "width": 3,
            }
        },
    ))
    del arr

    # Parameters for every values
    common_annotation_params = dict(
        font=dict(size=18, color="#ffffff"),
        showarrow=False,
        bgcolor=fig.data[0]["marker"]["color"], # Get same colour as the facet plot
        xref="x", # Specify which facet to put the annotation; Goes like x, x2, x3 ... xn.
        x=0.275,
        xanchor="left", # Align all the labels on x axis
    )

    # Values that need to be on the "left" (anchor: right) instead of "right" of the Box
    #   Move because of overlapping values in graph
    anchor_right = set(value_left)
    for annot in annots:
        annot = {**annot, **common_annotation_params}
        cur_name = annot["name"]
        if cur_name in offset:
            annot["x"] += offset[cur_name]
        if cur_name in anchor_right:
            annot["x"] *= -1
            annot["xanchor"] = "right"
        del cur_name
        fig.add_annotation(annot)
    del common_annotation_params, annot, annots, anchor_right

    # Update font size and turn off legend
    fig.update_layout(
        title=dict(
            text=f"Box Whisker Plot for \"{feature_title}\" Feature",
            font=dict(
                size=24
            ),
        ),
        showlegend=False,
        yaxis=dict(title_text=unit),
        font=dict(
            size=18
        ),
        margin=dict(
            l=110, r=50,
            t=75, b=75,
        )
    )

    # Display
    fig.show()

    # Save images
    fig.write_image(f"./../../images/{file_path}.png", width=WIDTH, height=HEIGHT, scale=1.0)
    if svg:
        fig.write_image(f"./../../images/{file_path}.svg", width=WIDTH, height=HEIGHT, scale=1.0)
    del fig

    return dict(
        min=min_,
        max=max_,
        mean=mean,
        std=std,
        median=median,
        q1=q1,
        q3=q3,
        iqr=iqr,
        lw_limit=lw_limit,
        up_limit=up_limit,
    )

def main() -> None:
    return

if __name__ == "__main__":
    main()