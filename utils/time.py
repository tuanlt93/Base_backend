from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

# =============================================================================
#  Time Utilities
# =============================================================================

# Múi giờ dùng cho Việt Nam
VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")

# ---------------------------------------------------------------------------
# Lấy thời gian hiện tại (UTC)
# ---------------------------------------------------------------------------
def now_utc() -> datetime:
    """
    Trả về thời gian hiện tại theo UTC (timezone-aware).
    """
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Lấy thời gian hiện tại theo múi giờ Việt Nam
# ---------------------------------------------------------------------------
def now_vn() -> datetime:
    """
    Trả về thời gian hiện tại tại Việt Nam (Asia/Ho_Chi_Minh).
    """
    return datetime.now(VN_TZ)


# ---------------------------------------------------------------------------
# Lấy thời gian hiện tại theo bất kỳ quốc gia nào
# ---------------------------------------------------------------------------
def now_timezone(tz_name: str) -> datetime:
    """
    Lấy thời gian hiện tại theo tên timezone, ví dụ:
    - "Asia/Ho_Chi_Minh"
    - "America/New_York"
    - "Europe/Berlin"
    """
    return datetime.now(ZoneInfo(tz_name))


# ---------------------------------------------------------------------------
# Chuyển đổi thời gian sang timezone khác
# ---------------------------------------------------------------------------
def to_timezone(dt: datetime, tz_name: str) -> datetime:
    """
    Chuyển đổi datetime sang timezone khác.
    Datetime phải là timezone-aware.
    """
    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    return dt.astimezone(ZoneInfo(tz_name))


# ---------------------------------------------------------------------------
# Thêm phút / giờ / ngày
# ---------------------------------------------------------------------------
def add_minutes(dt: datetime, minutes: int) -> datetime:
    return dt + timedelta(minutes=minutes)

def add_hours(dt: datetime, hours: int) -> datetime:
    return dt + timedelta(hours=hours)

def add_days(dt: datetime, days: int) -> datetime:
    return dt + timedelta(days=days)


# ---------------------------------------------------------------------------
# Format datetime thành string chuẩn ISO 8601
# ---------------------------------------------------------------------------
def to_iso(dt: datetime) -> str:
    """
    Convert datetime sang chuỗi ISO 8601.
    """
    return dt.isoformat()


# ---------------------------------------------------------------------------
# Parse ISO string thành datetime có timezone
# ---------------------------------------------------------------------------
def from_iso(text: str) -> datetime:
    """
    Parse chuỗi ISO thành datetime timezone-aware.
    """
    return datetime.fromisoformat(text)
