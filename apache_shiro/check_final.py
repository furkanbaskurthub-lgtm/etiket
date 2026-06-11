import json
from pathlib import Path
base = Path(r"c:\Users\Admin\Desktop\trino\apache_shiro")
with open(base/"Agent4_Output_apache_shiro_final.json", encoding="utf-8") as f:
    d = json.load(f)

cb_ids = {cb["context_bundle_id"] for cb in d["context_bundles"]}
print("Total CBs:", len(d["context_bundles"]))
print("Existing CB IDs (sorted last 5):", sorted(cb_ids)[-5:])

supp_hars = ["HAR-034","HAR-035","HAR-036","HAR-037","HAR-038"]
te_cb_map = {}
for te in d["training_examples"]:
    har_ref = "HAR-" + te["training_example_id"].split("HAR-")[1]
    te_cb_map[har_ref] = te["input"]["context_bundle"]["context_bundle_id"]
print("\nSupplementary HAR -> CB refs:")
for hid in supp_hars:
    print(f"  {hid} -> {te_cb_map.get(hid,'N/A')}")

nc = [h for h in d["human_analysis_records"] if h.get("outcome")=="not_crypto"]
print(f"\nnot_crypto count: {len(nc)}")
gdc_domain = {g["human_analysis_record_ref"]: g["coverage_contribution"]["domain"] for g in d["golden_dataset_candidates"]}
for h in nc:
    hid = h["analysis_record_id"]
    print(f"  {hid}: {gdc_domain.get(hid,'?')}")

ss = d.get("structural_scan", {})
print("\nstructural_scan top keys:", list(ss.keys()))
if "file_inventory" in ss:
    fi = ss["file_inventory"]
    print("  file_inventory type:", type(fi).__name__)
    if isinstance(fi, list):
        print("  file_inventory count:", len(fi))
        if fi:
            print("  first item keys:", list(fi[0].keys()) if isinstance(fi[0], dict) else fi[0])
    elif isinstance(fi, dict):
        print("  file_inventory keys:", list(fi.keys())[:5])
if "crypto_grep_hits" in ss:
    gh = ss["crypto_grep_hits"]
    print("  crypto_grep_hits type:", type(gh).__name__, "count:", len(gh) if isinstance(gh, list) else "?")
