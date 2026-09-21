import pandas as pd

from run_pipeline import main


def test_pipeline_incremental_success(monkeypatch, tmp_path):
    customers = pd.DataFrame({
        "id": [5],
        "nama": ["Eka"],
        "umur": [29],
        "kota": ["Bandung"],
        "total_belanja": [350000],
        "updated_at": pd.to_datetime(
            ["2026-09-21 13:00:00"]
        ),
    })

    orders = pd.DataFrame({
        "order_id": [105],
        "customer_id": [5],
        "amount": [325000],
        "updated_at": pd.to_datetime(
            ["2026-09-21 14:00:00"]
        ),
    })

    monkeypatch.setattr(
        "run_pipeline.extract_incremental_customers",
        lambda watermark: customers,
    )

    monkeypatch.setattr(
        "run_pipeline.extract_incremental_orders",
        lambda watermark: orders,
    )

    monkeypatch.setattr(
        "run_pipeline.extract_customers",
        lambda: customers,
    )

    monkeypatch.setattr(
        "run_pipeline.extract_orders",
        lambda: orders,
    )

    monkeypatch.setattr(
        "run_pipeline.REJECTED_DIR",
        tmp_path,
    )

    loaded = {
        "customers": None,
        "orders": None,
        "customer_watermark": None,
        "order_watermark": None,
    }

    class FakeCursor:
        def execute(self, *args, **kwargs):
            pass

        def fetchone(self):
            return (
                pd.Timestamp("2026-09-21 12:00:00"),
            )

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    class FakeConnection:
        def cursor(self):
            return FakeCursor()

        def commit(self):
            loaded["committed"] = True

        def rollback(self):
            loaded["rollback"] = True

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    def fake_connection():
        return FakeConnection()

    monkeypatch.setattr(
        "run_pipeline.get_connection",
        fake_connection,
    )

    def fake_load_customers(conn, df):
        loaded["customers"] = df.copy()

    def fake_load_orders(conn, df):
        loaded["orders"] = df.copy()

    def fake_soft_delete_customers(conn, ids):
        loaded["customer_ids"] = ids

    def fake_soft_delete_orders(conn, ids):
        loaded["order_ids"] = ids

    monkeypatch.setattr(
        "run_pipeline.load_customers",
        fake_load_customers,
    )

    monkeypatch.setattr(
        "run_pipeline.load_orders",
        fake_load_orders,
    )

    monkeypatch.setattr(
        "run_pipeline.soft_delete_missing_customers",
        fake_soft_delete_customers,
    )

    monkeypatch.setattr(
        "run_pipeline.soft_delete_missing_orders",
        fake_soft_delete_orders,
    )

    def fake_update_watermark(
        conn,
        pipeline_name,
        watermark,
    ):
        if pipeline_name == "customer_pipeline":
            loaded["customer_watermark"] = watermark

        if pipeline_name == "order_pipeline":
            loaded["order_watermark"] = watermark

    monkeypatch.setattr(
        "run_pipeline.update_last_successful_run",
        fake_update_watermark,
    )

    main()

    assert loaded["customers"] is not None
    assert loaded["orders"] is not None

    assert loaded["customers"].iloc[0]["id"] == 5
    assert loaded["orders"].iloc[0]["order_id"] == 105

    assert (
        loaded["customer_watermark"]
        == pd.Timestamp("2026-09-21 13:00:00")
    )

    assert (
        loaded["order_watermark"]
        == pd.Timestamp("2026-09-21 14:00:00")
    )

    assert loaded["committed"] is True
    assert "rollback" not in loaded
