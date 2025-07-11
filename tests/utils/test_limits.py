import pytest
from app.models import Usage, User
from app.utils.limits import update_usage
from app import db
from datetime import datetime, timezone

# Dummy user ID for isolated tests
@pytest.fixture
def user_id(app):
    with app.app_context():
        user = User(id=1, email="limituser@example.com", password="fakehash")
        db.session.add(user)
        db.session.commit()
    return 1

# Dummy feature name to simulate usage tracking
@pytest.fixture
def feature_name():
    return "limit"

# Test that first-time usage is allowed and recorded
def test_first_usage_allowed(app, user_id, feature_name):
    with app.app_context():
        result = update_usage(user_id, feature_name)
        assert result is True

        usage = db.session.execute(
            db.select(Usage).where(
                Usage.user_id == user_id,
                Usage.feature == feature_name,
                Usage.date == datetime.now(timezone.utc).date()
            )
        ).scalar_one()
        assert usage.count == 1

# Test that usage is allowed up to 3 times and blocked on the 4th
def test_multiple_usages(app, user_id, feature_name):
    with app.app_context():
        for i in range(3):
            allowed = update_usage(user_id, feature_name)
            assert allowed is True

        # 4th should be blocked
        blocked = update_usage(user_id, feature_name)
        assert blocked is False

        usage = db.session.execute(
            db.select(Usage).where(
                Usage.user_id == user_id,
                Usage.feature == feature_name,
                Usage.date == datetime.now(timezone.utc).date()
            )
        ).scalar_one()
        assert usage.count == 3