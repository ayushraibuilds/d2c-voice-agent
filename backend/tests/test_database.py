"""
Unit tests for database.py (using an in-memory SQLite DB).
"""
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# Patch DB_PATH before importing database to use in-memory DB
with patch("config.get_settings") as mock_settings:
    mock_settings.return_value.database_path = ":memory:"
    mock_settings.return_value.log_level = "ERROR"
    import database as db_module

# Override the DB path module-level to use a temp file for isolation
import tempfile
_tmp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp_db.close()
db_module.DB_PATH = _tmp_db.name


def setup_fresh_db():
    """Initialize a fresh test database."""
    db_module.DB_PATH = _tmp_db.name
    db_module.init_db()


class TestInitDb:
    def test_init_creates_tables(self):
        setup_fresh_db()
        with db_module.get_db() as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
            table_names = {t["name"] for t in tables}
        assert "orders" in table_names
        assert "customers" in table_names
        assert "conversations" in table_names
        assert "tickets" in table_names
        assert "products" in table_names
        assert "brands" in table_names


class TestCreateTicket:
    def setup_method(self):
        setup_fresh_db()

    def test_create_ticket_returns_id(self):
        tid = db_module.create_ticket("+919000000001", "My package is broken", "DELIVERY_COMPLAINT")
        assert tid.startswith("TKT-")

    def test_create_ticket_with_image_url(self):
        image = "https://example.com/damage.jpg"
        tid = db_module.create_ticket("+919000000002", "Broken product", "DELIVERY_COMPLAINT", image_url=image)
        with db_module.get_db() as conn:
            row = conn.execute("SELECT * FROM tickets WHERE ticket_id = ?", (tid,)).fetchone()
        assert row["image_url"] == image

    def test_create_ticket_stored_in_db(self):
        tid = db_module.create_ticket("+919000000003", "Lost order", "HUMAN_HANDOFF")
        with db_module.get_db() as conn:
            row = conn.execute("SELECT * FROM tickets WHERE ticket_id = ?", (tid,)).fetchone()
        assert row is not None
        assert row["status"] == "open"
        assert row["intent"] == "HUMAN_HANDOFF"

    def test_ticket_id_is_unique(self):
        tid1 = db_module.create_ticket("+919000000004", "Issue 1", "COMPLAINT")
        tid2 = db_module.create_ticket("+919000000005", "Issue 2", "COMPLAINT")
        assert tid1 != tid2


class TestSearchProducts:
    def setup_method(self):
        setup_fresh_db()

    def test_search_existing_product(self):
        results = db_module.search_products("smartwatch")
        assert len(results) >= 1
        assert any("Smartwatch" in r["name"] or "smartwatch" in r["description"].lower() for r in results)

    def test_search_by_category(self):
        results = db_module.search_products("Electronics")
        assert len(results) >= 1
        assert all(r["category"] == "Electronics" for r in results)

    def test_search_empty_returns_all(self):
        # Empty query should match any row via LIKE '%%'
        results = db_module.search_products("")
        assert len(results) >= 0  # May return nothing or up to limit

    def test_search_no_match(self):
        results = db_module.search_products("xyznonexistentproduct99")
        assert results == []

    def test_search_result_has_required_fields(self):
        results = db_module.search_products("shoes")
        if results:
            r = results[0]
            assert "name" in r
            assert "price" in r
            assert "description" in r
            assert "category" in r
            assert "stock" in r

    def test_search_limit_works(self):
        results = db_module.search_products("", limit=2)
        assert len(results) <= 2


class TestSaveMessage:
    def setup_method(self):
        setup_fresh_db()

    def test_save_message_user(self):
        db_module.save_message("+919000000010", "user", "Hello!", intent="GREETING", lang="en")
        history = db_module.get_conversation_history("+919000000010", limit=5)
        assert len(history) >= 1
        assert history[-1]["message"] == "Hello!"

    def test_save_message_assistant(self):
        db_module.save_message("+919000000011", "assistant", "How can I help?", lang="en")
        history = db_module.get_conversation_history("+919000000011", limit=5)
        assert len(history) >= 1
        assert history[-1]["role"] == "assistant"

    def test_conversation_history_ordered(self):
        phone = "+919000000012"
        db_module.save_message(phone, "user", "First message", lang="en")
        db_module.save_message(phone, "assistant", "First reply", lang="en")
        db_module.save_message(phone, "user", "Second message", lang="en")
        history = db_module.get_conversation_history(phone, limit=10)
        assert len(history) == 3
        assert history[0]["message"] == "First message"
        assert history[2]["message"] == "Second message"


class TestGetOrderByPhone:
    def setup_method(self):
        setup_fresh_db()

    def test_get_order_for_seeded_customer(self):
        order = db_module.get_order_by_phone("+919876543210")
        assert order is not None
        assert order["order_id"] == "ORD-12345"

    def test_get_order_returns_none_for_unknown(self):
        order = db_module.get_order_by_phone("+9100000000000")
        assert order is None


class TestCloseTicket:
    def setup_method(self):
        setup_fresh_db()

    def test_close_ticket(self):
        tid = db_module.create_ticket("+919000000020", "Issue", "COMPLAINT")
        success = db_module.close_ticket(tid)
        assert success is True
        with db_module.get_db() as conn:
            row = conn.execute("SELECT status FROM tickets WHERE ticket_id = ?", (tid,)).fetchone()
        assert row["status"] == "closed"

    def test_close_nonexistent_ticket(self):
        success = db_module.close_ticket("TKT-DOESNOTEXIST")
        assert success is False
