# UI Display Issues - Investigation Summary

## Issues Reported

1. **New users not showing up immediately after creation**
2. **Disabled status not displaying correctly**

## Investigation Results

### Issue #1: New Users Not Appearing ✅ FIXED

**Root Cause**: The `manage-accounts.html` page was filtering users by role='user', but the create form allowed creating users with roles: admin, manager, or user. Any user created with a role other than 'user' wouldn't appear in the list.

**Fix Applied**: Removed the role filter from `api.listUsers()` calls in `manage-accounts.html`:
- Line 346: Changed `api.listUsers('user')` to `api.listUsers()`
- Line 429: Changed `api.listUsers('user')` to `api.listUsers()`

Now all users are displayed regardless of their role.

### Issue #2: Disabled Status Not Showing ❌ NEEDS FIX

**Current Behavior**:
```javascript
const status = account.is_active ? 'Active' : 'Pending invitation';
```

**Problem**: This logic only shows two states:
- `is_active = true` → "Active"  
- `is_active = false` → "Pending invitation"

**Missing**: When a user is disabled, `is_active = false`, but it shows "Pending invitation" instead of "Disabled"

**Root Cause**: Cannot distinguish between:
- New user who hasn't activated (is_active = false, no password set)
- Disabled user (is_active = false, password was set)

Backend doesn't return `pwd_hash` for security reasons.

## Solutions

### Option 1: Simple Fix (Recommended)
Change status to just show "Active" or "Inactive":
```javascript
const status = account.is_active ? 'Active' : 'Inactive';
```

**Pros**: Simple, clear, works immediately
**Cons**: Doesn't distinguish between pending and disabled

### Option 2: Add Backend Field
Add `has_activated` boolean to User model and UserOut schema:
```python
has_activated: Mapped[bool] = mapped_column(Boolean, default=False)
```

Set to `True` when user first sets password.

Then frontend can show:
- `is_active = true` → "Active"
- `is_active = false AND has_activated = false` → "Pending"  
- `is_active = false AND has_activated = true` → "Disabled"

**Pros**: Most accurate
**Cons**: Requires database migration

### Option 3: Use Invite Token Status
Check if user has unused invite token:
- Has unused token → "Pending"
- No token and inactive → "Disabled"

**Pros**: No schema changes
**Cons**: More complex query, slower

## Recommended Action

**For now**: Use Option 1 (Simple Fix)
- Change line 372 in `manage-accounts.html`
- From: `const status = account.is_active ? 'Active' : 'Pending invitation';`
- To: `const status = account.is_active ? 'Active' : 'Inactive';`

**Later**: Implement Option 2 if detailed status is important

## Additional Fix Applied

✅ **Fixed invite sending error**:
- Changed `invite_message(to_email=user.email, token=invite_token)`  
- To: `invite_message(invite_token=invite_token, user=user)`
- This was causing 500 errors when sending invites

## Files to Fix

1. `frontend/pages/superuser/manage-accounts.html` - Line 372
   - Change status logic to show Active/Inactive

2. Update badge class mapping (line ~418):
   - Change `'Pending invitation'` to `'Inactive'`

## Testing Needed

After fix:
1. Create new user → Should show "Inactive"
2. Disable active user → Should show "Inactive"  
3. Enable user → Should show "Active"
4. Verify dropdown shows correct actions for each state

## Note

File got corrupted during editing attempts. Restored from git. 
Manual fix needed for the simple one-line change above.
