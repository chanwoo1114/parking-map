from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse, RedirectResponse
import httpx

from app.core.config import settings
from app.db.queries.social_user_queries import get_social_user, create_social_user
from app.core.security import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth/social", tags=["social_user"])

@router.get("/{provider}")
async def social_login(provider: str):
    if provider == "kakao":
        params = {
            "client_id":    settings.KAKAO_CLIENT_ID,
            "redirect_uri": settings.KAKAO_REDIRECT_URI,
            "response_type":"code",
            "scope":        "account_email profile_nickname",
            "prompt":       "login",
        }
        url = httpx.URL("https://kauth.kakao.com/oauth/authorize", params=params)

    elif provider == "google":
        params = {
            "client_id":     settings.GOOGLE_CLIENT_ID,
            "redirect_uri":  settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope":         "openid email profile",
            "access_type":   "offline",
            "prompt":        "consent",
        }
        url = httpx.URL("https://accounts.google.com/o/oauth2/v2/auth", params=params)

    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    return RedirectResponse(str(url))


@router.get("/{provider}/callback")
async def social_callback(
    provider: str,
    code: str,
    state: str = Query(None)  # Naver 용
):
    # 1) 토큰 교환
    async with httpx.AsyncClient() as client:
        if provider == "kakao":
            token_resp = await client.post(
                "https://kauth.kakao.com/oauth/token",
                data={
                    "grant_type":    "authorization_code",
                    "client_id":     settings.KAKAO_CLIENT_ID,
                    "client_secret": settings.KAKAO_CLIENT_SECRET,
                    "redirect_uri":  settings.KAKAO_REDIRECT_URI,
                    "code":          code,
                },
            )

        elif provider == "google":
            token_resp = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "grant_type":    "authorization_code",
                    "client_id":     settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri":  settings.GOOGLE_REDIRECT_URI,
                    "code":          code,
                },
            )

        else:
            raise HTTPException(status_code=400, detail="Unsupported provider")

    if token_resp.status_code != 200:
        detail = token_resp.json().get("error_description", token_resp.text)
        raise HTTPException(status_code=400, detail=f"{provider} token exchange failed: {detail}")

    tokens = token_resp.json()
    access_token = tokens.get("access_token")

    async with httpx.AsyncClient() as client:
        if provider == "kakao":
            profile_resp = await client.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            profile = profile_resp.json()
            pid      = str(profile["id"])
            email    = profile["kakao_account"].get("email")
            nickname = profile["properties"].get("nickname")

        elif provider == "naver":
            profile_resp = await client.get(
                "https://openapi.naver.com/v1/nid/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            profile = profile_resp.json()["response"]
            pid      = profile["id"]
            email    = profile.get("email")
            nickname = profile.get("nickname") or profile.get("name")

        elif provider == "google":
            profile_resp = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            profile = profile_resp.json()
            pid      = profile["id"]
            email    = profile.get("email")
            nickname = profile.get("name")

    # 3) DB 저장/조회
    user = await get_social_user(provider, pid)
    user_id = user["id"] if user else await create_social_user(provider, pid, email, nickname)

    # 4) JWT 생성 & 반환
    access_jwt  = create_access_token({"user_id": user_id})
    refresh_jwt = create_refresh_token({"user_id": user_id})

    return JSONResponse({
        "success":       True,
        "access_token":  access_jwt,
        "refresh_token": refresh_jwt,
    })
