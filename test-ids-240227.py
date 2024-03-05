# %% Imports JGTIDS
import jgtpy.JGTIDS as ids
import jgtpy.JGTPDSP as pds


# %%
# Instrument
i = "CORNF"  # @STCIssue M1 (74f), W1 (less than 313 frames)
i = "EUR/USD"
i = "WHEATF"
i = "SPX500"
t = "M1"
t = "W1"
t = "D1"

# %%
p = pds.getPH(i, t)
len(p)

# %% JGTIDSRequest
rq = ids.JGTIDSRequest()
rq.flag_AOF = False
rq.BigAlligator = False
rq.MFI = False
rq.rounding_decimal_min = 2

# %%
i2 = ids.ids_add_indicators(
    p, bypass_index_reset=False, quiet=True, big_alligator=True, rq=rq
)

# %%
i = ids.tocds(p, rq=rq)

# %%
i.to_csv("test-ids-240227.csv")
# %%
i

# %%
