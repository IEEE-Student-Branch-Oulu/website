# auth/ — placeholder

This module is deliberately empty. Member registration & login are planned
as a follow-up so that the backend foundation can land first without churn.

## Decisions deferred to the auth plan

- **Session cookies vs JWT.** Likely cookies — first-party SPA, no refresh
  token logic, fewer XSS-via-localStorage worries. Reconsider if we ever need
  cross-origin / mobile clients.
- **Password hashing:** lean toward `argon2-cffi` over `passlib[bcrypt]`.
- **User model location:** `app/domains/members/models.py`. `auth/` will
  hold only login/logout/register routers and a `get_current_user` dependency.
- **IEEE / OAuth as v2.** After password auth ships, add OAuth via
  `authlib` so members can sign in with IEEE credentials — strong identity
  fit for a branch site.

## Already in place for when auth lands

- `Settings.auth.secret_key` exists and is read from `AUTH_SECRET_KEY`.
- `.env.example` ships a placeholder so adding real auth doesn't churn the
  config layer.
- The `deps.py` shape (Annotated dependencies) is ready for a
  `CurrentUser = Annotated[User, Depends(get_current_user)]` to slot in.
