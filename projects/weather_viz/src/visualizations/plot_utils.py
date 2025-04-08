def apply_common_layout(fig, title):
    fig.update_layout(
        title=title,
        xaxis_tickangle=-45,
        template="plotly_white",
        margin=dict(t=60, b=40)
    )
    return fig
