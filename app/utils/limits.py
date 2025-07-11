from datetime import datetime, timezone
from app import db
from app.models import Usage

# Track and limit daily usage of a specific feature per user
def update_usage(user_id, feature):
    today = datetime.now(timezone.utc).date()

    # Check if user has already used this feature today
    usage = db.session.execute(
        db.select(Usage).where(
            Usage.user_id == user_id,
            Usage.feature == feature,
            Usage.date == today
        )
    ).scalar_one_or_none()

    # Block if limit reached
    if usage and usage.count >= 3:
        return False

    # Increment existing usage or create new record
    if usage:
        usage.count += 1
    else:
        usage = Usage(user_id=user_id, feature=feature, date=today, count=1)
        db.session.add(usage)

    db.session.commit()
    return True