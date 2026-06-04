"""Map Google Gemini / Pydantic AI errors to user-friendly Persian HTTP responses."""

from __future__ import annotations

from typing import Any

import httpx
from fastapi import HTTPException
from pydantic_ai.exceptions import ModelHTTPError


def extract_google_error_message(body: object | None) -> str:
    if body is None:
        return ""
    if isinstance(body, dict):
        error = body.get("error")
        if isinstance(error, dict):
            message = error.get("message")
            if isinstance(message, str):
                return message
            status = error.get("status")
            if isinstance(status, str):
                return status
        message = body.get("message")
        if isinstance(message, str):
            return message
    return str(body)


def parse_gemini_error(exc: Exception) -> tuple[int, str] | None:
    if isinstance(exc, ModelHTTPError):
        return exc.status_code, extract_google_error_message(exc.body)

    if isinstance(exc, httpx.HTTPStatusError):
        try:
            body: Any = exc.response.json()
        except ValueError:
            body = exc.response.text
        message = (
            extract_google_error_message(body) if isinstance(body, dict) else str(body)
        )
        return exc.response.status_code, message

    return None


def classify_gemini_http_error(status_code: int, message: str) -> tuple[int, str]:
    msg_lower = message.lower()

    if status_code == 403 and (
        "dunning" in msg_lower or "lightning dunning" in msg_lower
    ):
        return (
            403,
            "دسترسی به Gemini رد شد: حساب Google Cloud یا پرداخت این پروژه مسدود است. "
            "در Google AI Studio یا Cloud Console وضعیت billing را بررسی و پرداخت را فعال کنید.",
        )

    if status_code == 401 or "api key" in msg_lower or "unauthenticated" in msg_lower:
        return (
            401,
            "کلید API گوگل نامعتبر یا تنظیم نشده است. GOOGLE_API_KEY را در .env بررسی کنید.",
        )

    if status_code == 429 or "quota" in msg_lower or "rate limit" in msg_lower:
        return (
            429,
            "سهمیه یا نرخ درخواست Gemini تمام شده است. کمی بعد دوباره تلاش کنید.",
        )

    if status_code == 403:
        return (
            403,
            "دسترسی به Gemini مجاز نیست. کلید API، billing و دسترسی مدل را بررسی کنید.",
        )

    if status_code == 404 or "not found" in msg_lower:
        return (
            502,
            "مدل Gemini پیکربندی‌شده یافت نشد. GEMINI_MODEL را در .env بررسی کنید.",
        )

    if status_code >= 500:
        return (
            502,
            "سرویس Gemini موقتاً در دسترس نیست. بعداً دوباره تلاش کنید.",
        )

    return (
        502,
        f"خطا در ارتباط با Gemini ({status_code}): {message or 'خطای ناشناخته'}",
    )


def http_exception_from_gemini_error(
    exc: Exception, *, context: str = "پردازش"
) -> HTTPException:
    parsed = parse_gemini_error(exc)
    if parsed is None:
        return HTTPException(
            status_code=502,
            detail=f"خطا در {context}: {exc}",
        )

    status_code, message = parsed
    http_status, detail = classify_gemini_http_error(status_code, message)
    return HTTPException(status_code=http_status, detail=detail)


def raise_for_gemini_response(response: httpx.Response) -> None:
    if response.is_success:
        return
    try:
        body: Any = response.json()
    except ValueError:
        body = response.text
    message = (
        extract_google_error_message(body) if isinstance(body, dict) else str(body)
    )
    http_status, detail = classify_gemini_http_error(response.status_code, message)
    raise HTTPException(status_code=http_status, detail=detail)
