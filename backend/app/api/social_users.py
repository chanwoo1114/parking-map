from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from app.core.config import settings
from app.db.connect import AsyncDBPool
# from app.core.dependencies import get_current_active_user
import httpx


router = APIRouter(prefix="/users/social", tags=["social_user"])

@router.get("/{provider}")
async def social_login(provider: str):
    if provider == "kakao":
        params = {
            "client_id": settings.KAKAO_CLIENT_ID,
            "redirect_uri": settings.KAKAO_REDIRECT_URI,
            "response_type": "code",
            "scope": "account_email profile_nickname",
        }
        url = httpx.URL("https://kauth.kakao.com/oauth/authorize", params=params)

    # elif provider == "naver":
    #     state = os.urandom(16).hex()
    #     params = {
    #         "client_id": settings.NAVER_CLIENT_ID,
    #         "redirect_uri": settings.NAVER_REDIRECT_URI,
    #         "response_type": "code",
    #         "state": state,
    #     }
    #     url = httpx.URL("https://nid.naver.com/oauth2.0/authorize", params=params)
    #
    # elif provider == "google":
    #     params = {
    #         "client_id": settings.GOOGLE_CLIENT_ID,
    #         "redirect_uri": settings.GOOGLE_REDIRECT_URI,
    #         "response_type": "code",
    #         "scope": "openid email profile",
    #         "access_type": "offline",
    #     }
    #     url = httpx.URL("https://accounts.google.com/o/oauth2/v2/auth", params=params)
    #
    # else:
    #     raise HTTPException(status_code=400, detail="Unsupported provider")

    return RedirectResponse(str(url))

@router.get("/social/{provider}/callback")
async def social_callback(provider: str, code: str, state: str = None):
    async with httpx.AsyncClient() as client:
        if provider == "kakao":
            resp = await client.post(
                "https://kauth.kakao.com/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "client_id": settings.KAKAO_CLIENT_ID,
                    "client_secret": settings.KAKAO_CLIENT_SECRET,
                    "redirect_uri": settings.KAKAO_REDIRECT_URI,
                    "code": code,
                },
            )
            resp.raise_for_status()
            kakao_at = resp.json()["access_token"]
            # 프로필 조회
            prof = await client.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {kakao_at}"},
            )
            prof.raise_for_status()
            data = prof.json()
            external_id = str(data["id"])
            acct = data.get("kakao_account", {})
            email = acct.get("email")
            nickname = acct.get("profile", {}).get("nickname")
#
#         elif provider == "naver":
#             # 네이버 토큰 교환
#             resp = await client.post(
#                 "https://nid.naver.com/oauth2.0/token",
#                 params={
#                     "grant_type": "authorization_code",
#                     "client_id": settings.NAVER_CLIENT_ID,
#                     "client_secret": settings.NAVER_CLIENT_SECRET,
#                     "code": code,
#                     "state": state,
#                 },
#             )
#             resp.raise_for_status()
#             naver_at = resp.json()["access_token"]
#             prof = await client.get(
#                 "https://openapi.naver.com/v1/nid/me",
#                 headers={"Authorization": f"Bearer {naver_at}"},
#             )
#             prof.raise_for_status()
#             resp_data = prof.json().get("response", {})
#             external_id = resp_data.get("id")
#             email = resp_data.get("email")
#             nickname = resp_data.get("nickname")
#
#         elif provider == "google":
#             # 구글 토큰 교환
#             resp = await client.post(
#                 "https://oauth2.googleapis.com/token",
#                 data={
#                     "grant_type": "authorization_code",
#                     "client_id": settings.GOOGLE_CLIENT_ID,
#                     "client_secret": settings.GOOGLE_CLIENT_SECRET,
#                     "redirect_uri": settings.GOOGLE_REDIRECT_URI,
#                     "code": code,
#                 },
#             )
#             resp.raise_for_status()
#             j = resp.json()
#             google_at = j.get("access_token")
#             prof = await client.get(
#                 "https://openidconnect.googleapis.com/v1/userinfo",
#                 headers={"Authorization": f"Bearer {google_at}"},
#             )
#             prof.raise_for_status()
#             data = prof.json()
#             external_id = data.get("sub")
#             email = data.get("email")
#             nickname = data.get("name")
#
#         else:
#             raise HTTPException(status_code=400, detail="Unsupported provider")
#

    user = await get_or_create_social_user(provider, external_id, email, nickname)

    access_jwt = create_access_token({"user_id": user.id})
    refresh_jwt = create_refresh_token({"user_id": user.id})

    frontend = settings.FRONTEND_URL.rstrip("/")
    redirect_url = f"{frontend}/oauth-success?access_token={access_jwt}&refresh_token={refresh_jwt}"

    return RedirectResponse(redirect_url)