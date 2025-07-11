# This program gives a warning -> "findfont: Font family 'Helvetica' not found."
# Ignore it
import pandas as pd
import calplot as cp
import matplotlib.pyplot as plt
import io
from flask import send_file

def make_heatmap(visits_info):

  data = pd.Series(visits_info)
  data.index = pd.to_datetime(data.index)

  fig, ax = cp.calplot(data, cmap="Greens", colorbar=False, vmin=0, vmax=5,
    edgecolor=None, suptitle="Learning Activity")
  
  buf = io.BytesIO()
  plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.1)
  buf.seek(0)
  plt.close(fig)

  return send_file(buf, mimetype="image/png")