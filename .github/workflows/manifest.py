import os
import json

from worlds.Files import APWorldContainer

manifest_path = "worlds/megamix/archipelago.json"
APWC = APWorldContainer()

manifest = {}
if os.path.isfile(manifest_path):
    manifest = json.load(open(manifest_path))
    assert "game" in manifest
    APWC.game = manifest.get("game")
manifest.update(APWC.get_manifest())

with open(manifest_path, "w") as file:
    file.write(json.dumps(manifest))
