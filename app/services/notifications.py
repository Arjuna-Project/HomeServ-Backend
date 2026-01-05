# app/services/notifications.py

def send_notification(user_id: int, message: str):
    """
    Generic notification sender.
    Replace with Email / SMS / Push service logic.
    """
    print(f"Notification sent to user {user_id}: {message}")


def send_booking_confirmation(booking):
    """
    Send booking confirmation to user.
    """
    msg = (
        f"Booking #{booking.booking_id} confirmed for service {booking.service_id} "
        f"on {booking.scheduled_at}."
    )
    send_notification(booking.user_id, msg)
