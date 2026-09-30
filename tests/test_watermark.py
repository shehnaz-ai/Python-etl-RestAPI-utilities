from etl_utils.watermark import WatermarkStore


def test_watermark_set_and_get(tmp_path):

    path = tmp_path / "watermarks.json"

    store = WatermarkStore(str(path))

    assert store.get("customers") is None

    store.set(
        "customers",
        "2026-09-30T10:00:00",
    )

    assert (
            store.get("customers")
            == "2026-09-30T10:00:00"
    )