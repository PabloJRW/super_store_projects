import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# DISTRIBUCIONES DE VARIABLES SIN ESCALAR
# ==============================================================================
def plotDistributions(dataframe:pd.DataFrame, title=None):
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))
    axes = axes.flat

    for i, feature in enumerate(dataframe.columns):
        sns.histplot(
            x       =dataframe[feature],
            kde     = True,
            color   = (list(plt.rcParams['axes.prop_cycle'])*2)[i]["color"],
            ax      = axes[i]
        )
        axes[i].set_title(feature, fontsize = 12, fontweight = "bold")
        axes[i].tick_params(labelsize = 9)
        axes[i].set_xlabel("")

    
    fig.tight_layout()
    fig.suptitle(title, y=1.1,fontsize = 15, fontweight = "bold")
    