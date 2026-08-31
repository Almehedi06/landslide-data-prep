from __future__ import annotations

import os
import time
import zipfile

import requests


def download_file(
    url: str,
    out_path: str,
    timeout: int = 60,
    chunk_mb: int = 16,
    retries: int = 3,
) -> str:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    for attempt in range(retries):
        try:
            with requests.get(url, stream=True, timeout=timeout) as resp:
                resp.raise_for_status()
                with open(out_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=chunk_mb * 1024 * 1024):
                        if chunk:
                            f.write(chunk)
            return out_path
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(3)


def extract_first_tif(zip_path: str, extract_dir: str) -> str:
    return _extract_and_list_tifs(zip_path, extract_dir)[0]


def extract_tif_by_suffix(zip_path: str, extract_dir: str, suffix: str) -> str:
    """Extract a zip and return the .tif whose name ends with `suffix`.

    BAER "preliminary" bundles contain multiple .tif files (dNBR plus
    pre/post reflectance composites) - picking "the first tif" is not
    reliable, so callers that know the product they want (e.g. "_dnbr.tif")
    should use this instead of extract_first_tif.
    """
    tif_paths = _extract_and_list_tifs(zip_path, extract_dir)
    matches = [
        p
        for p in tif_paths
        if os.path.basename(p).lower().endswith(suffix.lower())
    ]
    if not matches:
        raise FileNotFoundError(
            f"No .tif ending in {suffix!r} inside {zip_path}. Found: {tif_paths}"
        )
    return matches[0]


def _extract_and_list_tifs(zip_path: str, extract_dir: str) -> list[str]:
    if os.path.exists(extract_dir):
        import shutil

        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)

    tif_paths = []
    for root, _, files in os.walk(extract_dir):
        for name in files:
            if name.lower().endswith(".tif"):
                tif_paths.append(os.path.join(root, name))

    if not tif_paths:
        raise FileNotFoundError(f"No .tif found inside {zip_path}")

    return tif_paths
