# The dashboard requires Bokeh and contourpy. This image does not need the
# telemetry web UI, and contourpy fails to cross-compile in EDF 26.06.1.
KRIA_PACKAGES:remove:kv260-accel-sdt = "kria-dashboard"
