# Troubleshooting

## Common Issues

### Issue: `ImportError: No module named 'src'`
**Solution:** Ensure you're running from the project root.
```bash
export PYTHONPATH=$(pwd)
```

### Issue: `psql: command not found`
**Solution:** Install PostgreSQL and ensure it's added to your system path.

### Issue: `JWT Token Expired`
**Solution:** Use the refresh token to obtain a new access token.
```bash
POST /api/v1/users/refresh
```

---


